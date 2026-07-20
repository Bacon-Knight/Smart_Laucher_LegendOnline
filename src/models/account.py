from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class Account:
    """Modelo de dados tipado representando uma conta do usuário no Launcher."""
    email: str
    password: str
    server_num: str = "1"
    nickname: str = ""
    color: str = "#0a2b10"  # Padrão Verde
    last_login: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a conta para dicionário para persistência em JSON no QSettings."""
        return {
            "email": self.email,
            "password": self.password,
            "server_num": self.server_num,
            "nickname": self.nickname,
            "color": self.color,
            "last_login": self.last_login
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Account":
        """Cria uma instância de Account a partir de um dicionário."""
        return cls(
            email=data.get("email", ""),
            password=data.get("password", ""),
            server_num=str(data.get("server_num", "1")),
            nickname=data.get("nickname", ""),
            color=data.get("color", "#0a2b10"),
            last_login=data.get("last_login")
        )
