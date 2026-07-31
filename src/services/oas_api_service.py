import re
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import List, Dict, Any
from src.core.logger import get_logger

logger = get_logger("OasApiService")

class OasApiService:
    """
    Serviço de comunicação com as APIs da OASGames / Creaction Network
    para obter a lista de servidores públicos e os servidores do jogador autenticado.
    """

    USER_SERVERS_URL_TEMPLATE = "https://odp3.oasgames.com/api/game/get-user-servers?uid={uid}&gamecode=lobr"
    PUBLIC_SERVER_LIST_URL = "https://odp3.oasgames.com/api/game/serverlist?gamecode=lobr"
    JSONP_REGEX = re.compile(r'^\s*[\w\.\$]+\s*\((?P<payload>.*)\)\s*;?\s*$', re.DOTALL)
    
    # RegEx Harvesters extraídos via Engenharia Reversa do Client Brov
    GAME_JSP_REGEX = re.compile(r'frame.*src=["\'](.*game\.jsp[^"\']*)["\']', re.IGNORECASE)
    TOKEN_IFRAME_REGEX = re.compile(r'iframe.*src=["\'](.*login\?token[^"\']*)["\']', re.IGNORECASE)
    OSDK_EXPS_REGEX = re.compile(r'OSDK\.config\.exps[^\"]*"([^\"]+)"', re.IGNORECASE)

    @staticmethod
    def extract_game_url_from_html(html_content: str) -> str:
        """
        Extrai a URL direta do jogo ou iFrame de login a partir do HTML cru de uma resposta da web.
        """
        if not html_content:
            return ""
        
        match_jsp = OasApiService.GAME_JSP_REGEX.search(html_content)
        if match_jsp:
            return match_jsp.group(1).replace("&amp;", "&")
            
        match_token = OasApiService.TOKEN_IFRAME_REGEX.search(html_content)
        if match_token:
            return match_token.group(1).replace("&amp;", "&")
            
        match_exps = OasApiService.OSDK_EXPS_REGEX.search(html_content)
        if match_exps:
            return match_exps.group(1)
            
        return ""

    @staticmethod
    def extract_json_from_jsonp(raw_body: str) -> str:
        """Remove o empacotador JSONP e retorna apenas a string JSON limpa."""
        if not raw_body or not raw_body.strip():
            return "{}"
        text = raw_body.strip()
        if text.startswith("[") or text.startswith("{"):
            return text
        match = OasApiService.JSONP_REGEX.match(text)
        if match:
            return match.group("payload")
        return text

    @classmethod
    def get_user_servers(cls, uid: str, session_cookies: Dict[str, str] = None, timeout: int = 8) -> List[Dict[str, Any]]:
        """
        Consulta os servidores em que o jogador logou usando a API autenticada da OASGames.
        """
        if not uid:
            return []
        
        url = cls.USER_SERVERS_URL_TEMPLATE.format(uid=urllib.parse.quote(uid))
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "Accept": "*/*"
        }

        if session_cookies:
            cookie_header = "; ".join([f"{k}={v}" for k, v in session_cookies.items()])
            headers["Cookie"] = cookie_header

        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status == 200:
                    raw_text = resp.read().decode("utf-8")
                    json_str = cls.extract_json_from_jsonp(raw_text)
                    data = json.loads(json_str)
                    
                    # Suporta diferentes chaves de resposta da API OAS
                    servers = data.get("data") or data.get("list") or data.get("servers") or []
                    if isinstance(servers, dict) and "list" in servers:
                        servers = servers["list"]
                    
                    if isinstance(servers, list):
                        logger.info(f"API OASGames retornou {len(servers)} servidor(es) para o UID {uid}.")
                        return servers
        except Exception as e:
            logger.debug(f"Falha ao obter servidores do usuário na API OASGames ({uid}): {e}")
            
        return []

    @classmethod
    def get_public_server_list(cls, timeout: int = 8) -> List[Dict[str, Any]]:
        """
        Consulta a lista pública oficial de servidores do Legend Online BR.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }
        try:
            req = urllib.request.Request(cls.PUBLIC_SERVER_LIST_URL, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status == 200:
                    raw_text = resp.read().decode("utf-8")
                    json_str = cls.extract_json_from_jsonp(raw_text)
                    data = json.loads(json_str)
                    servers = data.get("data") or data.get("list") or []
                    if isinstance(servers, list):
                        return servers
        except Exception as e:
            logger.debug(f"Falha ao obter lista pública de servidores OASGames: {e}")
            
        return []

