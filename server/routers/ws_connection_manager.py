from fastapi import WebSocket


class WsConnectionManager(object):
    def __init__(self):
        self.connections = {}

    def add_connection(self, connection: WebSocket, agent_id: str):
        self.connections[agent_id] = connection

    def remove_connection(self, agent_id: str):
        self.connections.pop(agent_id)

    async def broadcast(self, message):
        for connection in self.connections.values():
            await connection.send_text(message)
