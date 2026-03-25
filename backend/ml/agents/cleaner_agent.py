"""
Cleaner Agent Node: Placeholder for data cleaning operations.

To be fully implemented in a future step. Included now so the
LangGraph can compile cleanly.
"""

from loguru import logger
from backend.ml.agents.state import GraphState


def cleaner_agent_node(state: GraphState) -> dict:
    """
    LangGraph node: Placeholder for data cleaning.
    """
    logger.info("[Cleaner] Placeholder agent hit. No cleaning performed.")

    return {
        "current_agent": "cleaner_agent",
        "cleaning_log": {"status": "Cleaner agent not yet fully implemented"},
        "narrative": "The data cleaner agent is a placeholder and hasn't made any changes yet.",
    }
