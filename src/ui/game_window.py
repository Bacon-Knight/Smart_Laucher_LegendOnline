import os
import json
from PyQt5.QtCore import Qt, QUrl, QSettings, QTimer, QPoint, QCoreApplication, QEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox, QShortcut
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile, QWebEnginePage
from PyQt5.QtGui import QColor, QFont, QCursor, QMouseEvent, QPixmap, QIcon, QPainter, QKeySequence

from src.core.logger import get_logger
from src.core.config import get_cache_dir, LOGIN_JS_SCRIPT, BRIGHT_COLORS
from src.core.macros import MacroWorker
from src.ui.components.frameless import FramelessWindowMixin
from src.ui.components.title_bar import CustomTitleBar
from src.ui.components.dialogs import ImageViewerDialog, CustomCloseDialog

logger = get_logger("GameWindow")

class GameWindow(QMainWindow, FramelessWindowMixin):
    def __init__(self, email, password, server_url, enable_cache, nick, bg_color):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        
        self.email = email
        self.password = password
        self.server_url = server_url
        self.nick = nick
        self.is_muted = True
        self.bg_color = bg_color
        
        self.setGeometry(150, 150, 1040, 800)
        
        self.main_card = QWidget()
        self.main_card.setObjectName("MainCard")
        self.setCentralWidget(self.main_card)
        self.main_card.setStyleSheet(f"#MainCard {{ background-color: {self.bg_color}; border-radius: 10px; border: 1px solid #351554; }}")
        
        main_layout = QVBoxLayout(self.main_card)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.title_bar = CustomTitleBar(self, is_game_window=True)
        display_name = self.nick if self.nick else self.email
        self.setWindowTitle(display_name)
        self.title_bar.title.setText(f"Legend Online - Jogando como: {display_name}")
        main_layout.addWidget(self.title_bar)
        
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        bright_color = BRIGHT_COLORS.get(self.bg_color, "#cccccc")
        painter.setBrush(QColor(bright_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(2, 2, 28, 28)
        painter.end()
        self.setWindowIcon(QIcon(pixmap))
        
        self.browser = QWebEngineView()
        main_layout.addWidget(self.browser)
        
        self.macro_worker = None
        self.timer_countdown = QTimer(self)
        self.timer_countdown.timeout.connect(self.update_countdown)
        self.countdown_val = 0
        self.macro_type = None
        
        self.shortcut_stop = QShortcut(QKeySequence("F4"), self)
        self.shortcut_stop.activated.connect(self.stop_macros)
        
        self.autoluta_active = False
        self.timer_autoluta = QTimer(self)
        self.timer_autoluta.timeout.connect(self.check_autoluta)
        
        self.shortcut_autoluta = QShortcut(QKeySequence("F5"), self)
        self.shortcut_autoluta.activated.connect(self.toggle_autoluta)
        
        safe_email = "".join(c for c in email if c.isalnum() or c in ('@', '.', '_')).replace('@', '_')
        if not safe_email:
            safe_email = "default_profile"
            
        self.profile = QWebEngineProfile(safe_email, self.browser)
        self.profile.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        
        if enable_cache:
            cache_dir = get_cache_dir(safe_email)
            self.profile.setCachePath(cache_dir)
            self.profile.setPersistentStoragePath(cache_dir)
            self.profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
            self.profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
            self.profile.setHttpCacheMaximumSize(1024 * 1024 * 1024)
        else:
            self.profile.setHttpCacheType(QWebEngineProfile.NoCache)
            
        self.page = QWebEnginePage(self.profile, self.browser)
        self.page.setAudioMuted(self.is_muted)
        self.browser.setPage(self.page)
        
        self.title_bar.btn_mute.setText("🔇" if self.is_muted else "🔊")
        
        self.enable_windows_snap()
        self.browser.loadFinished.connect(self.inject_login)
        
        logger.info(f"[{email}] Conectando no servidor: {server_url}")
        self.browser.setUrl(QUrl(server_url))
        
        try:
            from src.core.config import resource_path
            with open(resource_path("style.qss"), "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            logger.error(f"Failed to load style: {e}")

    def start_autoclicker(self):
        self.stop_macros()
        self.macro_type = 'autoclick'
        self.countdown_val = 10
        self.title_bar.title.setText(f"🎯 Posicione o mouse onde deseja clicar em: {self.countdown_val}s")
        self.timer_countdown.start(1000)

    def start_formacao_magica(self):
        self.stop_macros()
        self.macro_type = 'formacao'
        self.countdown_val = 5
        self.title_bar.title.setText(f"🧙‍♂️ Formação: Posicione o mouse no CENTRO (X Vermelho) em: {self.countdown_val}s")
        self.timer_countdown.start(1000)

    def update_countdown(self):
        self.countdown_val -= 1
        if self.countdown_val > 0:
            if self.macro_type == 'autoclick':
                self.title_bar.title.setText(f"🎯 Posicione o mouse onde deseja clicar em: {self.countdown_val}s")
            else:
                self.title_bar.title.setText(f"🧙‍♂️ Formação: Posicione o mouse no CENTRO (X Vermelho) em: {self.countdown_val}s")
        else:
            self.timer_countdown.stop()
            center_pos = self.browser.mapFromGlobal(QCursor.pos())
            
            target_widget = self.browser.focusProxy() if self.browser.focusProxy() else self.browser
            
            if self.macro_type == 'autoclick':
                params = {'pos': center_pos, 'interval': 1.0}
                self.macro_worker = MacroWorker(target_widget, 'autoclick', params)
            else:
                queue = self.calculate_formacao(center_pos)
                params = {'queue': queue, 'combat_time': 5000}
                self.macro_worker = MacroWorker(target_widget, 'formacao', params)
                
            self.macro_worker.status_update.connect(self.title_bar.title.setText)
            self.macro_worker.finished.connect(self.stop_macros)
            self.macro_worker.start()

    def toggle_autoluta(self):
        self.autoluta_active = not self.autoluta_active
        if self.autoluta_active:
            self.title_bar.title.setText("⚔️ Auto Luta: ON (F5 para desligar, Lendo Tela...)")
            self.timer_autoluta.start(2000)
        else:
            self.timer_autoluta.stop()
            self.title_bar.title.setText(f"Legend Online - Jogando como: {self.nick or self.email}")

    def check_autoluta(self):
        if self.macro_worker and self.macro_worker.isRunning():
            return
            
        try:
            pixmap = self.browser.grab()
            img = pixmap.toImage()
            width, height = img.width(), img.height()
            
            found = False
            target_x, target_y = 0, 0
            
            start_x = int(width * 0.8)
            start_y = int(height * 0.8)
            for y in range(start_y, height, 5):
                for x in range(start_x, width, 5):
                    color = QColor(img.pixel(x, y))
                    if color.red() > 200 and color.green() > 160 and color.blue() < 80:
                        found = True
                        target_x, target_y = x, y
                        break
                if found: break
                
            if found:
                target_widget = self.browser.focusProxy() if self.browser.focusProxy() else self.browser
                params = {'pos': QPoint(target_x, target_y)}
                self.macro_worker = MacroWorker(target_widget, 'autoluta', params)
                self.macro_worker.status_update.connect(self.title_bar.title.setText)
                self.macro_worker.finished.connect(self.stop_macros)
                self.macro_worker.start()
                self.timer_autoluta.stop()
        except Exception as e:
            logger.error(f"Erro no Auto Luta: {e}")

    def calculate_formacao(self, center_pos):
        base_w, base_h = 104, 52
        win_w, win_h = 1040, 800
        zoom_w = self.width() / win_w
        zoom_h = self.height() / win_h
        zoom_factor = min(zoom_w, zoom_h)
        w = base_w * zoom_factor
        h = base_h * zoom_factor
        cx, cy = center_pos.x(), center_pos.y()
        
        priorities = {1: [], 2: []}
        for y in range(-2, 3):
            for x in range(-2, 3):
                prio = 2 if (x == 0 and y == 0) else 1
                screen_x = cx + (x - y) * (w / 2)
                screen_y = cy + (x + y) * (h / 2)
                priorities[prio].append(QPoint(int(screen_x), int(screen_y)))
                
        return priorities[1] + priorities[2]

    def stop_macros(self):
        self.timer_countdown.stop()
        if self.macro_worker and self.macro_worker.isRunning():
            self.macro_worker.stop()
            self.macro_worker.wait()
            self.macro_worker = None
            
        display_name = self.nick if self.nick else self.email
        if getattr(self, 'autoluta_active', False):
            self.title_bar.title.setText(f"⚔️ Auto Luta: ON (F5 para desligar, Lendo Tela...)")
            self.timer_autoluta.start(2000)
        else:
            self.title_bar.title.setText(f"Legend Online - Jogando como: {display_name}")

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        self.page.setAudioMuted(self.is_muted)
        self.title_bar.btn_mute.setText("🔇" if self.is_muted else "🔊")

    def open_image_viewer(self, rel_folder_path):
        from src.core.config import resource_path
        abs_path = resource_path(rel_folder_path)
        viewer = ImageViewerDialog(abs_path, self)
        viewer.exec_()

    def relog(self):
        logger.info(f"[{self.email}] Recarregando a página...")
        self.browser.reload()

    def clear_cache(self):
        logger.info(f"[{self.email}] Limpando cache do navegador...")
        self.profile.clearHttpCache()
        QMessageBox.information(self, "Cache", "Cache do navegador limpo com sucesso!")

    def inject_login(self, ok):
        if ok and self.email and self.password:
            js = LOGIN_JS_SCRIPT.format(email_json=json.dumps(self.email), password_json=json.dumps(self.password))
            self.page.runJavaScript(js)

    def nativeEvent(self, eventType, message):
        handled, result = self.frameless_native_event(eventType, message)
        if handled:
            return True, result
        return super().nativeEvent(eventType, message)

    def resizeEvent(self, event):
        base_width = 1040.0
        base_height = 800.0
        current_width = self.width()
        current_height = self.height()
        zoom_x = current_width / base_width
        zoom_y = current_height / base_height
        zoom_factor = min(zoom_x, zoom_y)
        if zoom_factor < 0.2:
            zoom_factor = 0.2
        self.page.setZoomFactor(zoom_factor)
        super().resizeEvent(event)

    def closeEvent(self, event):
        if getattr(self, 'force_close', False):
            logger.info(f"[{self.email}] Limpando recursos de memória e fechando (Forçado)...")
            try:
                if hasattr(self, 'page') and self.page: self.page.deleteLater()
                if hasattr(self, 'profile') and self.profile: self.profile.deleteLater()
            except Exception as e:
                logger.error(f"Erro ao limpar forçado: {e}")
            event.accept()
            return
            
        dialog = CustomCloseDialog(self)
        dialog.exec_()
        
        if dialog.result_action == "close":
            logger.info(f"[{self.email}] Limpando recursos de memória e fechando...")
            try:
                if hasattr(self, 'page') and self.page: self.page.deleteLater()
                if hasattr(self, 'profile') and self.profile: self.profile.deleteLater()
            except Exception as e:
                logger.error(f"Erro ao limpar: {e}")
            event.accept()
        elif dialog.result_action == "relog":
            self.relog()
            event.ignore()
        else:
            event.ignore()
