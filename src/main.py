import sys
import os

# Garante que o diretório raiz do projeto esteja no sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import ctypes
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from src.core.logger import get_logger, setup_global_exception_handler
from src.core.config import resource_path
from src.core.webengine import setup_webengine_environment, enable_webengine_plugins
from src.ui.launcher_hub import LauncherHub

def main() -> None:
    setup_global_exception_handler()
    logger = get_logger("Main")
    logger.info("Iniciando o Launcher Legend Online...")
    
    # Configura argumentos do Chromium antes de instanciar o QApplication
    setup_webengine_environment()

    if sys.platform == 'win32':
        try:
            myappid = 'baconknight.legendonline.launcher.v2'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            logger.warning(f"Não foi possível definir AppUserModelID: {e}")

    app = QApplication(sys.argv)
    
    # Habilita os plugins Qt WebEngine APÓS instanciar o QApplication
    enable_webengine_plugins()
    
    icon_path = resource_path("bacon_knight.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = LauncherHub()
    window.show()
    
    logger.info("Launcher carregado com sucesso.")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

