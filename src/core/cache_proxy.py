import os
import sys
import shutil
import urllib.request
import urllib.error
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from src.core.logger import get_logger
from src.core.config import get_app_data_dir

logger = get_logger("CacheProxy")

DEFAULT_PROXY_PORT = 8124
PROXY_CACHE_DIR = os.path.join(get_app_data_dir(), "proxy_cache")

# Extensões de arquivos estáticos que devem ser salvas em cache local
CACHEABLE_EXTENSIONS = {
    ".swf", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp",
    ".css", ".js", ".ttf", ".woff", ".woff2", ".mp3", ".wav", ".ogg"
}

# Trava para evitar conflito de gravação simultânea do mesmo arquivo por threads diferentes
CACHE_WRITE_LOCK = threading.Lock()

class AssetCacheHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Handler HTTP local que intercepta requisições de assets (.swf, imagens, js)
    e serve direto do cache em disco quando disponível.
    """

    def log_message(self, format, *args):
        # Desativa logs verbosos no console para performance
        pass

    def get_cache_filepath(self, url: str) -> str:
        """Mapeia a URL para um caminho único dentro da pasta de cache local."""
        parsed = urlparse(url)
        clean_path = parsed.netloc + parsed.path
        safe_path = "".join(c if c.isalnum() or c in ('/', '.', '_', '-') else '_' for c in clean_path)
        safe_path = safe_path.lstrip('/')
        return os.path.join(PROXY_CACHE_DIR, safe_path)

    def is_cacheable(self, url: str) -> bool:
        """Verifica se a URL é de um asset estático elegível para cache."""
        parsed = urlparse(url)
        ext = os.path.splitext(parsed.path)[1].lower()
        return ext in CACHEABLE_EXTENSIONS or ".swf" in parsed.path.lower()

    def do_GET(self):
        url = self.path
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"http://{self.headers.get('Host', '')}{self.path}"

        if not self.is_cacheable(url):
            self.proxy_pass(url)
            return

        cache_path = self.get_cache_filepath(url)

        # Se já existe no cache local, serve diretamente do disco (Leitura concorrente segura e sem trava)
        if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
            try:
                with open(cache_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", self.guess_content_type(cache_path))
                self.send_header("Content-Length", str(len(content)))
                self.send_header("X-BKLauncher-Cache", "HIT")
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                logger.debug(f"Erro ao ler arquivo de cache local ({cache_path}): {e}")

        # Se não está no cache, baixa do servidor original e armazena de forma atômica (Thread-Safe)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": self.headers.get("User-Agent", "Mozilla/5.0")})
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read()
                status_code = resp.status
                content_type = resp.headers.get("Content-Type", "application/octet-stream")

            if status_code == 200 and len(content) > 0:
                os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                tmp_path = f"{cache_path}.tmp_{threading.get_ident()}"
                try:
                    with open(tmp_path, "wb") as f:
                        f.write(content)
                    with CACHE_WRITE_LOCK:
                        os.replace(tmp_path, cache_path)
                except Exception as write_err:
                    logger.debug(f"Falha na gravação atômica do cache: {write_err}")
                    if os.path.exists(tmp_path):
                        try:
                            os.remove(tmp_path)
                        except Exception:
                            pass

            self.send_response(status_code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("X-BKLauncher-Cache", "MISS")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.proxy_pass(url)

    def proxy_pass(self, url: str):
        """Encaminhamento direto para requisições não cacheadas."""
        try:
            req = urllib.request.Request(url, headers={"User-Agent": self.headers.get("User-Agent", "Mozilla/5.0")})
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read()
                self.send_response(resp.status)
                self.send_header("Content-Type", resp.headers.get("Content-Type", "text/html"))
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
        except urllib.error.HTTPError as e:
            self.send_error(e.code, e.reason)
        except Exception as e:
            self.send_error(502, f"Bad Gateway: {e}")

    def guess_content_type(self, filepath: str) -> str:
        ext = os.path.splitext(filepath)[1].lower()
        types = {
            ".swf": "application/x-shockwave-flash",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".css": "text/css",
            ".js": "application/javascript",
            ".html": "text/html"
        }
        return types.get(ext, "application/octet-stream")

class CacheProxyServer:
    _instance = None

    def __init__(self, host="127.0.0.1", port=DEFAULT_PROXY_PORT):
        self.host = host
        self.port = port
        self.httpd = None
        self.thread = None
        self.is_running = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = CacheProxyServer()
        return cls._instance

    def start(self) -> int:
        if self.is_running:
            return self.port

        for p in range(self.port, self.port + 10):
            try:
                self.httpd = HTTPServer((self.host, p), AssetCacheHTTPRequestHandler)
                self.port = p
                break
            except OSError:
                continue

        if not self.httpd:
            logger.error("Não foi possível iniciar o Cache Proxy local em nenhuma porta.")
            return 0

        self.is_running = True
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        logger.info(f"Proxy Cache HTTP do BK Launcher iniciado com sucesso em http://{self.host}:{self.port}")
        return self.port

    def stop(self):
        if self.httpd and self.is_running:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.is_running = False
            logger.info("Proxy Cache HTTP encerrado.")

def clear_proxy_cache() -> bool:
    """Limpa toda a pasta de cache de assets do proxy."""
    try:
        if os.path.exists(PROXY_CACHE_DIR):
            shutil.rmtree(PROXY_CACHE_DIR)
            os.makedirs(PROXY_CACHE_DIR, exist_ok=True)
            logger.info("Cache local do proxy limpo com sucesso.")
            return True
    except Exception as e:
        logger.error(f"Erro ao limpar cache do proxy: {e}")
    return False
