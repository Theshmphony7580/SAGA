"""
Graph Compilation: Wires all SAGA nodes into a unified LangGraph StateMachine.

Topology:
- START -> Router
- Router -> (sql_agent | analyst_agent | cleaner_agent)
- sql_agent -> should_retry_sql (loops back on error, else flows to analyst_agent)
- analyst_agent -> END
- cleaner_agent -> END
"""

from langgraph.graph import StateGraph, END
from backend.ml.agents.state import GraphState
from backend.ml.agents.router import router_node
from backend.ml.agents.sql_agent import sql_agent_node, should_retry_sql
from backend.ml.agents.analyst_agent import analyst_agent_node
from backend.ml.agents.cleaner_agent import cleaner_agent_node


def build_saga_graph():
    """
    Compiles and returns the executable SAGA LangGraph.
    """
    workflow = StateGraph(GraphState)

    # 1. Add all nodes
    workflow.add_node("router", router_node)
    workflow.add_node("sql_agent", sql_agent_node)
    workflow.add_node("analyst_agent", analyst_agent_node)
    workflow.add_node("cleaner_agent", cleaner_agent_node)

    # 2. Set the entry point
    workflow.set_entry_point("router")

    # 3. Add Edges

    # The router decides which highly specialized agent gets the task
    workflow.add_conditional_edges(
        "router",
        lambda state: state["route"],  # Reads the route set by the router node
        {
            "sql_agent": "sql_agent",
            "analyst_agent": "analyst_agent",
            "cleaner_agent": "cleaner_agent",
        }
    )

    # SQL Agent self-correction loop
    workflow.add_conditional_edges(
        "sql_agent",
        should_retry_sql,
        {
            "sql_agent": "sql_agent",         # Loop back for retry
            "continue": "analyst_agent",      # Data flows directly to analyst!
        }
    )

    # Sink nodes go to END
    workflow.add_edge("analyst_agent", END)
    workflow.add_edge("cleaner_agent", END)

    # 4. Compile and return
    return workflow.compile()
