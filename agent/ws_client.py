"""Websocket client for connecting to the websocket server"""
import asyncio
import json
import queue

import websockets
from python_event_bus import EventBus

import logger_utils
from commons.base_listener import BaseMessageListener
from context import AgentContext
import events_types
from commons import base_message
from commons import messages


class WebSocketClient:
    def __init__(self, agent_ctx: AgentContext):
        self.agent_ctx = agent_ctx
        self.listener_map = {}  # message_type: listener
        self.is_connected = False
        self.max_reconnect_attempts = 5
        self.reconnect_attempts = 0
        self.logger = logger_utils.init_logger(__name__)
        self.websocket_url = agent_ctx.config_manager.config.websocket_url + f"/ws/agent/{agent_ctx.config_manager.config.node_id}"
        self.ws = None
        self.killed = False
        self.logger.info(f"Websocket URL: {self.websocket_url}")
        self.outgoing_queue = queue.Queue()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def start(self):
        self.loop.create_task(self.listen())
        self.on_outgoing_message(messages.NodeInfoRequest())
        self.loop.run_forever()

    def kill(self):
        """ Cancel tasks and stop loop from sync, threadsafe """
        self.killed = True
        asyncio.run_coroutine_threadsafe(self.stop_loop(), self.loop)

    def __exit__(self, *_):
        """ Context manager for cleaning up event loop and thread """
        if not self.killed:
            self.kill()

    async def stop_loop(self):
        tasks = [
            task
            for task in asyncio.all_tasks()
            if task is not asyncio.current_task()
        ]
        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)
        self.loop.stop()

    async def listen_queue(self, socket):
        while self.is_connected:
            if not self.outgoing_queue.empty():
                message = self.outgoing_queue.get()
                if isinstance(message, base_message.BaseMessage):
                    self.logger.info(f">> Sending message type: {message.message_type}")
                    await socket.send(message.to_json())
            else:
                await asyncio.sleep(1)

    async def listen_socket(self, socket):
        async for message in socket:
            asyncio.create_task(self.parse_message(message))

    async def parse_message(self, message: str):
        self.logger.info(f"<< Received message: {message}")
        if message is None:
            return
        # check if message is a valid json
        try:
            json_message = json.loads(message)
            message_type = json_message.get("message_type")

            if message_type is None:
                self.logger.error("Message type is None")
                return

            listener = self.listener_map.get(message_type)

            if listener is None:
                self.logger.error(f"No listener for message type {message_type}")
                return

            if isinstance(listener, BaseMessageListener):
                await listener.on_message(listener.deserialize(message))

        except Exception as e:
            self.logger.error(f"Error parsing message: {e}")
            return

    async def listen(self):
        while True:
            try:
                self.logger.info("Connecting to websocket")
                async with websockets.connect(self.websocket_url) as ws:
                    self.logger.info("Connected to websocket")
                    self.ws = ws
                    self.is_connected = True
                    self.reconnect_attempts = 0
                    self.loop = asyncio.get_event_loop()
                    task1 = self.listen_socket(ws)
                    task2 = self.listen_queue(ws)
                    await asyncio.gather(task1, task2)

            except Exception as e:
                self.logger.error(f"Error connecting to websocket: {e}")
                self.reconnect_attempts += 1
                if self.reconnect_attempts >= self.max_reconnect_attempts:
                    self.logger.error("Max reconnect attempts reached")
                    break
                await asyncio.sleep(self.reconnect_attempts * 5)

    def add_listener(self, message_type, listener: BaseMessageListener):
        self.logger.info(f"Adding listener for message type {message_type}")
        self.listener_map[message_type] = listener

    @EventBus.on(events_types.WS_SEND_MESSAGE_EVENT)
    def on_outgoing_message(self, message: base_message.BaseMessage):
        if message is None:
            return
        if isinstance(message, base_message.BaseMessage):
            self.outgoing_queue.put(message)
