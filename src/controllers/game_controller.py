import gc
import time
from typing import Optional
from PyQt5.QtCore import QObject, QTimer, QUrl
from src.core.logger import get_logger, mask_email
from src.models.game_session import GameSession
from src.models.relog_schedule import RelogScheduler
from src.ui.components.dialogs import RelogPromptDialog

logger = get_logger("GameController")

class GameController(QObject):
    """
    Controlador MVC responsável pela sessão da Janela do Jogo:
    - Gerencia o ciclo de vida do navegador (QtWebEngine).
    - Executa o Fast Relog (about:blank + gc.collect() + recarregamento).
    - Agenda o Auto-Relog Inteligente (15 min antes dos eventos das 11h, 13h, 15h, 17h, 19h, 21:35).
    - Dispara o popup de aviso de 15 segundos para o jogador antes de relogar.
    - Controla a execução de macros (AutoClick, Formação, Custom).
    """

    def __init__(self, session: GameSession, view):
        super().__init__()
        self.session = session
        self.view = view
        self.macro_worker = None
        self.macro_type = None

        # Timer de Auto-Relog Inteligente
        self.relog_timer = QTimer(self)
        self.relog_timer.setSingleShot(True)
        self.relog_timer.timeout.connect(self._on_auto_relog_trigger)

        if self.session.auto_relog_enabled:
            self.schedule_next_auto_relog()

    def schedule_next_auto_relog(self, custom_delay_secs: Optional[int] = None):
        """Agenda o próximo relog automático em segundos."""
        if custom_delay_secs is not None:
            secs = custom_delay_secs
            reason = "Adiado a pedido do usuário"
        else:
            secs, reason = RelogScheduler.calculate_next_relog_seconds(default_interval_mins=120)

        ms = secs * 1000
        self.relog_timer.stop()
        self.relog_timer.start(ms)

        mins = secs // 60
        logger.info(f"[{mask_email(self.session.email)}] Próximo Auto-Relog agendado em {mins} min ({secs}s). Motivo: {reason}")

    def _on_auto_relog_trigger(self):
        """Disparado quando o temporizador de Auto-Relog zera. Exibe a caixa de diálogo de 15s."""
        # Se a janela foi fechada ou está minimizada sem uso, não exibe
        if getattr(self.view, "_is_closing", False):
            return

        secs, reason = RelogScheduler.calculate_next_relog_seconds()
        
        # Exibe o popup com contagem regressiva de 15s
        dialog = RelogPromptDialog(reason_msg=reason, countdown_secs=15, parent=self.view)
        dialog.exec_()

        if dialog.result_action == "relog":
            logger.info(f"[{mask_email(self.session.email)}] Executando Auto-Relog programado...")
            self.fast_relog()
            # Reagenda para o próximo ciclo
            self.schedule_next_auto_relog()
        elif dialog.result_action == "postpone":
            logger.info(f"[{mask_email(self.session.email)}] Auto-Relog adiado por 30 minutos a pedido do usuário.")
            self.schedule_next_auto_relog(custom_delay_secs=30 * 60)
        else:
            logger.info(f"[{mask_email(self.session.email)}] Auto-Relog cancelado para este ciclo.")
            # Reagenda para o próximo ciclo
            self.schedule_next_auto_relog()

    def fast_relog(self):
        """Executa a limpeza da memória RAM e recarrega a sessão do jogo."""
        logger.info(f"[{mask_email(self.session.email)}] Limpando Memória (Fast Relog)...")
        # Descarrega a página para liberar RAM do Flash Player
        self.view.browser.setUrl(QUrl("about:blank"))
        gc.collect()

        # Recarrega o portal após 500ms
        QTimer.singleShot(500, lambda: self.view.browser.setUrl(QUrl(self.session.url)))

    def apply_zoom_debounced(self):
        """Aplica o fator de zoom com debounce de 150ms ao redimensionar a janela."""
        if getattr(self.view, '_is_closing', False) or not hasattr(self.view, 'page') or self.view.page is None:
            return
        try:
            base_width = 1040.0
            base_height = 800.0
            zoom_x = self.view.width() / base_width
            zoom_y = self.view.height() / base_height
            zoom_factor = max(0.2, min(zoom_x, zoom_y))
            self.view.page.setZoomFactor(zoom_factor)
        except Exception as e:
            logger.debug(f"Erro ao aplicar zoom factor: {e}")

    def stop_macros(self):
        """Interrompe qualquer macro em execução."""
        if hasattr(self.view, 'timer_countdown'):
            self.view.timer_countdown.stop()

        if self.macro_worker and self.macro_worker.isRunning():
            self.macro_worker.stop()
            self.macro_worker.wait()
            self.macro_worker = None

        display_name = self.session.nickname if self.session.nickname else self.session.email
        self.view.title_bar.title.setText(f"Legend Online - Jogando como: {display_name}")
