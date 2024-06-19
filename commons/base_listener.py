from json import loads


class BaseMessageListener:
    def __init__(self, message_class):
        self.message_class = message_class

    async def on_message(self, message, *args, **kwargs):
        pass

    def deserialize(self, message):
        return self.message_class(**loads(message))
