"""
Router Node: Ultra-fast intent classifier for the SAGA LangGraph.

Reads the user's question and classifies it into one of three routes:
- sql_agent: Data queries, filtering, aggregation
- analyst_agent: Charts, correlations, statistical analysis
- cleaner_agent: Data cleaning, fixing nulls, removing outliers
"""

from loguru import logger
from backend.ml.agents.state import GraphState
from backend.ml.agents.llm_gateway import LLMGateway

# Valid routes the router can output
VALID_ROUTES = {"sql_agent", "analyst_agent", "cleaner_agent"}
DEFAULT_ROUTE = "sql_agent"

CLASSIFICATION_PROMPT = """You are an intent classifier for a data analytics platform.
Given a user's question about a dataset, classify it into EXACTLY one category.

Categories:
- "sql_agent": The user wants to query, filter, count, aggregate, sort, or retrieve specific data rows.
- "analyst_agent": The user wants charts, plots, correlations, trends, distributions, or statistical analysis.
- "cleaner_agent": The user wants to clean data, fix missing values, remove outliers, handle duplicates, or transform columns.

Rules:
- Output ONLY the category name as a single word, nothing else.
- No quotes, no punctuation, no explanation.
- If unsure, output "sql_agent".

User question: {question}
Category:"""


def router_node(state: GraphState) -> dict:
    """
    LangGraph node: Classifies user intent and sets the route.

    Reads: state["messages"] (last user message)
    Writes: state["route"], state["current_agent"]
    """
    # Extract the latest user message
    last_message = state["messages"][-1].content
    logger.info(f"[Router] Classifying: '{last_message}'")

    try:
        llm = LLMGateway.get_fast_llm()
        prompt = CLASSIFICATION_PROMPT.format(question=last_message)
        response = llm.invoke(prompt)

        # Parse the raw response
        raw_route = response.content.strip().lower().replace('"', '').replace("'", "")
        logger.info(f"[Router] Raw classification: '{raw_route}'")

        # Validate — only accept known routes
        if raw_route in VALID_ROUTES:
            route = raw_route
        else:
            logger.warning(f"[Router] Unknown route '{raw_route}', defaulting to '{DEFAULT_ROUTE}'")
            route = DEFAULT_ROUTE

    except Exception as e:
        logger.error(f"[Router] Classification failed: {e}. Defaulting to '{DEFAULT_ROUTE}'")
        route = DEFAULT_ROUTE

    logger.info(f"[Router] Routed to: {route}")
    return {"route": route, "current_agent": "router"}
