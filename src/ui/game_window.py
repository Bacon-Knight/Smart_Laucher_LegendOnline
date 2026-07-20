import os
import time
import json
import urllib.request
from PyQt5.QtCore import Qt, QUrl, QSettings, QTimer, QPoint, QCoreApplication, QEvent, QRect
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox, QShortcut, QSystemTrayIcon, QMenu, QAction, QInputDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile, QWebEnginePage
from PyQt5.QtGui import QColor, QFont, QCursor, QMouseEvent, QPixmap, QIcon, QPainter, QKeySequence
from PyQt5.QtCore import pyqtSignal, QThread

from src.core.logger import get_logger, mask_email
from src.core.config import get_cache_dir, get_shared_cache_dir, LOGIN_JS_SCRIPT, BRIGHT_COLORS, resource_path
from src.core.macros import MacroWorker
from src.ui.components.frameless import FramelessWindowMixin
from src.ui.components.title_bar import CustomTitleBar
from src.ui.components.dialogs import ImageViewerDialog, CustomCloseDialog
from src.ui.components.floating_macro import FloatingMacroPanel


class PingWorker(QThread):
    """Mede o ping HTTP ao servidor em background sem travar a UI."""
    result = pyqtSignal(int)   # latencia em ms, -1 = falha

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            start = time.time()
            req = urllib.request.Request(self.url, method="HEAD")
            urllib.request.urlopen(req, timeout=5)
            ms = int((time.time() - start) * 1000)
            self.result.emit(ms)
        except Exception:
            self.result.emit(-1)


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
        self.shortcut_config_autoluta = QShortcut(QKeySequence("Shift+F5"), self)
        self.shortcut_config_autoluta.activated.connect(self.configure_autoluta_sequence)

        self.shortcut_fullscreen = QShortcut(QKeySequence("F11"), self)
        self.shortcut_fullscreen.activated.connect(self.toggle_fullscreen)
        self.shortcut_relog = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcut_relog.activated.connect(self.fast_relog)

        # Carrega sequência salva de teclas para o Auto-Luta
        self.autoluta_sequence = []
        _saved_seq = QSettings("CustomLauncher", "LegendOnline").value(
            f"autoluta_seq_{email}", ""
        )
        if _saved_seq:
            self.autoluta_sequence = self.parse_key_sequence(_saved_seq)

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
            logger.info(f"[{mask_email(email)}] Cache compartilhado: {shared_cache_dir}")
            logger.info(f"[{mask_email(email)}] Storage isolado: {cache_dir}")
        else:
            self.profile.setHttpCacheType(QWebEngineProfile.NoCache)
            
        self.page = QWebEnginePage(self.profile, self.browser)
        self.page.setAudioMuted(self.is_muted)
        self.browser.setPage(self.page)
        
        self.title_bar.btn_mute.setText("🔇" if self.is_muted else "🔊")
        
        self.enable_windows_snap()
        self.setup_linux_frameless()
        self.browser.loadFinished.connect(self.inject_login)
        
        logger.info(f"[{mask_email(email)}] Conectando no servidor: {server_url}")
        self.browser.setUrl(QUrl(server_url))
        
        try:
            with open(resource_path("style.qss"), "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            logger.error(f"Failed to load style: {e}")

        # Ping ao servidor — atualiza a cada 30s
        self.ping_worker = None
        self.ping_timer = QTimer(self)
        self.ping_timer.timeout.connect(self._run_ping)
        self.ping_timer.start(30000)
        QTimer.singleShot(2000, self._run_ping)  # primeira leitura após 2s

        # Painel flutuante de macros
        self.floating_panel = FloatingMacroPanel(self)

    def _run_ping(self):
        if self.ping_worker is not None:
            try:
                if self.ping_worker.isRunning():
                    return
            except RuntimeError:
                self.ping_worker = None

        self.ping_worker = PingWorker(self.server_url)
        self.ping_worker.result.connect(self._on_ping_result)
        self.ping_worker.finished.connect(self._on_ping_finished)
        self.ping_worker.start()

    def _on_ping_finished(self):
        if self.ping_worker is not None:
            try:
                self.ping_worker.deleteLater()
            except RuntimeError:
                pass
            self.ping_worker = None

    def _on_ping_result(self, ms):
        if ms < 0:
            icon, color, tip = "🟥", "#ff4d4d", "Servidor inacessível"
        elif ms < 100:
            icon, color, tip = "🟢", "#4dff88", f"Ping excelente: {ms}ms"
        elif ms < 300:
            icon, color, tip = "🟡", "#ffcc00", f"Ping ok: {ms}ms"
        else:
            icon, color, tip = "🟠", "#ff9900", f"Ping alto: {ms}ms"

        label = self.title_bar.ping_label
        label.setText(f"{icon} {ms if ms >= 0 else '??'}ms")
        label.setStyleSheet(f"color: {color}; font-size: 10px; padding: 0 4px;")
        label.setToolTip(tip)

    def toggle_floating_panel(self):
        """Abre ou fecha o painel flutuante de macros."""
        if self.floating_panel.isVisible():
            self.floating_panel.hide()
        else:
            # Posiciona próximo ao botão ⚡ da title bar na primeira abertura
            if not self.floating_panel.pos().x():
                tb_global = self.title_bar.mapToGlobal(self.title_bar.rect().bottomLeft())
                self.floating_panel.move(tb_global.x() + 20, tb_global.y() + 4)
            self.floating_panel.show()
            self.floating_panel.raise_()

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
        if self.autoluta_active:
            # Desligar
            self.autoluta_active = False
            self.timer_autoluta.stop()
            self.title_bar.title.setText(f"Legend Online - Jogando como: {self.nick or self.email}")
            return

        # Ligar: pede sequência se não estiver configurada
        if not self.autoluta_sequence:
            if not self.configure_autoluta_sequence():
                return  # Usuário cancelou

        self.autoluta_active = True
        seq_text = " ".join(t for _, t in self.autoluta_sequence)
        self.title_bar.title.setText(f"⚔️ Auto Luta: ON [{seq_text}] (F5 para desligar, Shift+F5 reconfigurar)")
        self.timer_autoluta.start(2000)

    def configure_autoluta_sequence(self):
        """Abre dialog para configurar a sequência de teclas do Auto-Luta. Retorna True se confirmado."""
        settings = QSettings("CustomLauncher", "LegendOnline")
        current = settings.value(f"autoluta_seq_{self.email}", "1 2 3")

        text, ok = QInputDialog.getText(
            self,
            "⚔️ Configurar Auto-Luta",
            "Digite a sequência de teclas separadas por espaço:\n"
            "Ex:  1 2 3 4 5     ou     1 s 2 q\n"
            "Teclas suportadas: 0-9, a-z, space, enter",
            text=current
        )
        if not ok:
            return False

        seq = self.parse_key_sequence(text.strip())
        if not seq:
            QMessageBox.warning(self, "Sequência Inválida",
                "Nenhuma tecla reconhecida.\nUse dígitos (0-9), letras (a-z), 'space' ou 'enter'.")
            return False

        self.autoluta_sequence = seq
        settings.setValue(f"autoluta_seq_{self.email}", text.strip())
        return True

    def parse_key_sequence(self, seq_text):
        """Converte string de teclas ('1 2 s q') em lista de (QtKey, texto)."""
        KEY_MAP = {
            '0': (Qt.Key_0, '0'), '1': (Qt.Key_1, '1'), '2': (Qt.Key_2, '2'),
            '3': (Qt.Key_3, '3'), '4': (Qt.Key_4, '4'), '5': (Qt.Key_5, '5'),
            '6': (Qt.Key_6, '6'), '7': (Qt.Key_7, '7'), '8': (Qt.Key_8, '8'),
            '9': (Qt.Key_9, '9'),
            'a': (Qt.Key_A, 'a'), 'b': (Qt.Key_B, 'b'), 'c': (Qt.Key_C, 'c'),
            'd': (Qt.Key_D, 'd'), 'e': (Qt.Key_E, 'e'), 'f': (Qt.Key_F, 'f'),
            'g': (Qt.Key_G, 'g'), 'h': (Qt.Key_H, 'h'), 'i': (Qt.Key_I, 'i'),
            'j': (Qt.Key_J, 'j'), 'k': (Qt.Key_K, 'k'), 'l': (Qt.Key_L, 'l'),
            'm': (Qt.Key_M, 'm'), 'n': (Qt.Key_N, 'n'), 'o': (Qt.Key_O, 'o'),
            'p': (Qt.Key_P, 'p'), 'q': (Qt.Key_Q, 'q'), 'r': (Qt.Key_R, 'r'),
            's': (Qt.Key_S, 's'), 't': (Qt.Key_T, 't'), 'u': (Qt.Key_U, 'u'),
            'v': (Qt.Key_V, 'v'), 'w': (Qt.Key_W, 'w'), 'x': (Qt.Key_X, 'x'),
            'y': (Qt.Key_Y, 'y'), 'z': (Qt.Key_Z, 'z'),
            'space': (Qt.Key_Space, ' '), 'enter': (Qt.Key_Return, '\n'),
        }
        parts = seq_text.replace(',', ' ').split()
        return [KEY_MAP[p.lower()] for p in parts if p.lower() in KEY_MAP]

    def check_autoluta(self):
        if self.macro_worker and self.macro_worker.isRunning():
            return

        try:
            bw, bh = self.browser.width(), self.browser.height()
            if bw <= 0 or bh <= 0:
                return

            # Captura apenas o retalho do canto inferior esquerdo (HUD do orbe de vida) em vez da tela inteira
            crop_rect = QRect(int(bw * 0.03), int(bh * 0.82), int(bw * 0.13), int(bh * 0.18))
            pixmap = self.browser.grab(crop_rect)
            img = pixmap.toImage()
            width, height = img.width(), img.height()

            in_combat = False
            red_pixels = 0
            for y in range(0, height, 4):
                for x in range(0, width, 4):
                    c = QColor(img.pixel(x, y))
                    if c.red() > 170 and c.green() < 70 and c.blue() < 70:
                        red_pixels += 1
                        if red_pixels >= 5:   # threshold: 5 pixels vermelhos confirmam o orbe
                            in_combat = True
                            break
                if in_combat:
                    break

            if in_combat and self.autoluta_sequence:
                target_widget = self.browser.focusProxy() if self.browser.focusProxy() else self.browser
                params = {'sequence': self.autoluta_sequence}
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

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        if hasattr(self, 'page') and self.page is not None:
            try:
                self.page.setAudioMuted(self.is_muted)
            except RuntimeError:
                pass
        self.title_bar.btn_mute.setText("🔇" if self.is_muted else "🔊")

    def open_image_viewer(self, rel_folder_path):
        from src.core.config import resource_path
        abs_path = resource_path(rel_folder_path)
        viewer = ImageViewerDialog(abs_path, self)
        viewer.exec_()

    def relog(self):
        logger.info(f"[{mask_email(self.email)}] Recarregando a página...")
        self.browser.reload()



    def fast_relog(self):
        import gc
        logger.info(f"[{mask_email(self.email)}] Limpando Memória (Fast Relog)...")
        # Descarrega o jogo da memória para liberar RAM instantaneamente
        self.browser.setUrl(QUrl("about:blank"))
        gc.collect()
        # Recarrega o portal após meio segundo para pegar um token novo
        QTimer.singleShot(500, lambda: self.browser.setUrl(QUrl(self.server_url)))


    def clear_cache(self):
        logger.info(f"[{mask_email(self.email)}] Limpando cache do navegador...")
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
            now = time.time()
            if not hasattr(self, '_last_idle_reset') or (now - self._last_idle_reset) > 10.0:
                self._last_idle_reset = now
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
        if not getattr(self, '_is_closing', False) and hasattr(self, 'page') and self.page is not None:
            try:
                self.page.setZoomFactor(zoom_factor)
            except RuntimeError:
                pass
        super().resizeEvent(event)

    def closeEvent(self, event):
        if getattr(self, 'force_close', False):
            self._is_closing = True
            logger.info(f"[{mask_email(self.email)}] Limpando recursos de memória e fechando (Forçado)...")
            try:
                if hasattr(self, 'page') and self.page is not None:
                    self.page.deleteLater()
                    self.page = None
                if hasattr(self, 'profile') and self.profile is not None:
                    self.profile.deleteLater()
                    self.profile = None
                if hasattr(self, 'browser') and self.browser is not None:
                    self.browser.deleteLater()
                    self.browser = None
            except Exception as e:
                logger.error(f"Erro ao limpar forçado: {e}")
            event.accept()
            return
            
        dialog = CustomCloseDialog(self)
        dialog.exec_()
        
        if dialog.result_action == "close":
            self._is_closing = True
            logger.info(f"[{mask_email(self.email)}] Limpando recursos de memória e fechando...")
            try:
                if hasattr(self, 'page') and self.page is not None:
                    self.page.deleteLater()
                    self.page = None
                if hasattr(self, 'profile') and self.profile is not None:
                    self.profile.deleteLater()
                    self.profile = None
                if hasattr(self, 'browser') and self.browser is not None:
                    self.browser.deleteLater()
                    self.browser = None
            except Exception as e:
                logger.error(f"Erro ao limpar: {e}")
            event.accept()
        elif dialog.result_action == "relog":
            self.relog()
            event.ignore()
        else:
            event.ignore()

