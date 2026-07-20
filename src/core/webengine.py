import os
import sys
from typing import List
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from src.core.config import resource_path
from src.core.logger import get_logger

logger = get_logger("WebEngine")

def get_chromium_flags() -> List[str]:
    """Retorna a lista de argumentos de linha de comando otimizados para o Chromium / Flash WebEngine."""
    if sys.platform == 'win32':
        plugin_path = resource_path("pepflashplayer.dll")
    else:
        system_plugin = "/usr/lib/pepperflashplugin-nonfree/libpepflashplayer.so"
        if os.path.exists(system_plugin):
            plugin_path = system_plugin
        else:
            plugin_path = resource_path("libpepflashplayer.so")

    flags = [
        f"--ppapi-flash-path={plugin_path}",
        "--ppapi-flash-version=32.0.0.371",
        "--ignore-gpu-blocklist",
        "--enable-gpu-rasterization",
        "--enable-zero-copy",
        "--disable-site-isolation-trials",
        "--renderer-process-limit=4",
        "--js-flags=--max-old-space-size=2048",
        "--disable-logging",
        "--disable-gpu-memory-buffer-video-frames",
        "--enable-gpu-compositing",
        "--enable-begin-frame-scheduling",
        "--disable-smooth-scrolling",
        "--disable-background-networking",
        "--disable-component-update",
        "--disable-domain-reliability",
        "--disable-sync",
        "--disable-client-side-phishing-detection",
        "--disable-hang-monitor"
    ]
    return flags

def setup_webengine_environment() -> None:
    """Aplica os argumentos do Chromium em sys.argv e habilita plugins no QWebEngineSettings."""
    flags = get_chromium_flags()
    for flag in flags:
        if flag not in sys.argv:
            sys.argv.append(flag)
            
    QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
    logger.info("Ambiente Qt WebEngine e plugin Flash configurados com sucesso.")
