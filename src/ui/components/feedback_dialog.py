from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QTextEdit, QLineEdit, QCheckBox, QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor
from src.services.feedback_service import FeedbackService

class FeedbackSendThread(QThread):
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, category, message, contact, include_logs):
        super().__init__()
        self.category = category
        self.message = message
        self.contact = contact
        self.include_logs = include_logs

    def run(self):
        success, reason = FeedbackService.send_feedback(
            category=self.category,
            message=self.message,
            user_contact=self.contact,
            include_logs=self.include_logs
        )
        self.finished_signal.emit(success, reason)


class FeedbackDialog(QDialog):
    """
    Diálogo modal para envio direto de sugestões ou bugs ao Discord da comunidade.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(500, 440)

        main_card = QFrame(self)
        main_card.setObjectName("FeedbackCard")
        main_card.setGeometry(0, 0, 500, 440)
        main_card.setStyleSheet("""
            #FeedbackCard {
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

        # Header
        header_layout = QHBoxLayout()
        lbl_title = QLabel("💬 ENVIAR FEEDBACK OU BUG")
        lbl_title.setStyleSheet("color: #d9b855; font-size: 13px; font-weight: bold;")
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(24, 24)
        btn_close.setStyleSheet("""
            QPushButton { background: transparent; color: #8a7a9e; font-size: 13px; font-weight: bold; border: none; }
            QPushButton:hover { color: #ff4d4d; }
        """)
        btn_close.clicked.connect(self.reject)

        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        header_layout.addWidget(btn_close)
        layout.addLayout(header_layout)

        # Category
        lbl_cat = QLabel("Categoria:")
        lbl_cat.setStyleSheet("color: #a893c4; font-size: 11px;")
        self.combo_cat = QComboBox()
        self.combo_cat.addItems(["Relato de Bug 🐛", "Sugestão de Recurso 💡", "Dúvida / Outro ❓"])
        self.combo_cat.setStyleSheet("""
            QComboBox {
                background-color: #0b0712;
                border: 1px solid #351554;
                border-radius: 5px;
                color: white;
                padding: 4px 8px;
            }
        """)
        layout.addWidget(lbl_cat)
        layout.addWidget(self.combo_cat)

        # Message Body
        lbl_msg = QLabel("Descrição detalhada:")
        lbl_msg.setStyleSheet("color: #a893c4; font-size: 11px;")
        self.txt_msg = QTextEdit()
        self.txt_msg.setPlaceholderText("Descreva o problema ou sugestão aqui...")
        self.txt_msg.setStyleSheet("""
            QTextEdit {
                background-color: #0b0712;
                border: 1px solid #351554;
                border-radius: 6px;
                color: white;
                padding: 8px;
            }
        """)
        layout.addWidget(lbl_msg)
        layout.addWidget(self.txt_msg)

        # Optional Contact
        self.input_contact = QLineEdit()
        self.input_contact.setPlaceholderText("Seu Discord ou E-mail para contato (Opcional)")
        self.input_contact.setStyleSheet("""
            QLineEdit {
                background-color: #0b0712;
                border: 1px solid #351554;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
        """)
        layout.addWidget(self.input_contact)

        # Checkbox for logs
        self.chk_logs = QCheckBox("Anexar últimas linhas do Log (Ajuda na investigação de erros)")
        self.chk_logs.setChecked(True)
        self.chk_logs.setStyleSheet("color: #8a7a9e; font-size: 10px;")
        layout.addWidget(self.chk_logs)

        # Submit button
        self.btn_send = QPushButton("ENVIAR FEEDBACK 🚀")
        self.btn_send.setFixedHeight(34)
        self.btn_send.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #351554, stop:1 #5c3285);
                border: 1px solid #c9a444;
                border-radius: 6px;
                color: #ffffff;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #481f73, stop:1 #703da4);
            }
        """)
        self.btn_send.clicked.connect(self.submit_feedback)
        layout.addWidget(self.btn_send)

    def submit_feedback(self):
        msg_text = self.txt_msg.toPlainText().strip()
        if not msg_text:
            QMessageBox.warning(self, "Aviso", "Por favor, digite uma mensagem antes de enviar.")
            return

        self.btn_send.setEnabled(False)
        self.btn_send.setText("ENVIANDO...")

        cat = self.combo_cat.currentText()
        contact = self.input_contact.text().strip()
        include_logs = self.chk_logs.isChecked()

        self.thread = FeedbackSendThread(cat, msg_text, contact, include_logs)
        self.thread.finished_signal.connect(self.on_sent_result)
        self.thread.start()

    def on_sent_result(self, success: bool, reason: str):
        self.btn_send.setEnabled(True)
        self.btn_send.setText("ENVIAR FEEDBACK 🚀")
        if success:
            QMessageBox.information(self, "Sucesso", "Obrigado! Seu feedback foi enviado diretamente à nossa equipe.")
            self.accept()
        elif reason == "NO_WEBHOOK":
            QMessageBox.warning(
                self, "Servidor de Feedback Desativado",
                "O envio de feedback está desativado nesta compilação local.\n\n"
                "A variável de ambiente 'DISCORD_WEBHOOK_URL' não está configurada no ambiente do projeto.\n"
                "Defina a variável no ambiente ou no arquivo de build para habilitar o envio direto."
            )
        else:
            QMessageBox.warning(
                self, "Falha na Conexão com o Discord",
                "Não foi possível conectar ao servidor do Discord para enviar o feedback.\n\n"
                "Verifique se o Discord/Webhook está acessível ou se sua conexão caiu."
            )
