from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
from .ws_connection_manager import WsConnectionManager

router = APIRouter(prefix="/ws")

connection_manager = WsConnectionManager()

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


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
