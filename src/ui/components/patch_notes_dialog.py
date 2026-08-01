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
<h3>🥓 O que há de novo no BK Launcher LO v2.4.3?</h3>
<ul>
    <li><b>🔒 Criptografia DPAPI de Senhas:</b> Senhas salvas agora são encriptadas no registro do Windows via DPAPI nativa.</li>
    <li><b>🌐 Trava de Segurança no Autologin:</b> Proteção contra injeção de credenciais fora dos domínios oficiais.</li>
    <li><b>✨ Redesign do Game Hub:</b> Novo ícone de lixeira `🗑`, destaque da conta ativa e transição suave no painel.</li>
    <li><b>🧹 Limpeza de Cache de Assets:</b> Botão direto no Hub para esvaziar o cache compartilhado.</li>
    <li><b>⚡ Proxy Cache Acelerado (v8124):</b> Servidor de aceleração local ativado para zerar o lag de carregamento.</li>
</ul>
<p style='color: #a893c4;'>Aproveite o jogo com o BK Launcher LO!</p>
"""

    def __init__(self, version: str = "2.4.3", changelog_html: str = None, parent=None):
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


class UpdateDialog(QDialog):
    """
    Diálogo modal moderno exibido quando uma nova versão do Launcher é encontrada.
    Exibe o Release Notes / Patch Notes vindo do GitHub com botão direto para download.
    """
    def __init__(self, version: str, download_url: str, release_notes: str = "", parent=None):
        super().__init__(parent)
        self.download_url = download_url
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(580, 460)

        main_card = QFrame(self)
        main_card.setObjectName("UpdateCard")
        main_card.setGeometry(0, 0, 580, 460)
        main_card.setStyleSheet("""
            #UpdateCard {
                background-color: #120b1c;
                border: 2px solid #ff4d4d;
                border-radius: 14px;
            }
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(255, 77, 77, 90))
        shadow.setOffset(0, 0)
        main_card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(main_card)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(12)

        # Header bar
        header_layout = QHBoxLayout()
        lbl_title = QLabel(f"🚀 NOVA VERSÃO v{version} DISPONÍVEL!")
        lbl_title.setStyleSheet("color: #ff4d4d; font-size: 15px; font-weight: bold;")
        
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(24, 24)
        btn_close.setStyleSheet("""
            QPushButton { background: transparent; color: #8a7a9e; font-size: 14px; font-weight: bold; border: none; }
            QPushButton:hover { color: #ff4d4d; }
        """)
        btn_close.clicked.connect(self.reject)

        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        header_layout.addWidget(btn_close)
        layout.addLayout(header_layout)

        # Body area - Patch Notes
        txt_body = QTextBrowser()
        txt_body.setOpenExternalLinks(True)
        txt_body.setStyleSheet("""
            QTextBrowser {
                background-color: #0b0712;
                border: 1px solid #351554;
                border-radius: 8px;
                color: #e1d4f2;
                font-size: 13px;
                padding: 12px;
            }
            QScrollBar:vertical {
                width: 6px;
                background: #120b1c;
            }
            QScrollBar::handle:vertical {
                background: #ff4d4d;
                border-radius: 3px;
            }
        """)

        html_notes = self.markdown_to_html(release_notes, version)
        txt_body.setHtml(html_notes)
        layout.addWidget(txt_body)

        # Footer buttons
        btn_layout = QHBoxLayout()
        
        btn_later = QPushButton("LEMBRAR MAIS TARDE")
        btn_later.setFixedHeight(38)
        btn_later.setStyleSheet("""
            QPushButton {
                background: #1a1226;
                border: 1px solid #351554;
                border-radius: 6px;
                color: #a893c4;
                font-size: 11px;
                font-weight: bold;
                padding: 0 15px;
            }
            QPushButton:hover {
                background: #2b1b3d;
                color: #ffffff;
            }
        """)
        btn_later.clicked.connect(self.reject)

        btn_download = QPushButton("🚀 BAIXAR NOVA VERSÃO AGORA")
        btn_download.setFixedHeight(38)
        btn_download.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #801515, stop:1 #b32424);
                border: 1px solid #ff4d4d;
                border-radius: 6px;
                color: #ffffff;
                font-size: 12px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #a61c1c, stop:1 #d93030);
            }
        """)
        btn_download.clicked.connect(self.on_download_clicked)

        btn_layout.addWidget(btn_later)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_download)
        layout.addLayout(btn_layout)

    def on_download_clicked(self):
        from PyQt5.QtGui import QDesktopServices
        from PyQt5.QtCore import QUrl
        QDesktopServices.openUrl(QUrl(self.download_url))
        self.accept()

    def markdown_to_html(self, text: str, version: str) -> str:
        if not text or not text.strip():
            return f"<h3 style='color: #ff4d4d;'>Uma nova versão (v{version}) do BK Launcher LO está disponível!</h3><p>Clique abaixo para fazer o download oficial no GitHub.</p>"
        
        import re
        html = text
        html = re.sub(r'###\s*(.*)', r'<h4 style="color: #c9a444; margin-top: 10px;">\1</h4>', html)
        html = re.sub(r'##\s*(.*)', r'<h3 style="color: #ff4d4d; margin-top: 12px;">\1</h3>', html)
        html = re.sub(r'#\s*(.*)', r'<h2 style="color: #ffffff; margin-top: 14px;">\1</h2>', html)
        html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html)
        html = re.sub(r'\*(.*?)\*', r'<i>\1</i>', html)
        html = re.sub(r'^\*\s*(.*)', r'• \1<br>', html, flags=re.MULTILINE)
        html = re.sub(r'^\-\s*(.*)', r'• \1<br>', html, flags=re.MULTILINE)
        html = html.replace('\n', '<br>')
        return html
