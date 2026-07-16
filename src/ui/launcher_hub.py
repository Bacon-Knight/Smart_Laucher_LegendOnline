import json
import ctypes
from ctypes import wintypes
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QSystemTrayIcon, QMenu, QAction, QMessageBox, QGraphicsDropShadowEffect, QStyle, QApplication, QShortcut
from PyQt5.QtCore import Qt, QSettings, QPoint, QObject, QTimer
from PyQt5.QtGui import QColor, QKeySequence

from src.core.logger import get_logger
from src.core.config import resource_path, COLOR_MAP, COLOR_ORDER
from src.ui.components.title_bar import CustomTitleBar
from src.ui.game_window import GameWindow

logger = get_logger("LauncherHub")

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("dwTime", wintypes.DWORD)
    ]

def get_system_idle_time_ms():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        return ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return 0

class AFKManager(QObject):
    def __init__(self, hub, timeout_mins=2):
        super().__init__()
        self.hub = hub
        self.timeout_ms = timeout_mins * 60 * 1000
        self.inactive_ms = 0
        
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_state)
        self.check_timer.start(5000) # Checa a cada 5 segundos

    def check_state(self):
        app = QApplication.instance()
        is_app_focused = app.activeWindow() is not None
        sys_idle = get_system_idle_time_ms()
        
        if sys_idle >= self.timeout_ms:
            self.hub.hide_to_tray()
            return
            
        if not is_app_focused:
            self.inactive_ms += 5000
            if self.inactive_ms >= self.timeout_ms:
                self.hub.hide_to_tray()
        else:
            self.inactive_ms = 0

class LauncherHub(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 1100, 80)
        
        self.settings = QSettings("CustomLauncher", "LegendOnline")
        self.game_windows = []
        
        self.boss_hidden = False
        self.setup_tray()
        
        self.shortcut_boss = QShortcut(QKeySequence("Ctrl+Shift+A"), self)
        self.shortcut_boss.setContext(Qt.ApplicationShortcut)
        self.shortcut_boss.activated.connect(self.toggle_boss_key)
        
        # Reativando o AFKManager a pedido do usuário (esconde o app automaticamente)
        self.afk_manager = AFKManager(self, timeout_mins=2)
        
        self.init_ui()
        self.load_styles()

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        tray_menu = QMenu()
        tray_menu.setStyleSheet("QMenu { background-color: #2b1b3d; color: white; border: 1px solid #c9a444; } QMenu::item:selected { background-color: #c9a444; color: black; }")
        
        action_show = QAction("Mostrar Hub", self)
        action_show.triggered.connect(lambda: [self.showNormal(), self.activateWindow()])
        tray_menu.addAction(action_show)
        
        action_show_all = QAction("Mostrar Todos os Jogos", self)
        action_show_all.triggered.connect(self.show_all_games)
        tray_menu.addAction(action_show_all)
        
        action_close_all = QAction("Encerrar todas as contas", self)
        action_close_all.triggered.connect(self.close_all_games)
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
            self.boss_hidden = False
            self.showNormal()
            self.activateWindow()
            self.show_all_games()

    def toggle_boss_key(self):
        if self.boss_hidden:
            self.show_from_tray()
        else:
            self.hide_to_tray()
            
    def hide_to_tray(self):
        if not self.boss_hidden:
            logger.info("Modo Privacidade/AFK Ativado: Escondendo janelas.")
            self.boss_hidden = True
            self.hide()
            for gw in self.game_windows:
                try: gw.hide()
                except: pass

    def show_from_tray(self):
        self.boss_hidden = False
        self.showNormal()
        self.activateWindow()
        self.show_all_games()
            
    def show_all_games(self):
        for gw in self.game_windows:
            try:
                gw.showNormal()
                gw.activateWindow()
                gw.raise_()
            except:
                pass

    def close_all_games(self):
        for gw in self.game_windows:
            try: gw.close()
            except: pass
        self.game_windows.clear()
        
    def closeEvent(self, event):
        self.close_all_games()
        event.accept()

    def load_styles(self):
        try:
            qss_path = resource_path("style.qss")
            with open(qss_path, "r") as f:
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
        
        self.saved_accounts = {}
        try:
            accounts_json = self.settings.value("saved_accounts", "{}")
            self.saved_accounts = json.loads(accounts_json)
            for k, v in self.saved_accounts.items():
                if isinstance(v, str):
                    self.saved_accounts[k] = {"password": v, "server": "1252", "nick": ""}
        except:
            self.saved_accounts = {}
            
        email_container = QWidget()
        email_layout = QHBoxLayout(email_container)
        email_layout.setContentsMargins(0, 0, 0, 0)
        email_layout.setSpacing(5)
        
        self.input_email = QComboBox()
        self.input_email.setEditable(True)
        self.input_email.lineEdit().setPlaceholderText("E-mail da Conta")
        self.input_email.addItems(list(self.saved_accounts.keys()))
        self.input_email.setCurrentText(self.settings.value("last_email", ""))
        self.input_email.currentTextChanged.connect(self.on_email_changed)
        self.input_email.setMinimumWidth(200)
        
        self.btn_accounts = QPushButton("📋")
        self.btn_accounts.setObjectName("TogglePassBtn") 
        self.btn_accounts.setFixedSize(30, 30)
        self.btn_accounts.setToolTip("Contas Salvas")
        self.btn_accounts.clicked.connect(self.show_accounts_menu)
        
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
        self.input_server.setText(current_acc.get("server", self.settings.value("server", "1252")))
        self.input_server.setFixedWidth(100)
        
        self.input_nick = QLineEdit()
        self.input_nick.setPlaceholderText("Nick")
        self.input_nick.setText(current_acc.get("nick", ""))
        self.input_nick.setFixedWidth(120)
        
        self.input_color = QComboBox()
        self.input_color.hide()
        
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
        content_layout.addWidget(self.input_color)
        
        card_layout.addWidget(content_widget)

    def show_accounts_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background-color: #2b1b3d; color: white; border: 1px solid #c9a444; } QMenu::item:selected { background-color: #c9a444; color: black; }")
        
        if not self.saved_accounts:
            action = QAction("Nenhuma conta salva.", self)
            action.setEnabled(False)
            menu.addAction(action)
        else:
            for email, data in self.saved_accounts.items():
                server = data.get("server", "N/A")
                nick = data.get("nick", "")
                display_text = f"[S{server}] {nick} - {email}" if nick else f"[S{server}] {email}"
                
                acc_menu = menu.addMenu(display_text)
                
                action_load = QAction("Selecionar", self)
                action_load.triggered.connect(lambda checked, e=email: self.input_email.setCurrentText(e))
                acc_menu.addAction(action_load)
                
                action_del = QAction("Excluir Conta", self)
                action_del.triggered.connect(lambda checked, e=email: self.delete_account(e))
                acc_menu.addAction(action_del)
                
        menu.exec_(self.btn_accounts.mapToGlobal(QPoint(0, self.btn_accounts.height())))
        
    def delete_account(self, email):
        reply = QMessageBox.question(self, "Excluir Conta", f"Tem certeza que deseja excluir a conta {email}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if email in self.saved_accounts:
                del self.saved_accounts[email]
                self.settings.setValue("saved_accounts", json.dumps(self.saved_accounts))
                if self.input_email.currentText() == email:
                    self.input_email.setCurrentText("")
                    self.input_password.setText("")
                    self.input_server.setText("")
                    self.input_nick.setText("")
                
                self.input_email.clear()
                self.input_email.addItems(list(self.saved_accounts.keys()))
                QMessageBox.information(self, "Excluída", "Conta excluída com sucesso.")

    def on_email_changed(self, text):
        if text in self.saved_accounts:
            acc = self.saved_accounts[text]
            self.input_password.setText(acc.get("password", ""))
            self.input_server.setText(acc.get("server", ""))
            self.input_nick.setText(acc.get("nick", ""))
            self.input_color.setCurrentText(acc.get("color", "Padrão"))
            
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
        
        if not email:
            QMessageBox.warning(self, "Aviso de Autenticação", "Por favor, digite ou selecione um e-mail.")
            return
            
        if not server_num:
            QMessageBox.warning(self, "Aviso de Servidor", "O número do servidor não pode ficar vazio.")
            return
        
        if email:
            self.saved_accounts[email] = {
                "password": password,
                "server": server_num,
                "nick": self.input_nick.text().strip(),
                "color": self.input_color.currentText()
            }
            self.settings.setValue("saved_accounts", json.dumps(self.saved_accounts))
            self.settings.setValue("last_email", email)
            
        self.settings.setValue("server", server_num)
        
        enable_cache = self.settings.value("enable_cache", True, type=bool)
        
        url_completa = f"https://lobr.creaction-network.com/serverlist/s{server_num}"
        nick = self.input_nick.text().strip()
        
        color_name = COLOR_ORDER[len(self.game_windows) % len(COLOR_ORDER)]
        bg_color = COLOR_MAP.get(color_name, "#120c18")
        
        gw = GameWindow(email, password, url_completa, enable_cache, nick, bg_color)
        self.game_windows.append(gw)
        gw.show()
