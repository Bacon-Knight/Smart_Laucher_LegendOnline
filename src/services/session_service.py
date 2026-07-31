from typing import Optional, List, Dict
from PyQt5.QtWebEngineWidgets import QWebEngineProfile
from src.core.logger import get_logger

logger = get_logger("SessionService")

UID_COOKIE_CANDIDATES = ["uid", "userid", "user_id", "userId", "playerid", "player_id"]

class SessionCookieExtractor:
    """
    Utilitário para extração do UID e cookies de sessão do QWebEngineProfile.
    """

    @staticmethod
    def try_find_uid_from_cookies(cookies_dict: Dict[str, str]) -> Optional[str]:
        for candidate in UID_COOKIE_CANDIDATES:
            for k, v in cookies_dict.items():
                if k.lower() == candidate.lower() and v:
                    return v
        return None
