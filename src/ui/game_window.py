import os
import time
import json
from PyQt5.QtCore import Qt, QUrl, QSettings, QTimer, QPoint, QCoreApplication, QEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox, QShortcut, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile, QWebEnginePage
from PyQt5.QtGui import QColor, QFont, QCursor, QMouseEvent, QPixmap, QIcon, QPainter, QKeySequence

from src.core.logger import get_logger
from src.core.config import get_cache_dir, get_shared_cache_dir, LOGIN_JS_SCRIPT, BRIGHT_COLORS, resource_path
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
        
        icon_path = resource_path("bacon_knight.ico")
        app_icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()
        self.setWindowIcon(app_icon)
        
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(app_icon)
        tray_menu = QMenu()
        restore_action = QAction("Restaurar", self)
        restore_action.triggered.connect(self.restore_from_tray)
        quit_action = QAction("Fechar Conta", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)

        self.idle_timer = QTimer(self)
        self.idle_timer.timeout.connect(self.hide_to_tray)
        self.idle_timer.start(90000)
        
        self.shortcut_hide = QShortcut(QKeySequence("Ctrl+Shift+A"), self)
        self.shortcut_hide.activated.connect(self.hide_to_tray)
        
        self.is_recording_macro = False
        self.recorded_macro_events = []
        self.macro_start_time = 0
        self.shortcut_record = QShortcut(QKeySequence("F7"), self)
        self.shortcut_record.activated.connect(self.toggle_record_macro)
        self.shortcut_play = QShortcut(QKeySequence("F8"), self)
        self.shortcut_play.activated.connect(self.play_custom_macro)
        
        self.installEventFilter(self)
        
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
        self.profile.setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")
        self.profile.setHttpAcceptLanguage("pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7")
        
        if enable_cache:
            cache_dir = get_cache_dir(safe_email)
            shared_cache_dir = get_shared_cache_dir()
            self.profile.setCachePath(shared_cache_dir)
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
        self.setup_linux_frameless()
        self.browser.loadFinished.connect(self.inject_login)
        
        logger.info(f"[{email}] Conectando no servidor: {server_url}")
        self.browser.setUrl(QUrl(server_url))
        
        try:
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
            
            proxy = self.browser.focusProxy()
            if proxy:
                proxy.installEventFilter(self)

    def nativeEvent(self, eventType, message):
        handled, result = self.frameless_native_event(eventType, message)
        if handled:
            return True, result
        return super().nativeEvent(eventType, message)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick or reason == QSystemTrayIcon.Trigger:
            self.restore_from_tray()

    def hide_to_tray(self):
        self.hide()
        self.tray_icon.show()

    def restore_from_tray(self):
        self.showNormal()
        self.activateWindow()
        self.tray_icon.hide()
        self.idle_timer.start(90000)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                QTimer.singleShot(0, self.hide_to_tray)
                event.ignore()
                return
            elif self.isMaximized():
                self.main_card.setStyleSheet(f"#MainCard {{ background-color: {self.bg_color}; border-radius: 0px; border: none; }}")
            else:
                self.main_card.setStyleSheet(f"#MainCard {{ background-color: {self.bg_color}; border-radius: 10px; border: 1px solid #351554; }}")
        super().changeEvent(event)

    def eventFilter(self, obj, event):
        if self.linux_event_filter(obj, event):
            return True
        if event.type() in (QEvent.MouseMove, QEvent.MouseButtonPress, QEvent.KeyPress):
            self.idle_timer.start(90000)
            
        if self.is_recording_macro:
            if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonRelease, QEvent.KeyPress, QEvent.KeyRelease):
                elapsed = time.time() - self.macro_start_time
                event_data = None
                
                if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonRelease):
                    event_data = {
                        'type': event.type(),
                        'pos': event.pos(),
                        'button': event.button(),
                        'modifiers': event.modifiers()
                    }
                elif event.type() in (QEvent.KeyPress, QEvent.KeyRelease):
                    event_data = {
                        'type': event.type(),
                        'key': event.key(),
                        'modifiers': event.modifiers(),
                        'text': event.text(),
                        'autorepeat': event.isAutoRepeat(),
                        'count': event.count()
                    }
                    
                if event_data:
                    self.recorded_macro_events.append((elapsed, event_data))
                    
        return super().eventFilter(obj, event)

    def toggle_record_macro(self):
        if not self.is_recording_macro:
            self.is_recording_macro = True
            self.recorded_macro_events = []
            self.macro_start_time = time.time()
            self.title_bar.title.setText("🔴 GRAVANDO MACRO... (F7 para parar)")
        else:
            self.is_recording_macro = False
            self.title_bar.title.setText(f"✅ MACRO SALVO! ({len(self.recorded_macro_events)} eventos)")
            QTimer.singleShot(2000, lambda: self.title_bar.title.setText(f"Legend Online - Jogando como: {self.nick or self.email}"))

    def play_custom_macro(self):
        if not self.recorded_macro_events:
            return
        self.stop_macros()
        self.macro_type = 'custom'
        self.title_bar.title.setText("▶️ TOCANDO MACRO... (F4 para parar)")
        target_widget = self.browser.focusProxy() if self.browser.focusProxy() else self.browser
        params = {'queue': self.recorded_macro_events}
        self.macro_worker = MacroWorker(target_widget, 'custom', params)
        self.macro_worker.status_update.connect(self.title_bar.title.setText)
        self.macro_worker.finished.connect(self.stop_macros)
        self.macro_worker.start()

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
                if hasattr(self, 'browser') and self.browser: self.browser.deleteLater()
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
                if hasattr(self, 'browser') and self.browser: self.browser.deleteLater()
            except Exception as e:
                logger.error(f"Erro ao limpar: {e}")
            event.accept()
        elif dialog.result_action == "relog":
            self.relog()
            event.ignore()
        else:
            event.ignore()
