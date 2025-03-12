from fastapi import WebSocket
from typing import Dict, List, Optional
import asyncio


class ConnectionManager:
    def __init__(self):
        # Store active connections by user_id
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # Store user agents by connection
        self.user_agents = {}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept and store a new connection"""
        await websocket.accept()
        async with self.lock:
            if user_id not in self.active_connections:
                self.active_connections[user_id] = []
            self.active_connections[user_id].append(websocket)
        return len(self.active_connections[user_id])

    async def disconnect(self, websocket: WebSocket, user_id: str):
        """Remove a connection"""
        async with self.lock:
            if user_id in self.active_connections:
                if websocket in self.active_connections[user_id]:
                    self.active_connections[user_id].remove(websocket)

                # Clean up empty user entries
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]

            # Remove any associated agent
            if websocket in self.user_agents:
                del self.user_agents[websocket]

    async def send_message(
        self, user_id: str, message: dict, exclude: Optional[WebSocket] = None
    ):
        """Send a message to all connections for a specific user"""
        if user_id not in self.active_connections:
            return

        for connection in self.active_connections[user_id]:
            if connection != exclude:
                await connection.send_json(message)

    def get_connection_count(self, user_id: str = None):
        """Get total connection count or for a specific user"""
        if user_id:
            return len(self.active_connections.get(user_id, []))

        # Count all connections
        count = 0
        for user_conns in self.active_connections.values():
            count += len(user_conns)
        return count

    def store_agent(self, websocket: WebSocket, agent):
        """Store an agent instance for a specific connection"""
        self.user_agents[websocket] = agent

    def get_agent(self, websocket: WebSocket):
        """Get the agent for a specific connection"""
        return self.user_agents.get(websocket)
