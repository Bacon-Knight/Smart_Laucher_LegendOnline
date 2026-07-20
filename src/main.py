import sys
import os
import ctypes
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

from src.core.logger import get_logger, setup_global_exception_handler
from src.core.config import resource_path
from src.ui.launcher_hub import LauncherHub

def main():
    setup_global_exception_handler()
    logger = get_logger("Main")
    logger.info("Iniciando o Launcher Legend Online...")
    
    if sys.platform == 'win32':
        plugin_path = resource_path("pepflashplayer.dll")
    else:
        system_plugin = "/usr/lib/pepperflashplugin-nonfree/libpepflashplayer.so"
        if os.path.exists(system_plugin):
            plugin_path = system_plugin
        else:
            plugin_path = resource_path("libpepflashplayer.so")

    sys.argv.append(f"--ppapi-flash-path={plugin_path}")
    sys.argv.append("--ppapi-flash-version=32.0.0.371") 
    sys.argv.append("--ignore-gpu-blocklist")
    sys.argv.append("--enable-gpu-rasterization")
    sys.argv.append("--enable-zero-copy")
    sys.argv.append("--disable-site-isolation-trials")
    sys.argv.append("--renderer-process-limit=4")
    sys.argv.append("--js-flags=--max-old-space-size=2048")
    sys.argv.append("--disable-logging")
    sys.argv.append("--disable-gpu-memory-buffer-video-frames")
    sys.argv.extend([
        "--enable-gpu-compositing",
        "--enable-begin-frame-scheduling",
        "--disable-smooth-scrolling",
        "--disable-background-networking",
        "--disable-component-update",
        "--disable-domain-reliability",
        "--disable-sync",
        "--disable-client-side-phishing-detection",
        "--disable-hang-monitor"
    ])

    # No Linux, o sandbox do Chromium bloqueia o carregamento do plugin Flash
    # via EPERM. Desabilitar o sandbox permite que o plugin seja carregado.
    if sys.platform != 'win32':
        pass
        # sys.argv.append("--no-sandbox")
        # sys.argv.append("--disable-setuid-sandbox")

    if sys.platform == 'win32':
        try:
            myappid = 'baconknight.legendonline.launcher.v2'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass

    app = QApplication(sys.argv)
    
    icon_path = resource_path("bacon_knight.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        
    QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)

    window = LauncherHub()
    window.show()
    
    logger.info("Launcher carregado com sucesso.")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
