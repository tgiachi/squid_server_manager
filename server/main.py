import asyncio
from contextlib import asynccontextmanager
from server.routers import ws
from server.routers import manager
from fastapi import FastAPI


@asynccontextmanager
def on_startup():
    asyncio.create_task(ws.ping_agents())


app = FastAPI(on_startup=[on_startup])

app.include_router(ws.router)
app.include_router(manager.router)
