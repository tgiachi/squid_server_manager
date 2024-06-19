from dataclasses import dataclass

from commons.base_message import BaseMessage
import commons.message_types


@dataclass
class NodeInfoRequest(BaseMessage):
    def __init__(self):
        super().__init__(commons.message_types.NODE_INFO_REQUEST)


@dataclass
class NodeInfoResponse(BaseMessage):
    def __init__(self):
        super().__init__(commons.message_types.NODE_INFO_RESPONSE)
        self.node_id = None
        self.processor = None
