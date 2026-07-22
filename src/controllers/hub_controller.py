import sys
import ctypes
import datetime
from typing import List, Dict, Any
from PyQt5.QtCore import QObject, QTimer, QSettings
from PyQt5.QtWidgets import QApplication

from src.core.logger import get_logger
from src.core.config import GAME_URL_TEMPLATE, COLOR_ORDER, COLOR_MAP
from src.services.account_service import AccountService
from src.models.account import Account
from src.models.game_session import GameSession

logger = get_logger("HubController")

if sys.platform == 'win32':
    from ctypes import wintypes
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.UINT),
            ("dwTime", wintypes.DWORD)
        ]

def get_system_idle_time_ms():
    if sys.platform != 'win32':
        return 0
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        return ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return 0

class AFKManager(QObject):
    """Gerencia a inatividade global do usuário para acionar o Modo Chefe / Oculto."""
    def __init__(self, hub_controller, timeout_mins=2):
        super().__init__()
        self.hub_controller = hub_controller
        self.timeout_ms = timeout_mins * 60 * 1000
        self.inactive_ms = 0
        
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_state)
        self.check_timer.start(5000)

    def check_state(self):
        if not self.hub_controller.settings.value("afk_enabled", True, type=bool):
            self.inactive_ms = 0
            return

        app = QApplication.instance()
        is_app_focused = app.activeWindow() is not None
        sys_idle = get_system_idle_time_ms()
        
        if sys_idle >= self.timeout_ms:
            self.hub_controller.hide_to_tray()
            return
            
        if not is_app_focused:
            self.inactive_ms += 5000
            if self.inactive_ms >= self.timeout_ms:
                self.hub_controller.hide_to_tray()
        else:
            self.inactive_ms = 0

class HubController(QObject):
    """
    Controlador MVC responsável pelo Launcher Hub:
    - Gerencia carregamento, adição e exclusão de contas via AccountService.
    - Controla a execução do AFKManager e Modo Oculto.
    - Lança novas janelas de jogo (instanciando GameSession, GameView e GameController).
    """

    def __init__(self, view=None):
        super().__init__()
        self.view = view
        self.settings = QSettings("CustomLauncher", "LegendOnline")
        self.account_service = AccountService()
        self.game_windows = []
        self.boss_hidden = False

        self.afk_manager = AFKManager(self, timeout_mins=2)

    def get_saved_accounts(self) -> Dict[str, Any]:
        """Retorna o dicionário de contas salvas."""
        try:
            accs_json = self.settings.value("saved_accounts", "{}")
            import json
            raw_dict = json.loads(accs_json)
            for k, v in raw_dict.items():
                if isinstance(v, str):
                    raw_dict[k] = {"password": v, "server": "1252", "nick": ""}
            return raw_dict
        except Exception as e:
            logger.error(f"Erro ao carregar contas: {e}")
            return {}

    def save_account(self, email: str, password: str, server_num: str, nick: str):
        """Salva ou atualiza os dados de uma conta no QSettings."""
        import json
        saved = self.get_saved_accounts()
        saved[email] = {
            "password": password,
            "server": server_num,
            "nick": nick,
            "last_login": datetime.datetime.now().strftime("%d/%m %H:%M"),
        }
        self.settings.setValue("saved_accounts", json.dumps(saved))
        self.settings.setValue("last_email", email)
        self.settings.setValue("server", server_num)
        return saved

    def delete_account(self, email: str):
        """Remove uma conta salva pelo e-mail."""
        import json
        saved = self.get_saved_accounts()
        if email in saved:
            del saved[email]
            self.settings.setValue("saved_accounts", json.dumps(saved))
        return saved

    def launch_game(self, email: str, password: str, server_num: str, nick: str):
        """Instancia a sessão de jogo e abre a nova janela."""
        if not email or not server_num:
            return None

        self.save_account(email, password, server_num, nick)

        url_completa = GAME_URL_TEMPLATE.format(server_num=server_num)
        color_name = COLOR_ORDER[len(self.game_windows) % len(COLOR_ORDER)]
        bg_color = COLOR_MAP.get(color_name, "#120c18")

        session = GameSession(
            email=email,
            password=password,
            server_num=server_num,
            url=url_completa,
            nickname=nick,
            color=bg_color,
            enable_cache=True,
            auto_relog_enabled=True
        )

        from src.ui.views.game_view import GameView
        gw = GameView(session)
        self.game_windows.append(gw)
        gw.show()
        return gw

    def toggle_boss_key(self):
        if self.boss_hidden:
            self.show_from_tray()
        else:
            self.hide_to_tray()

    def hide_to_tray(self):
        if not self.boss_hidden:
            logger.info("Modo Privacidade/AFK Ativado: Escondendo janelas.")
            self.boss_hidden = True
            if self.view:
                self.view.hide()
            for gw in self.game_windows:
                try:
                    gw.hide()
                except Exception as e:
                    logger.debug(f"Erro ao ocultar janela de jogo: {e}")

    def show_from_tray(self):
        self.boss_hidden = False
        if self.view:
            self.view.showNormal()
            self.view.activateWindow()
        self.show_all_games()

    def show_all_games(self):
        for gw in self.game_windows:
            try:
                gw.showNormal()
                gw.activateWindow()
                gw.raise_()
            except Exception as e:
                logger.debug(f"Erro ao exibir janela de jogo: {e}")

    def close_all_games(self):
        for gw in self.game_windows:
            try:
                gw.close()
            except Exception as e:
                logger.debug(f"Erro ao fechar janela de jogo: {e}")
        self.game_windows.clear()
