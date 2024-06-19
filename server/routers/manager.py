from fastapi import APIRouter
from server.routers.ws import send_ws_message
from commons.messages import NodeInfoRequest
router = APIRouter(prefix="/manager")


@router.get("/status")
async def get_status():
    return {"status": "ok"}


@router.get("/send_message")
async def send_message():
    await send_ws_message(NodeInfoRequest())
    return {"message": "Message sent to all agents"}

