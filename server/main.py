from server.routers import ws
from fastapi import FastAPI

app = FastAPI()

app.include_router(ws.router)

