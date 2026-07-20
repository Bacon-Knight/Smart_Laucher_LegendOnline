import sys
import os
import ctypes
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from src.core.logger import get_logger, setup_global_exception_handler
from src.core.config import resource_path
from src.core.webengine import setup_webengine_environment
from src.ui.launcher_hub import LauncherHub

def main() -> None:
    setup_global_exception_handler()
    logger = get_logger("Main")
    logger.info("Iniciando o Launcher Legend Online...")
    
    # Configura argumentos do Chromium e ativa os plugins Qt WebEngine
    setup_webengine_environment()

    if sys.platform == 'win32':
        try:
            myappid = 'baconknight.legendonline.launcher.v2'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            logger.warning(f"Não foi possível definir AppUserModelID: {e}")

    app = QApplication(sys.argv)
    
    icon_path = resource_path("bacon_knight.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = LauncherHub()
    window.show()
    
    logger.info("Launcher carregado com sucesso.")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

