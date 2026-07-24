import os
import gc
import time

try:
    import psutil
except ImportError:
    psutil = None

from typing import Optional
from PyQt5.QtCore import QObject, QTimer, QUrl
from src.core.logger import get_logger, mask_email
from src.models.game_session import GameSession
from src.models.relog_schedule import RelogScheduler
from src.ui.components.dialogs import RelogPromptDialog, RAMLimitDialog

logger = get_logger("GameController")

class GameController(QObject):
    """
    Controlador MVC responsável pela sessão da Janela do Jogo:
    - Gerencia o ciclo de vida do navegador (QtWebEngine).
    - Executa o Fast Relog (about:blank + gc.collect() + recarregamento).
    - Avisos inteligentes pré-eventos (sem forçar o relog se o usuário ignorar).
    - Monitoramento de RAM a cada 5 minutos (limite de 700 MB ideal para Multi-Boxing de 4 contas).
    - Controle de qualidade gráfica do Flash Player (Baixa, Média, Alta).
    - Controla a execução de macros (AutoClick, Formação, Custom).
    """

    # Limite padrão de RAM por janela (700 MB é o ponto ideal para rodar 4 contas no mesmo PC)
    RAM_LIMIT_MB = 700

    def __init__(self, session: GameSession, view, stagger_index: int = 0):
        super().__init__()
        self.session = session
        self.view = view
        self.stagger_index = stagger_index
        self._pending_relog_afk = False
        self.macro_worker = None
        self.macro_type = None

        # Timer de Aviso Pré-Evento
        self.relog_timer = QTimer(self)
        self.relog_timer.setSingleShot(True)
        self.relog_timer.timeout.connect(self._on_auto_relog_trigger)

        # Timer de Monitoramento de Memória RAM (A cada 5 minutos = 300.000 ms)
        self.ram_timer = QTimer(self)
        self.ram_timer.setInterval(5 * 60 * 1000)
        self.ram_timer.timeout.connect(self.check_ram_usage)
        self.ram_timer.start()

        if self.session.auto_relog_enabled:
            self.schedule_next_auto_relog()

    def schedule_next_auto_relog(self, custom_delay_secs: Optional[int] = None):
        """Agenda o próximo aviso pré-evento em segundos com deslocamento estocástico (stagger)."""
        if custom_delay_secs is not None:
            secs = custom_delay_secs
            reason = "Adiado pelo usuário"
        else:
            secs, reason = RelogScheduler.calculate_next_relog_seconds(default_interval_mins=120)
            # Adiciona um deslocamento por índice de janela (0s, 7s, 14s, 21s...) para evitar colisões
            stagger_offset = (self.stagger_index % 8) * 7
            secs += stagger_offset

        ms = secs * 1000
        self.relog_timer.stop()
        self.relog_timer.start(ms)

        mins = secs // 60
        logger.info(f"[{mask_email(self.session.email)}] Próximo aviso de evento em {mins} min ({secs}s). Motivo: {reason}")

    def _on_auto_relog_trigger(self):
        """Disparado quando o temporizador de evento se aproxima."""
        if getattr(self.view, "_is_closing", False):
            return

        secs, reason = RelogScheduler.calculate_next_relog_seconds()

        # Se a janela está visível na tela, exibe o aviso flutuante
        if hasattr(self.view, 'isVisible') and self.view.isVisible():
            dialog = RelogPromptDialog(reason_msg=reason, countdown_secs=20, parent=self.view)
            dialog.exec_()
            action = dialog.result_action
        else:
            # Se a janela está oculta (Modo AFK / Tray), agenda para relogar limpo quando for restaurada
            logger.info(f"[{mask_email(self.session.email)}] Aviso pré-evento em modo AFK (Janela Oculta). Agendando relog limpo para quando a janela for restaurada...")
            self._pending_relog_afk = True
            self.schedule_next_auto_relog()
            return

        if action == "relog":
            logger.info(f"[{mask_email(self.session.email)}] Executando Relog aceito pelo usuário...")
            self.fast_relog()
            self.schedule_next_auto_relog()
        elif action == "postpone":
            logger.info(f"[{mask_email(self.session.email)}] Relog adiado por 30 minutos.")
            self.schedule_next_auto_relog(custom_delay_secs=30 * 60)
        else:
            logger.info(f"[{mask_email(self.session.email)}] Relog ignorado pelo usuário. O jogo continua normalmente sem interrupção.")
            self.schedule_next_auto_relog()

    def check_ram_usage(self):
        """
        Monitora o consumo de RAM da instância a cada 5 minutos.
        Se ultrapassar 700 MB (ideal para multi-boxing de 4 contas), sugere relog ao usuário.
        """
        if getattr(self.view, "_is_closing", False) or not hasattr(self.view, 'isVisible') or not self.view.isVisible():
            return

        try:
            ram_mb = 0
            if psutil:
                proc = psutil.Process(os.getpid())
                mem = proc.memory_info()
                ram_mb = int(mem.rss / (1024 * 1024))

            if ram_mb > self.RAM_LIMIT_MB:
                logger.warning(f"[{mask_email(self.session.email)}] Alerta de RAM: Janela consumindo {ram_mb} MB (Limite: {self.RAM_LIMIT_MB} MB).")
                dialog = RAMLimitDialog(ram_mb=ram_mb, limit_mb=self.RAM_LIMIT_MB, parent=self.view)
                dialog.exec_()
                if dialog.result_action == "relog":
                    logger.info(f"[{mask_email(self.session.email)}] Relog acionado via Alerta de RAM ({ram_mb} MB).")
                    self.fast_relog()
        except Exception as e:
            logger.debug(f"Erro ao verificar consumo de RAM: {e}")

    def set_flash_quality(self, quality: str = "low"):
        """
        Injeta a configuração de qualidade no Flash Player ('low', 'medium', 'high').
        'low' desativa anti-aliasing e economiza CPU/GPU para Multi-boxing.
        """
        if getattr(self.view, "_is_closing", False) or not hasattr(self.view, 'page') or self.view.page is None:
            return

        js_script = f"""
        (function(q) {{
            var elems = document.querySelectorAll('embed, object');
            elems.forEach(function(el) {{
                el.setAttribute('quality', q);
                try {{
                    if (typeof el.SetVariable === 'function') {{
                        el.SetVariable('stage.quality', q.toUpperCase());
                    }}
                }} catch(e) {{}}
            }});
            console.log('Qualidade do Flash ajustada para:', q);
        }})('{quality}');
        """
        try:
            self.view.page.runJavaScript(js_script)
            logger.info(f"[{mask_email(self.session.email)}] Qualidade gráfica do Flash ajustada para: {quality.upper()}")
        except Exception as e:
            logger.error(f"Erro ao aplicar qualidade do Flash: {e}")

    def check_pending_afk_relog(self):
        """Executa o relog pendente assim que a janela é restaurada do modo AFK / Tray."""
        if getattr(self, '_pending_relog_afk', False):
            self._pending_relog_afk = False
            logger.info(f"[{mask_email(self.session.email)}] Executando Auto-Relog pendente do modo AFK...")
            self.fast_relog()

    def fast_relog(self):
        """Executa o recarregamento seguro da sessão do jogo sem derrubar o plugin Flash."""
        if getattr(self.view, "_is_closing", False) or not hasattr(self.view, 'browser') or self.view.browser is None:
            return

        logger.info(f"[{mask_email(self.session.email)}] Recarregando sessão do jogo (Fast Relog)...")
        try:
            self.view.browser.setUrl(QUrl(self.session.url))
            gc.collect()
        except Exception as e:
            logger.error(f"Erro ao recarregar página no Fast Relog: {e}")

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
