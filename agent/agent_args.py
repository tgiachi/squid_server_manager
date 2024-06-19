class AgentArgs:
    def __init__(self, config_file: str, log_directory: str, log_level: str, node_id: str, websocket_url: str,
                 steam_cmd_path: str):
        self.config_file = config_file
        self.log_directory = log_directory
        self.log_level = log_level
        self.node_id = node_id
        self.websocket_url = websocket_url
        self.steam_cmd_path = steam_cmd_path
