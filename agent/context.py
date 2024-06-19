import dataclasses


@dataclasses.dataclass
class AgentContext:
    a_args = None
    config_manager = None
    steam_cmd_manager = None
    ws_client = None
