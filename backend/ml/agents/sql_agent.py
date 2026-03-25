"""
SQL Agent Node: Converts natural language to SQL, executes it, and self-corrects.

This LangGraph node replaces the old text2sql_engine.py (HuggingFace/Qwen)
with Gemini Pro via LLMGateway. Includes a self-correction loop that retries
up to 3 times when SQL execution fails.
"""

import sqlite3
from loguru import logger

from backend.config import DATABASE_FILE
from backend.ml.agents.state import GraphState
from backend.ml.agents.llm_gateway import LLMGateway
from backend.ml.sql_sanitize import validate_sql

MAX_RETRIES = 3

SQL_GENERATION_PROMPT = """You are an expert SQL generator for SQLite databases.

Schema:
{schema}

Rules:
- Use ONLY SELECT queries. No INSERT, UPDATE, DELETE, DROP, ALTER, CREATE.
- Use the EXACT table and column names from the schema above.
- Add LIMIT 100 if the user doesn't specify a row count.
- For aggregations (AVG, SUM, COUNT, etc.), use appropriate GROUP BY if needed.
- Output ONLY the raw SQL query. No explanations, no markdown fences, no commentary.
{error_section}
User question: {question}
SQL:"""


def _build_error_section(sql_error: str | None) -> str:
    """Builds the error feedback section for retry prompts."""
    if not sql_error:
        return ""
    return f"""
IMPORTANT: Your previous SQL attempt failed with this error:
{sql_error}
Fix the query to avoid this error. Double-check table and column names against the schema.
"""


def _execute_sql(sql: str) -> dict:
    """
    Executes a sanitized SQL query against the SQLite cache DB.
    Returns columns and rows, or raises on failure.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description] if cur.description else []
        return {
            "columns": columns,
            "rows": [list(row) for row in rows],  # Convert tuples to lists for JSON
        }
    finally:
        conn.close()


def sql_agent_node(state: GraphState) -> dict:
    """
    LangGraph node: Generates SQL from NL, executes it, self-corrects on failure.

    Reads:  messages, schema_context, table_name, sql_retry_count, sql_error
    Writes: generated_sql, sql_result_columns, sql_result_rows,
            sql_error, sql_retry_count, current_agent, error
    """
    last_message = state["messages"][-1].content
    schema_context = state["schema_context"]
    retry_count = state.get("sql_retry_count", 0)
    previous_error = state.get("sql_error")

    logger.info(f"[SQLAgent] Attempt {retry_count + 1}/{MAX_RETRIES} — Question: '{last_message}'")

    # --- Phase 1: Generate SQL via Gemini Pro ---
    try:
        llm = LLMGateway.get_power_llm()
        prompt = SQL_GENERATION_PROMPT.format(
            schema=schema_context,
            question=last_message,
            error_section=_build_error_section(previous_error),
        )
        response = llm.invoke(prompt)
        raw_sql = response.content.strip()
        logger.info(f"[SQLAgent] Raw SQL from Gemini: {raw_sql}")

    except Exception as e:
        logger.error(f"[SQLAgent] LLM call failed: {e}")
        return {
            "generated_sql": None,
            "sql_error": f"LLM call failed: {str(e)}",
            "sql_retry_count": retry_count + 1,
            "current_agent": "sql_agent",
            "error": f"SQL generation failed: {str(e)}" if retry_count + 1 >= MAX_RETRIES else None,
        }

    # --- Phase 2: Sanitize SQL ---
    try:
        clean_sql = validate_sql(raw_sql)
        logger.info(f"[SQLAgent] Sanitized SQL: {clean_sql}")
    except ValueError as e:
        logger.warning(f"[SQLAgent] Sanitization rejected: {e}")
        new_count = retry_count + 1
        return {
            "generated_sql": raw_sql,
            "sql_error": f"SQL rejected by sanitizer: {str(e)}",
            "sql_retry_count": new_count,
            "current_agent": "sql_agent",
            "error": f"SQL failed after {MAX_RETRIES} retries" if new_count >= MAX_RETRIES else None,
        }

    # --- Phase 3: Execute against SQLite ---
    try:
        result = _execute_sql(clean_sql)
        logger.info(f"[SQLAgent] Query returned {len(result['rows'])} rows, {len(result['columns'])} columns")

        return {
            "generated_sql": clean_sql,
            "sql_result_columns": result["columns"],
            "sql_result_rows": result["rows"],
            "sql_error": None,
            "sql_retry_count": retry_count,
            "current_agent": "sql_agent",
            "error": None,
        }

    except Exception as e:
        logger.warning(f"[SQLAgent] Execution failed: {e}")
        new_count = retry_count + 1
        return {
            "generated_sql": clean_sql,
            "sql_error": f"SQLite execution error: {str(e)}",
            "sql_retry_count": new_count,
            "current_agent": "sql_agent",
            "error": f"SQL failed after {MAX_RETRIES} retries: {str(e)}" if new_count >= MAX_RETRIES else None,
        }


def should_retry_sql(state: GraphState) -> str:
    """
    Conditional edge function for the LangGraph.
    Determines if the SQL Agent should retry or continue.
    Used in Step 7 when compiling the graph.
    """
    if state.get("sql_error") and state.get("sql_retry_count", 0) < MAX_RETRIES:
        return "sql_agent"  # Loop back for self-correction
    return "continue"       # Move to next node (analyst or END)
