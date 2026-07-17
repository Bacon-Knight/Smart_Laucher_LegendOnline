import sys
import os
import ctypes
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

from src.core.logger import get_logger
from src.core.config import resource_path
from src.ui.launcher_hub import LauncherHub

def main():
    logger = get_logger("Main")
    logger.info("Iniciando o Launcher Legend Online...")
    
    if sys.platform == 'win32':
        plugin_path = resource_path("pepflashplayer.dll")
    else:
        plugin_path = resource_path("libpepflashplayer.so")

    sys.argv.append(f"--ppapi-flash-path={plugin_path}")
    sys.argv.append("--ppapi-flash-version=32.0.0.371") 
    sys.argv.append("--ignore-gpu-blocklist")
    sys.argv.append("--enable-gpu-rasterization")
    sys.argv.append("--enable-zero-copy")
    sys.argv.append("--disable-site-isolation-trials")
    sys.argv.append("--renderer-process-limit=3")
    sys.argv.append("--js-flags=--max-old-space-size=512")
    sys.argv.append("--disable-logging")
    sys.argv.append("--disable-gpu-memory-buffer-video-frames")

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
