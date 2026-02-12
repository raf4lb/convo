import logging
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time message updates.

    Clients connect here to receive real-time notifications when new messages
    are received via webhook.
    """
    connection_id = str(uuid.uuid4())
    connection_manager = websocket.app.state.connection_manager

    try:
        # Accept and register the connection
        await connection_manager.connect(connection_id, websocket)
        logger.info(f"Client {connection_id} connected to WebSocket")

        # Keep connection alive - listen for messages (though we mainly broadcast)
        while True:
            # Receive any messages from client (for keep-alive or future client->server messages)
            data = await websocket.receive_text()
            logger.debug(f"Received from {connection_id}: {data}")

            # For now, just echo back or ignore
            # In future, could handle client commands here

    except WebSocketDisconnect:
        logger.info(f"Client {connection_id} disconnected normally")
    except Exception as e:
        logger.error(f"WebSocket error for {connection_id}: {e}")
    finally:
        # Clean up connection
        await connection_manager.disconnect(connection_id)
