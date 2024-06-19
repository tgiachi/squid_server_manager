import os

import yaml
from python_event_bus import EventBus

import logger_utils
from agent_args import AgentArgs
import events_types


class AgentConfig:
    def __init__(self):
        self.steam_user_name = None
        self.steam_password = None
        self.websocket_url = None
        self.node_id = None


class ConfigManager:
    def __init__(self, a_args: AgentArgs):
        self.logger = logger_utils.init_logger(__name__)
        self.a_args = a_args
        self.config = None
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.a_args.config_file):
            self.logger.warn("Config file does not exist, creating default config")
            self.create_default()
        with open(self.a_args.config_file, 'r') as file:
            config_dict = yaml.safe_load(file)
            self.config = AgentConfig()
            self.config.__dict__.update(config_dict)
        self.logger.info("Config file loaded")
        EventBus.call(events_types.CONFIG_LOADED_EVENT, self.config)

    def save_config(self, config: AgentConfig):
        with open(self.a_args.config_file, 'w') as file:
            yaml.dump(config.__dict__, file)
        EventBus.call(events_types.CONFIG_SAVED_EVENT, config)
        self.logger.info("Config file saved")

    def create_default(self):
        config = AgentConfig()
        config.node_id = self.a_args.node_id
        config.websocket_url = self.a_args.websocket_url

        with open(self.a_args.config_file, 'w') as file:
            yaml.dump(config.__dict__, file)
        self.logger.info("Default config file created")
        EventBus.call(events_types.CONFIG_CREATED_EVENT, config)
        return config

    @EventBus.on(events_types.CONFIG_UPDATED_EVENT)
    def on_config_update(self, config: AgentConfig):
        if config is None:
            self.logger.error("Config is None")
            return
        self.save_config(config)
        self.logger.info("Config saved")
