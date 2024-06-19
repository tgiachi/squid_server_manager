import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
from .ws_connection_manager import WsConnectionManager
from server.models.ws_models import WsConnectionList
from commons.base_message import BaseMessage
from commons.messages import NodeInfoRequest, PingRequest
from python_event_bus import EventBus

router = APIRouter(prefix="/ws")

connection_manager = WsConnectionManager()

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


async def ping_agents():
    while True:
        await send_ws_message(PingRequest())
        await asyncio.sleep(10)


async def send_ws_message(message: BaseMessage, agent_id: str = None):
    print(f"Sending message to agent: {agent_id} type: {message.message_type}")
    if agent_id:
        await connection_manager.connections[agent_id].send_text(message.to_json())
    else:
        await connection_manager.broadcast(message.to_json())


@router.post("/broadcast")
async def broadcast_message(message: str, agent_id: str = None):
    await send_ws_message(NodeInfoRequest(), agent_id)
    return {"message": "Message sent to all agents"}


@router.get("/connections", response_model=WsConnectionList)
async def get_connections():
    return WsConnectionList(connections=list(connection_manager.connections.keys()))


@router.websocket("/agent/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    LOG.info(f"Agent {agent_id} connected")
    connection_manager.add_connection(websocket, agent_id)
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data} from agent_id: {agent_id}")
        except WebSocketDisconnect as e:
            connection_manager.remove_connection(agent_id)
            break
