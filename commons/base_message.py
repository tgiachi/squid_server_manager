from dataclasses import dataclass
import json


@dataclass
class BaseMessage:
    message_type: str

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_string):
        return cls(**json.loads(json_string))
