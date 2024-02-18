# websocket_manager.py
from fastapi import WebSocket
from typing import List

connections: List[WebSocket] = []

async def broadcast(message: str):
    disconnected_clients = []
    # print(connections)
    for connection in connections:
        try:
            # print(connection)
            await connection.send_text(message)
        except RuntimeError as e:
            # Handle disconnected client
            disconnected_clients.append(connection)
    # Remove disconnected clients
    for client in disconnected_clients:
        connections.remove(client)
