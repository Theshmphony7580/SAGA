"""
Analyst Agent Node: Generates Plotly charts and text narratives from data.

Operates in two modes:
1. Post-SQL: Analyzes results from the SQL Agent
2. Direct: Loads data from SQLite when routed directly by the Router

Uses Gemini Pro to generate Python/Plotly code, then executes it in a
restricted sandbox (only pd, np, px, df, print available).
"""

import json
from io import StringIO
from loguru import logger

from backend.ml.agents.state import GraphState
from backend.ml.agents.llm_gateway import LLMGateway
from backend.database.utils import read_dataframe_from_db


ANALYST_PROMPT = """You are a data analyst. Given a dataset and a user's question, write Python code that:
1. Creates a Plotly Express figure answering the question.
2. Prints a 2-3 sentence narrative explaining the key finding.

Available data:
- `df` is a pandas DataFrame already loaded with the data below.

Data (first rows):
{data_sample}

Schema:
{schema}

Rules:
- Use plotly.express (imported as px). Do NOT use plotly.graph_objects.
- Store the figure in a variable called `fig`.
- Print the narrative text using print().
- Do NOT call fig.show(). Do NOT use display().
- Do NOT import anything. pd, np, px, and df are already available.
- Output ONLY Python code. No markdown fences, no explanations.

User question: {question}
Code:"""


def _format_sql_results_as_csv(columns: list, rows: list) -> str:
    """Converts SQL Agent output into a CSV string for the analyst prompt."""
    if not columns or not rows:
        return "No data available."
    header = ",".join(columns)
    data_lines = [",".join(str(v) for v in row) for row in rows[:50]]  # Cap at 50 rows
    return header + "\n" + "\n".join(data_lines)


def _clean_code(raw_code: str) -> str:
    """Strips markdown fences and leading/trailing whitespace from LLM output."""
    code = raw_code.strip()
    if code.startswith("```python"):
        code = code[len("```python"):]
    elif code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    return code.strip()


def _execute_in_sandbox(code: str, data_csv: str) -> tuple:
    """
    Executes AI-generated Python code in a restricted namespace.

    Only pd, np, px, df, and print are available.
    No os, sys, subprocess, open, __import__ — prevents malicious code.

    Returns:
        (chart_json_dict or None, narrative_text)
    """
    import pandas as pd
    import numpy as np
    import plotly.express as px

    df = pd.read_csv(StringIO(data_csv))

    # Capture print output for narrative
    captured = StringIO()

    # Restricted namespace — NO os, sys, open, __import__
    namespace = {
        "pd": pd,
        "np": np,
        "px": px,
        "df": df,
        "print": lambda *args, **kwargs: captured.write(" ".join(str(a) for a in args) + "\n"),
        "__builtins__": {
            "range": range,
            "len": len,
            "int": int,
            "float": float,
            "str": str,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "bool": bool,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
            "sorted": sorted,
            "enumerate": enumerate,
            "zip": zip,
            "abs": abs,
            "True": True,
            "False": False,
            "None": None,
        },
    }

    exec(code, namespace)

    # Extract chart
    fig = namespace.get("fig")
    chart_json = json.loads(fig.to_json()) if fig else None

    # Extract narrative
    narrative = captured.getvalue().strip() or "Analysis complete."

    return chart_json, narrative


def analyst_agent_node(state: GraphState) -> dict:
    """
    LangGraph node: Generates Plotly charts + text narrative from data.

    Reads:  messages, schema_context, table_name,
            sql_result_columns, sql_result_rows (if from SQL Agent)
    Writes: chart_json, narrative, generated_code, current_agent, error
    """
    last_message = state["messages"][-1].content
    logger.info(f"[Analyst] Processing: '{last_message}'")

    # --- Phase 1: Build data context ---
    if state.get("sql_result_columns") and state.get("sql_result_rows"):
        # Post-SQL mode: use SQL Agent's results
        data_csv = _format_sql_results_as_csv(
            state["sql_result_columns"],
            state["sql_result_rows"],
        )
        logger.info(f"[Analyst] Using SQL result ({len(state['sql_result_rows'])} rows)")
    else:
        # Direct mode: load from SQLite
        try:
            df = read_dataframe_from_db(state["table_name"])
            data_csv = df.head(50).to_csv(index=False)
            logger.info(f"[Analyst] Loaded {len(df)} rows from '{state['table_name']}', using top 50")
        except Exception as e:
            logger.error(f"[Analyst] Failed to load data: {e}")
            return {
                "chart_json": None,
                "narrative": f"Could not load data for analysis: {str(e)}",
                "generated_code": None,
                "current_agent": "analyst_agent",
                "error": str(e),
            }

    # --- Phase 2: Generate Python/Plotly code via Gemini Pro ---
    try:
        llm = LLMGateway.get_power_llm()
        prompt = ANALYST_PROMPT.format(
            schema=state["schema_context"],
            data_sample=data_csv[:3000],  # Cap prompt size
            question=last_message,
        )
        response = llm.invoke(prompt)
        raw_code = response.content
        clean_code = _clean_code(raw_code)
        logger.info(f"[Analyst] Generated code ({len(clean_code)} chars)")

    except Exception as e:
        logger.error(f"[Analyst] LLM call failed: {e}")
        return {
            "chart_json": None,
            "narrative": f"Analysis generation failed: {str(e)}",
            "generated_code": None,
            "current_agent": "analyst_agent",
            "error": None,  # Non-fatal — we just skip the chart
        }

    # --- Phase 3: Execute in sandbox ---
    try:
        chart_json, narrative = _execute_in_sandbox(clean_code, data_csv)
        logger.info(f"[Analyst] Chart: {'generated' if chart_json else 'none'}, Narrative: {len(narrative)} chars")

        return {
            "chart_json": chart_json,
            "narrative": narrative,
            "generated_code": clean_code,
            "current_agent": "analyst_agent",
            "error": None,
        }

    except Exception as e:
        logger.warning(f"[Analyst] Sandbox execution failed: {e}")
        # Graceful fallback: narrative only, no chart
        return {
            "chart_json": None,
            "narrative": f"I wasn't able to generate a chart, but here's what I found: The query returned {len(state.get('sql_result_rows', []))} rows across columns: {', '.join(state.get('sql_result_columns', []))}.",
            "generated_code": clean_code,
            "current_agent": "analyst_agent",
            "error": None,  # Non-fatal
        }
