import asyncio
import json
import logging

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages active WebSocket connections and broadcasts messages."""

    def __init__(self):
        # Dictionary mapping connection_id to WebSocket instance
        self.active_connections: dict[str, WebSocket] = {}
        self._lock = asyncio.Lock()

    async def connect(self, connection_id: str, websocket: WebSocket):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        async with self._lock:
            self.active_connections[connection_id] = websocket
        logger.info(
            f"WebSocket connected: {connection_id} (total: {len(self.active_connections)})"
        )

    async def disconnect(self, connection_id: str):
        """Remove a WebSocket connection."""
        async with self._lock:
            if connection_id in self.active_connections:
                del self.active_connections[connection_id]
        logger.info(
            f"WebSocket disconnected: {connection_id} (total: {len(self.active_connections)})"
        )

    async def broadcast_message(self, message: dict):
        """
        Broadcast a message to all active connections.

        Args:
            message: Dictionary containing message data (will be JSON serialized)
        """
        if not self.active_connections:
            logger.debug("No active WebSocket connections to broadcast to")
            return

        message_json = json.dumps(message)
        disconnected = []

        # Send to all connections
        async with self._lock:
            connections = list(self.active_connections.items())

        for connection_id, websocket in connections:
            try:
                await websocket.send_text(message_json)
                logger.debug(f"Broadcasted message to {connection_id}")
            except Exception as e:
                logger.error(f"Error broadcasting to {connection_id}: {e}")
                disconnected.append(connection_id)

        # Clean up disconnected clients
        if disconnected:
            async with self._lock:
                for connection_id in disconnected:
                    if connection_id in self.active_connections:
                        del self.active_connections[connection_id]
            logger.info(f"Removed {len(disconnected)} disconnected clients")

    def get_connection_count(self) -> int:
        """Return the number of active connections."""
        return len(self.active_connections)
