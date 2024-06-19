#!/usr/bin/env python3

import argparse
import uuid

from config_manager import ConfigManager
from steam_cmd_manager import SteamCmdManager
from agent_args import AgentArgs
from context import AgentContext
from ws_client import WebSocketClient


def main(a_args: AgentArgs):
    """ Main entry point for the agent """
    context = AgentContext()
    context.a_args = a_args
    context.config_manager = ConfigManager(a_args)
    context.steam_cmd_manager = SteamCmdManager(context)
    context.ws_client = WebSocketClient(context)

    context.ws_client.start()


if __name__ == '__main__':
    """ On start, parse the arguments and call the main function"""
    parser = argparse.ArgumentParser(description='Agent for the project')
    parser.add_argument('--config', type=str, help='Path to the config file', default="config.yaml")
    parser.add_argument('--log', type=str, help='Path to the log file', default="logs")
    parser.add_argument('--log-level', type=str, help='Log level', default="INFO")
    parser.add_argument('--node-id', type=str, help='Node ID', default=str(uuid.uuid4()))
    parser.add_argument('--websocket-url', type=str, help='Websocket URL', default="ws://localhost:8000")
    parser.add_argument("--steam-cmd-path", type=str, help="Path to the steamcmd executable", default="steamcmd")
    args = parser.parse_args()
    agent_args = AgentArgs(args.config, args.log, args.log_level, args.node_id, args.websocket_url, args.steam_cmd_path)
    main(agent_args)
