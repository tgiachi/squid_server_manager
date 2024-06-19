import asyncio

from server.routers import ws
from server.routers import manager
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

app.include_router(ws.router)
app.include_router(manager.router)


@app.on_event("startup")
async def startup_event():
    await asyncio.create_task(ws.ping_agents())
