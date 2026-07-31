from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextBrowser,
    QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class PatchNotesDialog(QDialog):
    """
    Diálogo modal com as Notas de Atualização (Patch Notes) do Launcher.
    Exibido de forma intuitiva após o aviso de doação.
    """

    DEFAULT_CHANGELOG = """
<h3>🥓 O que há de novo no BK Launcher LO v2.4.2?</h3>
<ul>
    <li><b>🔒 Criptografia DPAPI de Senhas:</b> Senhas salvas agora são encriptadas no registro do Windows via DPAPI nativa.</li>
    <li><b>🌐 Trava de Segurança no Autologin:</b> Proteção contra injeção de credenciais fora dos domínios oficiais.</li>
    <li><b>✨ Redesign do Game Hub:</b> Novo ícone de lixeira `🗑`, destaque da conta ativa e transição suave no painel.</li>
    <li><b>🧹 Limpeza de Cache de Assets:</b> Botão direto no Hub para esvaziar o cache compartilhado.</li>
    <li><b>⚡ Proxy Cache Acelerado (v8124):</b> Servidor de aceleração local ativado para zerar o lag de carregamento.</li>
</ul>
<p style='color: #a893c4;'>Aproveite o jogo com o BK Launcher LO!</p>
"""

    def __init__(self, version: str = "2.4.2", changelog_html: str = None, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(560, 420)

        main_card = QFrame(self)
        main_card.setObjectName("PatchNotesCard")
        main_card.setGeometry(0, 0, 560, 420)
        main_card.setStyleSheet("""
            #PatchNotesCard {
                background-color: #120b1c;
                border: 1px solid #351554;
                border-radius: 12px;
            }
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 0)
        main_card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        # Header bar
        header_layout = QHBoxLayout()
        lbl_subtitle = QLabel(f"LEGEND ONLINE LAUNCHER // NOVIDADES v{version}")
        lbl_subtitle.setStyleSheet("color: #c9a444; font-size: 11px; font-weight: bold;")
        
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(24, 24)
        btn_close.setStyleSheet("""
            QPushButton { background: transparent; color: #8a7a9e; font-size: 13px; font-weight: bold; border: none; }
            QPushButton:hover { color: #ff4d4d; }
        """)
        btn_close.clicked.connect(self.accept)

        header_layout.addWidget(lbl_subtitle)
        header_layout.addStretch()
        header_layout.addWidget(btn_close)
        layout.addLayout(header_layout)

        # Body area
        txt_body = QTextBrowser()
        txt_body.setOpenExternalLinks(True)
        txt_body.setStyleSheet("""
            QTextBrowser {
                background-color: #0b0712;
                border: 1px solid #231138;
                border-radius: 8px;
                color: #e1d4f2;
                font-size: 12px;
                padding: 10px;
            }
            QScrollBar:vertical {
                width: 6px;
                background: #120b1c;
            }
            QScrollBar::handle:vertical {
                background: #351554;
                border-radius: 3px;
            }
        """)
        txt_body.setHtml(changelog_html or self.DEFAULT_CHANGELOG)
        layout.addWidget(txt_body)

        # Footer button
        btn_ok = QPushButton("ENTENDIDO 👍")
        btn_ok.setFixedHeight(34)
        btn_ok.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #351554, stop:1 #5c3285);
                border: 1px solid #c9a444;
                border-radius: 6px;
                color: #ffffff;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #481f73, stop:1 #703da4);
            }
        """)
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)
