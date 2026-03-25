"""
WebSocket Chat Endpoint for SAGA.

Handles persistent WebSocket connections for real-time AI chat streaming.
Currently serves dummy events; Step 7 will wire this to the LangGraph swarm.
"""

import asyncio
from typing import List, Any
from fastapi import WebSocket, WebSocketDisconnect, FastAPI
from loguru import logger

from backend.database.utils import get_dataset_metadata, get_table_schema


class ConnectionManager:
    """Manages active WebSocket connections for concurrent clients."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"[WS] Client connected. Total active: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Unregister a disconnected WebSocket."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"[WS] Client disconnected. Total active: {len(self.active_connections)}")

    async def send_event(self, websocket: WebSocket, event_type: str, agent: str, content: Any):
        """Send a single streaming event to the client."""
        await websocket.send_json({
            "type": event_type,
            "agent": agent,
            "content": content,
        })


# Singleton manager instance
manager = ConnectionManager()


async def handle_chat_message(websocket: WebSocket, data: dict):
    """
    Process one incoming chat message from the WebSocket.

    Validates input, loads dataset context, and streams back events.
    Currently sends dummy events. Step 7 will replace the body with
    real LangGraph invocation via `build_saga_graph().astream_events()`.
    """

    # --- 1. Validate required fields ---
    action = data.get("action")
    dataset_id = data.get("dataset_id")
    message = data.get("message")

    if action != "query":
        await manager.send_event(websocket, "error", "System", f"Unknown action: '{action}'. Expected 'query'.")
        return

    if not dataset_id:
        await manager.send_event(websocket, "error", "System", "Missing required field: dataset_id")
        return

    if not message or not message.strip():
        await manager.send_event(websocket, "error", "System", "Missing required field: message")
        return

    logger.info(f"[WS] Query received — dataset: {dataset_id}, message: '{message}'")

    # --- 2. Load dataset metadata ---
    metadata = get_dataset_metadata(dataset_id)
    if not metadata:
        await manager.send_event(websocket, "error", "System", f"Dataset '{dataset_id}' not found.")
        return

    table_name = metadata["table_name"]

    # --- 3. Load schema context (same format FileIngestionManager generates) ---
    try:
        schema_context = get_table_schema(table_name)
    except Exception as e:
        await manager.send_event(websocket, "error", "System", f"Failed to load schema: {str(e)}")
        return

    # --- 4. Stream REAL LangGraph events ---
    from backend.ml.agents.graph import build_saga_graph
    from backend.ml.agents.state import create_initial_state
    
    # In a production app you'd instantiate this globally, but here we do it per-request for simplicity
    saga_graph = build_saga_graph()

    initial_state = create_initial_state(
        dataset_id=dataset_id,
        table_name=table_name,
        schema_context=schema_context,
        user_message=message
    )

    try:
        current_agent = "router"

        # V2 streams much richer events
        async for event in saga_graph.astream_events(initial_state, version="v2"):
            kind = event["event"]

            # Sub-graph / Node started
            if kind == "on_chain_start":
                name = event.get("name")
                if name in ["router", "sql_agent", "analyst_agent", "cleaner_agent"]:
                    current_agent = name
                    await manager.send_event(websocket, "status", current_agent, "Thinking...")

            # Node finished - Check for outputs
            elif kind == "on_chain_end":
                data = event.get("data", {}).get("output", {})
                if isinstance(data, dict):
                    # Check what the agent produced and stream it
                    
                    if "generated_sql" in data and data["generated_sql"]:
                        await manager.send_event(
                            websocket, "thought", current_agent, 
                            f"Generated SQL:\n{data['generated_sql']}"
                        )
                    
                    if "chart_json" in data and data["chart_json"]:
                        await manager.send_event(
                            websocket, "chart", current_agent, data["chart_json"]
                        )
                    
                    if "narrative" in data and data["narrative"]:
                        await manager.send_event(
                            websocket, "token", current_agent, data["narrative"]
                        )
                        
                    if "error" in data and data["error"]:
                        await manager.send_event(
                            websocket, "error", current_agent, data["error"]
                        )

        await manager.send_event(websocket, "final_answer", "System", "Analysis complete.")

    except Exception as e:
        logger.error(f"[WS] Graph execution failed: {e}")
        await manager.send_event(websocket, "error", "System", f"Graph execution failed: {e}")


def create_websocket_route(app: FastAPI):
    """
    Registers the WebSocket endpoint on the FastAPI app.
    Called from main.py during app creation.
    """

    @app.websocket("/v1/api/ws/chat")
    async def websocket_chat(websocket: WebSocket):
        await manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_json()
                await handle_chat_message(websocket, data)
        except WebSocketDisconnect:
            manager.disconnect(websocket)
        except Exception as e:
            logger.error(f"[WS] Unexpected error: {e}")
            manager.disconnect(websocket)
