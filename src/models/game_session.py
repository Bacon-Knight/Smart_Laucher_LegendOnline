from dataclasses import dataclass
from typing import Optional

@dataclass
class GameSession:
    """Modelo representando uma sessão de jogo ativa."""
    email: str
    password: str
    server_num: str
    url: str
    nickname: str = ""
    color: str = "#120c18"
    enable_cache: bool = True
    auto_relog_enabled: bool = True
