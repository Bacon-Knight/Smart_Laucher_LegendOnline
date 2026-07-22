from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer


class FloatingMacroPanel(QWidget):
    """
    Painel flutuante arrastavel com atalhos de macro.
    Fica sempre sobre o jogo (WindowStaysOnTopHint).
    Aberto via botao na title bar da GameWindow.
    """

    def __init__(self, game_window):
        super().__init__(None)  # sem pai = janela independente
        self.game_window = game_window
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool  # nao aparece na barra de tarefas
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._drag_pos = None
        self._build_ui()
        self.adjustSize()

    # ------------------------------------------------------------------
    # Estilo dos botoes
    # ------------------------------------------------------------------
    def _btn_style(self, bg, border):
        return (
            "QPushButton {"
            f" background-color: {bg}; border: 1px solid {border};"
            " border-radius: 6px; color: #e0d0b0;"
            " font-size: 11px; padding: 4px 8px; }"
            " QPushButton:hover { border-color: #d9b855; color: #d9b855; }"
            " QPushButton:checked { background-color: #351554;"
            " border-color: #d9b855; color: #d9b855; }"
        )

    # ------------------------------------------------------------------
    # Construcao da UI
    # ------------------------------------------------------------------
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.card = QWidget()
        self.card.setObjectName("FloatCard")
        self.card.setStyleSheet(
            "#FloatCard {"
            " background-color: rgba(18,12,24,220);"
            " border: 1px solid #482963;"
            " border-radius: 8px; }"
        )

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(8, 6, 8, 8)
        card_layout.setSpacing(6)

        # -- Cabecalho arrastavel --
        header = QHBoxLayout()
        lbl_title = QLabel("\u26a1 Macros")
        lbl_title.setStyleSheet("color: #d9b855; font-size: 11px; font-weight: bold;")

        btn_close = QPushButton("\u2715")
        btn_close.setFixedSize(16, 16)
        btn_close.setStyleSheet(
            "QPushButton { background: transparent; border: none;"
            " color: #8c73a6; font-size: 10px; }"
            " QPushButton:hover { color: #ff4d4d; }"
        )
        btn_close.clicked.connect(self.hide)

        header.addWidget(lbl_title)
        header.addStretch()
        header.addWidget(btn_close)
        card_layout.addLayout(header)

        # Separador
        sep = QWidget()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #351554;")
        card_layout.addWidget(sep)

        # -- AutoClick --
        self.btn_autoclick = QPushButton("🎯 AutoClick: OFF")
        self.btn_autoclick.setCheckable(True)
        self.btn_autoclick.setStyleSheet(self._btn_style("#2b1b3d", "#482963"))
        self.btn_autoclick.toggled.connect(self._toggle_autoclick)
        card_layout.addWidget(self.btn_autoclick)

        # -- Fast Relog --
        btn_relog = QPushButton("🔄 Fast Relog")
        btn_relog.setStyleSheet(self._btn_style("#1a1a2e", "#2d6ca3"))
        btn_relog.clicked.connect(self.game_window.fast_relog)
        card_layout.addWidget(btn_relog)

        # -- Status --
        self.lbl_status = QLabel("Pronto.")
        self.lbl_status.setStyleSheet("color: #888; font-size: 10px;")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.lbl_status)

        root.addWidget(self.card)

        # Sincroniza estado com a GameWindow a cada 500ms
        self._sync_timer = QTimer(self)
        self._sync_timer.timeout.connect(self._sync_state)
        self._sync_timer.start(500)

    # ------------------------------------------------------------------
    # Acoes dos botoes
    # ------------------------------------------------------------------
    def _toggle_autoclick(self, checked):
        if checked:
            self.game_window.start_autoclicker()
        else:
            self.game_window.stop_macros()

    def _sync_state(self):
        """Mantém os botoes sincronizados com o estado real da GameWindow."""
        gw = self.game_window

        autoclick_on = (
            gw.macro_worker is not None
            and gw.macro_worker.isRunning()
            and getattr(gw, "macro_type", "") == "autoclick"
        )
        self.btn_autoclick.blockSignals(True)
        self.btn_autoclick.setChecked(autoclick_on)
        self.btn_autoclick.setText(
            "🎯 AutoClick: ON" if autoclick_on else "🎯 AutoClick: OFF"
        )
        self.btn_autoclick.blockSignals(False)

    # ------------------------------------------------------------------
    # Drag (arrastar pelo cabecalho)
    # ------------------------------------------------------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
