import json
import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QLineEdit, QSystemTrayIcon, QMenu, QAction, QMessageBox,
    QGraphicsDropShadowEffect, QStyle, QApplication, QShortcut, QCheckBox,
    QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QTimer, QUrl, QPoint
from PyQt5.QtGui import QColor, QKeySequence, QDesktopServices

from src.core.logger import get_logger
from src.core.config import resource_path
from src.controllers.hub_controller import HubController
from src.ui.components.title_bar import CustomTitleBar

logger = get_logger("HubView")

class HubView(QMainWindow):
    """
    Camada VIEW da arquitetura MVC para o Launcher Hub.
    Focada exclusivamente na construção e atualização da interface gráfica.
    Delegando a lógica de estado e persistência para o HubController.
    """

    def __init__(self, controller: HubController = None):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 1100, 80)
        self._grid_visible = False

        self.controller = controller or HubController(view=self)
        self.controller.view = self

        self.setup_tray()

        self.shortcut_boss = QShortcut(QKeySequence("Ctrl+Shift+A"), self)
        self.shortcut_boss.setContext(Qt.ApplicationShortcut)
        self.shortcut_boss.activated.connect(self.controller.toggle_boss_key)

        self.init_ui()
        self.load_styles()

        QTimer.singleShot(600, self.check_previous_crash)
        QTimer.singleShot(1200, self.show_donation_popup)

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        tray_menu = QMenu()
        tray_menu.setStyleSheet("QMenu { background-color: #2b1b3d; color: white; border: 1px solid #c9a444; } QMenu::item:selected { background-color: #c9a444; color: black; }")
        
        action_show = QAction("Mostrar Hub", self)
        action_show.triggered.connect(lambda: [self.showNormal(), self.activateWindow()])
        tray_menu.addAction(action_show)
        
        action_show_all = QAction("Mostrar Todos os Jogos", self)
        action_show_all.triggered.connect(self.controller.show_all_games)
        tray_menu.addAction(action_show_all)
        
        action_close_all = QAction("Encerrar todas as contas", self)
        action_close_all.triggered.connect(self.controller.close_all_games)
        tray_menu.addAction(action_close_all)
        
        tray_menu.addSeparator()
        
        action_exit = QAction("Sair do Launcher", self)
        action_exit.triggered.connect(self.close)
        tray_menu.addAction(action_exit)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_activated)
        self.tray_icon.show()

    def tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.controller.show_from_tray()

    def closeEvent(self, event):
        self.controller.close_all_games()
        event.accept()

    def load_styles(self):
        try:
            qss_path = resource_path("style.qss")
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            logger.error(f"style.qss não encontrado: {e}")

    def init_ui(self):
        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(15, 15, 15, 15)
        self.setCentralWidget(wrapper)
        
        self.main_card = QWidget()
        self.main_card.setObjectName("MainCard")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(72, 41, 99, 200))
        shadow.setOffset(0, 0)
        self.main_card.setGraphicsEffect(shadow)
        
        wrapper_layout.addWidget(self.main_card)
        
        card_layout = QVBoxLayout(self.main_card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)
        
        self.title_bar = CustomTitleBar(self)
        self.title_bar.setObjectName("TitleBar")
        card_layout.addWidget(self.title_bar)
        
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 5, 20, 5)
        content_layout.setSpacing(8)
        
        self.saved_accounts = self.controller.get_saved_accounts()
            
        email_container = QWidget()
        email_layout = QHBoxLayout(email_container)
        email_layout.setContentsMargins(0, 0, 0, 0)
        email_layout.setSpacing(5)
        
        self.input_email = QComboBox()
        self.input_email.setEditable(True)
        self.input_email.lineEdit().setPlaceholderText("E-mail da Conta")
        self.input_email.addItems(list(self.saved_accounts.keys()))
        self.input_email.setCurrentText(self.controller.settings.value("last_email", ""))
        self.input_email.currentTextChanged.connect(self.on_email_changed)
        self.input_email.setMinimumWidth(200)
        
        self.btn_accounts = QPushButton("📋")
        self.btn_accounts.setObjectName("TogglePassBtn") 
        self.btn_accounts.setFixedSize(30, 30)
        self.btn_accounts.setToolTip("Mostrar/ocultar painel de contas salvas")
        self.btn_accounts.clicked.connect(self.toggle_accounts_grid)
        
        email_layout.addWidget(self.input_email)
        email_layout.addWidget(self.btn_accounts)
        
        pass_container = QWidget()
        pass_layout = QHBoxLayout(pass_container)
        pass_layout.setContentsMargins(0, 0, 0, 0)
        pass_layout.setSpacing(5)
        
        current_acc = self.saved_accounts.get(self.input_email.currentText(), {})
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setPlaceholderText("Senha")
        self.input_password.setText(current_acc.get("password", ""))
        self.input_password.setMinimumWidth(150)
        
        self.btn_toggle_pass = QPushButton("👁")
        self.btn_toggle_pass.setObjectName("TogglePassBtn")
        self.btn_toggle_pass.setFixedSize(30, 30)
        self.btn_toggle_pass.clicked.connect(self.toggle_password_visibility)
        
        pass_layout.addWidget(self.input_password)
        pass_layout.addWidget(self.btn_toggle_pass)
        
        self.input_server = QLineEdit()
        self.input_server.setPlaceholderText("Srv (ex: 1252)")
        self.input_server.setText(current_acc.get("server", self.controller.settings.value("server", "1252")))
        self.input_server.setFixedWidth(100)
        
        self.input_nick = QLineEdit()
        self.input_nick.setPlaceholderText("Nick")
        self.input_nick.setText(current_acc.get("nick", ""))
        self.input_nick.setFixedWidth(120)
        
        self.chk_afk = QCheckBox("Modo Oculto")
        self.chk_afk.setToolTip("Oculta o jogo após 2 min de inatividade (Modo Chefe)")
        self.chk_afk.setStyleSheet("color: white;")
        self.chk_afk.setChecked(self.controller.settings.value("afk_enabled", True, type=bool))
        self.chk_afk.stateChanged.connect(self.on_afk_changed)
        
        self.btn_ok = QPushButton(" INICIAR JOGO ")
        self.btn_ok.setObjectName("LaunchBtn")
        self.btn_ok.setFixedHeight(30)
        self.btn_ok.setMinimumWidth(140)
        self.btn_ok.clicked.connect(self.launch_game)
        
        self.btn_cancel = QPushButton(" SAIR ")
        self.btn_cancel.setObjectName("ExitBtn")
        self.btn_cancel.setFixedHeight(30)
        self.btn_cancel.setFixedWidth(80)
        self.btn_cancel.clicked.connect(self.close)
        
        content_layout.addWidget(email_container)
        content_layout.addWidget(pass_container)
        content_layout.addWidget(self.input_server)
        content_layout.addWidget(self.input_nick)
        content_layout.addStretch()
        content_layout.addWidget(self.btn_ok)
        content_layout.addWidget(self.btn_cancel)
        content_layout.addWidget(self.chk_afk)
        
        card_layout.addWidget(content_widget)

        # ── Grid de Contas (colapsável) ──────────────────────────────
        self.accounts_grid_container = QWidget()
        self.accounts_grid_container.setVisible(False)

        grid_outer = QVBoxLayout(self.accounts_grid_container)
        grid_outer.setContentsMargins(12, 4, 12, 8)
        grid_outer.setSpacing(0)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #351554;")
        grid_outer.addWidget(sep)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(160)
        self.scroll_area.setStyleSheet(
            "QScrollArea { border: none; background: transparent; }"
            "QScrollBar:horizontal { height: 6px; background: #1e1526; }"
            "QScrollBar::handle:horizontal { background: #482963; border-radius: 3px; }"
        )
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")
        self.scroll_layout = QHBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 6, 0, 4)
        self.scroll_layout.setSpacing(8)
        self.scroll_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_content)
        grid_outer.addWidget(self.scroll_area)

        card_layout.addWidget(self.accounts_grid_container)
        self._refresh_accounts_grid()

    def toggle_accounts_grid(self):
        """Expande ou recolhe o painel de cartões de contas."""
        self._grid_visible = not self._grid_visible
        self.accounts_grid_container.setVisible(self._grid_visible)
        if self._grid_visible:
            self.setFixedHeight(260)
            self._refresh_accounts_grid()
        else:
            self.setFixedHeight(80)
        self.adjustSize()

    def _refresh_accounts_grid(self):
        """Reconstrói todos os cartões de conta no scroll horizontal."""
        self.saved_accounts = self.controller.get_saved_accounts()
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.saved_accounts:
            lbl = QLabel("Nenhuma conta salva ainda.")
            lbl.setStyleSheet("color: #666; font-size: 11px;")
            self.scroll_layout.insertWidget(0, lbl)
            return

        for email, data in self.saved_accounts.items():
            card = self._make_account_card(email, data)
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, card)

    def _make_account_card(self, email, data):
        """Cria um cartão visual para uma conta."""
        nick   = data.get("nick", "") or email.split("@")[0]
        server = data.get("server", "?")
        last   = data.get("last_login", "Nunca")

        card = QWidget()
        card.setFixedWidth(160)
        card.setStyleSheet(
            "QWidget { background-color: #1a1028; border: 1px solid #351554;"
            " border-radius: 8px; }"
            "QWidget:hover { border-color: #c9a444; }"
        )

        layout = QVBoxLayout(card)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(3)

        lbl_nick = QLabel(nick[:18])
        lbl_nick.setStyleSheet("color: #d9b855; font-weight: bold; font-size: 12px; border: none;")
        lbl_nick.setAlignment(Qt.AlignCenter)

        lbl_server = QLabel(f"Servidor {server}")
        lbl_server.setStyleSheet("color: #a893c4; font-size: 10px; border: none;")
        lbl_server.setAlignment(Qt.AlignCenter)

        lbl_email = QLabel(email[:22] + ("…" if len(email) > 22 else ""))
        lbl_email.setStyleSheet("color: #666; font-size: 9px; border: none;")
        lbl_email.setAlignment(Qt.AlignCenter)
        lbl_email.setToolTip(email)

        lbl_last = QLabel(f"🕐 {last}")
        lbl_last.setStyleSheet("color: #444; font-size: 9px; border: none;")
        lbl_last.setAlignment(Qt.AlignCenter)

        btn_enter = QPushButton("▶ Entrar")
        btn_enter.setObjectName("LaunchBtn")
        btn_enter.setFixedHeight(24)
        btn_enter.setStyleSheet(
            "QPushButton { background: #351554; border: 1px solid #c9a444;"
            " border-radius: 5px; color: white; font-size: 10px; }"
            "QPushButton:hover { background: #5c3285; }"
        )
        btn_enter.clicked.connect(lambda _, e=email, d=data: self._launch_from_card(e, d))

        btn_del = QPushButton("✕")
        btn_del.setFixedSize(20, 20)
        btn_del.setStyleSheet(
            "QPushButton { background: transparent; border: none; color: #482963; font-size: 10px; }"
            "QPushButton:hover { color: #ff4d4d; }"
        )
        btn_del.clicked.connect(lambda _, e=email: self._delete_from_card(e))

        top_row = QHBoxLayout()
        top_row.addStretch()
        top_row.addWidget(btn_del)
        layout.addLayout(top_row)
        layout.addWidget(lbl_nick)
        layout.addWidget(lbl_server)
        layout.addWidget(lbl_email)
        layout.addWidget(lbl_last)
        layout.addStretch()
        layout.addWidget(btn_enter)

        return card

    def _launch_from_card(self, email, data):
        self.input_email.setCurrentText(email)
        self.input_password.setText(data.get("password", ""))
        self.input_server.setText(data.get("server", "1252"))
        self.input_nick.setText(data.get("nick", ""))
        self.launch_game()

    def _delete_from_card(self, email):
        reply = QMessageBox.question(self, "Excluir Conta", f"Tem certeza que deseja excluir a conta {email}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.controller.delete_account(email)
            self._refresh_accounts_grid()

    def on_email_changed(self, text):
        self.saved_accounts = self.controller.get_saved_accounts()
        if text in self.saved_accounts:
            acc = self.saved_accounts[text]
            self.input_password.setText(acc.get("password", ""))
            self.input_server.setText(acc.get("server", ""))
            self.input_nick.setText(acc.get("nick", ""))

    def on_afk_changed(self, state):
        self.controller.settings.setValue("afk_enabled", state == Qt.Checked)

    def toggle_password_visibility(self):
        if self.input_password.echoMode() == QLineEdit.Password:
            self.input_password.setEchoMode(QLineEdit.Normal)
            self.btn_toggle_pass.setText("X")
        else:
            self.input_password.setEchoMode(QLineEdit.Password)
            self.btn_toggle_pass.setText("👁")

    def launch_game(self):
        email = self.input_email.currentText().strip()
        password = self.input_password.text()
        server_num = self.input_server.text().strip()
        nick = self.input_nick.text().strip()
        
        if not email:
            QMessageBox.warning(self, "Aviso de Autenticação", "Por favor, digite ou selecione um e-mail.")
            return
            
        if not server_num:
            QMessageBox.warning(self, "Aviso de Servidor", "O número do servidor não pode ficar vazio.")
            return
        
        self.controller.launch_game(email, password, server_num, nick)
        self._refresh_accounts_grid()

    def show_donation_popup(self):
        try:
            msg = QMessageBox(self)
            msg.setWindowTitle("Apoie o Projeto 🥓")
            msg.setTextFormat(Qt.RichText)
            msg.setTextInteractionFlags(Qt.TextBrowserInteraction)
            msg.setText(
                "<h3>Gostando do Bacon Knight Launcher? 🥓</h3>"
                "<p>Este projeto é feito para a comunidade!<br>"
                "Considere pagar um bacon para o desenvolvedor.</p>"
                "<br><a href='https://Bacon-Knight.github.io/Smart_Laucher_LegendOnline/' style='color: #c9a444;'>👉 Clique aqui para visitar nosso site oficial e fazer uma doação anônima!</a><br><br>"
            )
            msg.setIcon(QMessageBox.Information)
            msg.addButton("Entendido!", QMessageBox.AcceptRole)
            msg.setStyleSheet("QMessageBox { background-color: #120c18; color: white; } QLabel { color: white; } QPushButton { background-color: #2b1b3d; color: white; padding: 5px 15px; border: 1px solid #c9a444; border-radius: 4px; }")
            msg.exec_()
        except Exception as e:
            logger.error(f"Erro no popup de doacao: {e}")

    def check_previous_crash(self):
        try:
            if self.controller.settings.value("has_crashed", False, type=bool):
                log_path = self.controller.settings.value("last_crash_log", "")
                err_code = self.controller.settings.value("last_crash_code", "ERR-UNK-999")
                
                self.controller.settings.setValue("has_crashed", False)
                
                msg = QMessageBox(self)
                msg.setWindowTitle("⚠️ Relatório de Encerramento Inesperado")
                msg.setIcon(QMessageBox.Warning)
                msg.setText(
                    f"<h3>O Launcher detectou um encerramento inesperado na última execução [{err_code}].</h3>"
                    f"<p>Os logs detalhados do erro foram salvos em:<br><b>{log_path}</b></p>"
                    f"<p>Deseja abrir a pasta onde o log está salvo para envio ao suporte?</p>"
                )
                btn_open = msg.addButton("📁 Abrir Pasta do Log", QMessageBox.ActionRole)
                btn_ok = msg.addButton("OK", QMessageBox.AcceptRole)
                
                msg.setStyleSheet(
                    "QMessageBox { background-color: #120c18; color: white; }"
                    " QLabel { color: white; }"
                    " QPushButton { background-color: #2b1b3d; color: white; padding: 5px 15px; border: 1px solid #c9a444; border-radius: 4px; }"
                    " QPushButton:hover { background-color: #5c3285; }"
                )
                msg.exec_()
                
                if msg.clickedButton() == btn_open and log_path:
                    folder_path = os.path.dirname(log_path)
                    QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))
        except Exception as e:
            logger.error(f"Erro ao verificar marcador de crash: {e}")
