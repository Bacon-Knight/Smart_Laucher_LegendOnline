import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap

class ImageViewerDialog(QDialog):
    def __init__(self, folder_path, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.folder_path = folder_path
        self.images = []
        self.current_index = 0
        
        self.load_images()
        
        layout = QVBoxLayout(self)
        
        self.main_card = QWidget()
        self.main_card.setObjectName("MainCard")
        self.main_card.setFixedSize(800, 650)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(72, 41, 99, 200))
        shadow.setOffset(0, 0)
        self.main_card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(self.main_card)
        
        top_bar = QHBoxLayout()
        self.lbl_title = QLabel("Galeria")
        self.lbl_title.setObjectName("TitleLabel")
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(30, 30)
        btn_close.setObjectName("TitleBtnClose")
        btn_close.clicked.connect(self.close)
        
        top_bar.addWidget(self.lbl_title)
        top_bar.addStretch()
        top_bar.addWidget(btn_close)
        
        self.image_label = QLabel("Nenhuma imagem encontrada na pasta.")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("color: white; font-size: 14px;")
        
        controls_layout = QHBoxLayout()
        self.btn_prev = QPushButton("< Anterior")
        self.btn_prev.setObjectName("LoginBtn")
        self.btn_prev.clicked.connect(self.prev_image)
        
        self.btn_next = QPushButton("Próximo >")
        self.btn_next.setObjectName("LoginBtn")
        self.btn_next.clicked.connect(self.next_image)
        
        controls_layout.addStretch()
        controls_layout.addWidget(self.btn_prev)
        controls_layout.addWidget(self.btn_next)
        controls_layout.addStretch()
        
        card_layout.addLayout(top_bar)
        card_layout.addWidget(self.image_label, 1)
        card_layout.addLayout(controls_layout)
        
        layout.addWidget(self.main_card)
        
        self.start_pos = None
        self.update_view()

    def load_images(self):
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path, exist_ok=True)
            return
            
        valid_exts = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}
        for f in os.listdir(self.folder_path):
            if os.path.splitext(f)[1].lower() in valid_exts:
                self.images.append(os.path.join(self.folder_path, f))

    def update_view(self):
        if not self.images:
            self.btn_prev.hide()
            self.btn_next.hide()
            return
            
        self.btn_prev.setVisible(len(self.images) > 1)
        self.btn_next.setVisible(len(self.images) > 1)
        
        img_path = self.images[self.current_index]
        self.lbl_title.setText(f"Galeria - {os.path.basename(img_path)} ({self.current_index + 1}/{len(self.images)})")
        
        pixmap = QPixmap(img_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(760, 540, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setText("Erro ao carregar imagem.")

    def prev_image(self):
        if self.images:
            self.current_index = (self.current_index - 1) % len(self.images)
            self.update_view()

    def next_image(self):
        if self.images:
            self.current_index = (self.current_index + 1) % len(self.images)
            self.update_view()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.start_pos is not None:
            delta = event.globalPos() - self.start_pos
            self.move(self.pos() + delta)
            self.start_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.start_pos = None

class CustomCloseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.result_action = "cancel"
        
        layout = QVBoxLayout(self)
        
        self.main_card = QWidget()
        self.main_card.setObjectName("MainCard")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(72, 41, 99, 200))
        shadow.setOffset(0, 0)
        self.main_card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(self.main_card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_msg = QLabel("Deseja realmente fechar o jogo?")
        lbl_msg.setAlignment(Qt.AlignCenter)
        lbl_msg.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 15px;")
        
        btn_layout = QHBoxLayout()
        
        self.btn_relog = QPushButton("Relogar")
        self.btn_relog.setObjectName("LaunchBtn")
        self.btn_relog.clicked.connect(self.action_relog)
        
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setObjectName("ExitBtn")
        self.btn_cancel.clicked.connect(self.action_cancel)
        
        self.btn_close = QPushButton("Sair")
        self.btn_close.setObjectName("ExitBtn")
        self.btn_close.setStyleSheet("background-color: #5c1616; border-color: #ff4d4d; color: white;")
        self.btn_close.clicked.connect(self.action_close)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_relog)
        btn_layout.addWidget(self.btn_close)
        
        card_layout.addWidget(lbl_msg)
        card_layout.addLayout(btn_layout)
        
        layout.addWidget(self.main_card)
        
    def action_relog(self):
        self.result_action = "relog"
        self.accept()
        
    def action_cancel(self):
        self.result_action = "cancel"
        self.reject()
        
    def action_close(self):
        self.result_action = "close"
        self.accept()


class RelogPromptDialog(QDialog):
    """
    Diálogo flutuante exibido 15 segundos antes de um Auto-Relog programado.
    Permite ao jogador:
    - [▶ Relogar Agora]: Executa o relog imediatamente.
    - [⏰ Adiar +30 min]: Adia o relog em 30 minutos.
    - [✕ Cancelar]: Cancela a sessão atual do relog.
    - Se o jogador estiver AFK, o timer de 15s estoura e aceita o relog automaticamente.
    """

    def __init__(self, reason_msg: str, countdown_secs: int = 15, parent=None):
        super().__init__(parent)
        from PyQt5.QtCore import QTimer
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.result_action = "relog"
        self.countdown_val = countdown_secs

        layout = QVBoxLayout(self)

        self.main_card = QWidget()
        self.main_card.setObjectName("MainCard")
        self.main_card.setFixedWidth(420)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(72, 41, 99, 200))
        shadow.setOffset(0, 0)
        self.main_card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.main_card)
        card_layout.setContentsMargins(18, 16, 18, 16)
        card_layout.setSpacing(10)

        lbl_header = QLabel("⚠️ Auto-Relog Programado")
        lbl_header.setStyleSheet("color: #d9b855; font-size: 14px; font-weight: bold;")
        lbl_header.setAlignment(Qt.AlignCenter)

        self.lbl_msg = QLabel(
            f"O jogo será recarregado em <b>{self.countdown_val}s</b> para otimização de RAM.<br>"
            f"<span style='color: #a893c4; font-size: 11px;'>Motivo: {reason_msg}</span>"
        )
        self.lbl_msg.setWordWrap(True)
        self.lbl_msg.setAlignment(Qt.AlignCenter)
        self.lbl_msg.setStyleSheet("color: white; font-size: 12px;")

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.btn_now = QPushButton("▶ Relogar Agora")
        self.btn_now.setStyleSheet(
            "QPushButton { background: #351554; border: 1px solid #c9a444; border-radius: 5px; color: white; padding: 6px; font-size: 11px; }"
            "QPushButton:hover { background: #5c3285; }"
        )
        self.btn_now.clicked.connect(self.action_relog_now)

        self.btn_postpone = QPushButton("⏰ Adiar +30 min")
        self.btn_postpone.setStyleSheet(
            "QPushButton { background: #1a1028; border: 1px solid #482963; border-radius: 5px; color: #d9b855; padding: 6px; font-size: 11px; }"
            "QPushButton:hover { border-color: #c9a444; }"
        )
        self.btn_postpone.clicked.connect(self.action_postpone)

        self.btn_cancel = QPushButton("✕ Cancelar")
        self.btn_cancel.setStyleSheet(
            "QPushButton { background: transparent; border: 1px solid #5c1616; border-radius: 5px; color: #ff4d4d; padding: 6px; font-size: 11px; }"
            "QPushButton:hover { background: #5c1616; color: white; }"
        )
        self.btn_cancel.clicked.connect(self.action_cancel)

        btn_layout.addWidget(self.btn_now)
        btn_layout.addWidget(self.btn_postpone)
        btn_layout.addWidget(self.btn_cancel)

        card_layout.addWidget(lbl_header)
        card_layout.addWidget(self.lbl_msg)
        card_layout.addLayout(btn_layout)

        layout.addWidget(self.main_card)

        # Timer de contagem regressiva (1 por segundo)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_countdown)
        self.timer.start(1000)

    def _update_countdown(self):
        self.countdown_val -= 1
        if self.countdown_val > 0:
            self.lbl_msg.setText(
                f"O jogo será recarregado em <b>{self.countdown_val}s</b> para otimização de RAM.<br>"
                f"<span style='color: #a893c4; font-size: 11px;'>Sua sessão será limpa e reiniciada.</span>"
            )
        else:
            self.timer.stop()
            self.result_action = "relog"
            self.accept()

    def action_relog_now(self):
        self.timer.stop()
        self.result_action = "relog"
        self.accept()

    def action_postpone(self):
        self.timer.stop()
        self.result_action = "postpone"
        self.accept()

    def action_cancel(self):
        self.timer.stop()
        self.result_action = "cancel"
        self.reject()

