import sys
import os

# Garante que o diretório raiz do projeto esteja no sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import ctypes
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
import PyQt5.QtWebEngineWidgets  # Import precoce obrigatório para o WebEngine
from PyQt5.QtGui import QIcon

from src.core.logger import get_logger, setup_global_exception_handler
from src.core.config import resource_path
from src.core.webengine import setup_webengine_environment, enable_webengine_plugins
from src.core.flash_permissions import ensure_flash_permissions
from src.core.cache_proxy import CacheProxyServer
from src.controllers.hub_controller import HubController
from src.ui.views.hub_view import HubView

def main() -> None:
    setup_global_exception_handler()
    logger = get_logger("Main")
    logger.info("Iniciando o BK Launcher LO (v2.4.3)...")
    
    # Injeta permissões automáticas do Flash Player (%AppData%\Macromedia\Flash Player)
    ensure_flash_permissions()

    # Inicia o servidor de Proxy Cache HTTP Local em background
    proxy_port = CacheProxyServer.get_instance().start()
    if proxy_port:
        logger.info(f"⚡ Proxy Cache HTTP Local ativo na porta {proxy_port}")

    # Habilita o compartilhamento de contexto OpenGL para o WebEngine
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    # Configura argumentos do Chromium antes de instanciar o QApplication
    setup_webengine_environment()

    if sys.platform == 'win32':
        try:
            myappid = 'baconknight.bklauncherlo.v242'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            logger.warning(f"Não foi possível definir AppUserModelID: {e}")

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(CacheProxyServer.get_instance().stop)
    
    # Habilita os plugins Qt WebEngine APÓS instanciar o QApplication
    enable_webengine_plugins()
    
    icon_path = resource_path("bacon_knight.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    controller = HubController()
    window = HubView(controller)
    window.show()
    
    logger.info("BK Launcher LO v2.4.3 carregado com sucesso.")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

