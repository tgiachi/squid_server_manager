from enum import Enum

from pydantic import BaseModel


class WsConnectionList(BaseModel):
    connections: list[str]
