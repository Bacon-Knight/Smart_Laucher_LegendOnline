import sys
import os
import json
from PyQt5.QtCore import QUrl, QSettings, Qt, QPoint, QTimer, QCoreApplication, QEvent
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLineEdit, QPushButton, QLabel, QComboBox, 
                             QCheckBox, QFormLayout, QGroupBox, QMessageBox, QGraphicsDropShadowEffect, QDialog, QSizeGrip, QMenu, QShortcut, QAction, QInputDialog)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile, QWebEnginePage
from PyQt5.QtGui import QColor, QFont, QCursor, QMouseEvent, QKeySequence, QPixmap

def resource_path(relative_path):
    """ Pega o caminho absoluto, funcionando tanto em dev quanto num .exe do PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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
        
        # Barra superior customizada para o Pop-up
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
        
        # Visualizador
        self.image_label = QLabel("Nenhuma imagem encontrada na pasta.")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("color: white; font-size: 14px;")
        
        # Controles
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
            # Escala a imagem mantendo a proporção para caber em 760x540
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

    # Drag para a janela toda
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
        self.result_action = "cancel" # Pode ser "close", "relog" ou "cancel"
        
        layout = QVBoxLayout(self)
        
        # O Card Principal visível (dialog)
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

class CustomTitleBar(QWidget):
    def __init__(self, parent=None, is_game_window=False):
        super().__init__(parent)
        self.parent = parent
        self.is_game_window = is_game_window
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(15, 0, 10, 0)
        self.setFixedHeight(40)
        
        self.title = QLabel("Launcher By Bacon Knight")
        self.title.setObjectName("TitleLabel")
        self.layout.addWidget(self.title)
        self.layout.addStretch()
        
        # Utilitários apenas para a tela do jogo
        if self.is_game_window:
            self.btn_tools = QPushButton("🛠")
            self.btn_tools.setFixedSize(30, 30)
            self.btn_tools.setObjectName("TitleBtn")
            self.btn_tools.setToolTip("Ferramentas e Macros")
            
            # Adiciona o drop-down nativo invisível no botão, ou o custom QMenu
            self.tool_menu = QMenu(self.btn_tools)
            
            # Action: AutoClicker
            action_autoclick = QAction("Iniciar AutoClicker (F4)", self)
            action_autoclick.triggered.connect(self.parent.start_autoclicker)
            self.tool_menu.addAction(action_autoclick)
            
            # Action: Formação Mágica
            action_formacao = QAction("Formação Mágica (Macro 5x5)", self)
            action_formacao.triggered.connect(self.parent.start_formacao_magica)
            self.tool_menu.addAction(action_formacao)
            
            # Action: Plano de Crise
            action_crise = QAction("Plano de Crise", self)
            action_crise.triggered.connect(lambda: self.parent.open_image_viewer("Ferramentas/Planos de Crise"))
            self.tool_menu.addAction(action_crise)
            
            # Submenu: Minas
            menu_minas = self.tool_menu.addMenu("Minas ▶")
            
            action_minas_atual = QAction("Atual", self)
            action_minas_atual.triggered.connect(lambda: self.parent.open_image_viewer("Ferramentas/Planos de Mina/Atual"))
            menu_minas.addAction(action_minas_atual)
            
            action_minas_baixo = QAction("Baixo & Médio", self)
            action_minas_baixo.triggered.connect(lambda: self.parent.open_image_viewer("Ferramentas/Planos de Mina/Baixo & Médio"))
            menu_minas.addAction(action_minas_baixo)
            
            action_minas_grande = QAction("Grande", self)
            action_minas_grande.triggered.connect(lambda: self.parent.open_image_viewer("Ferramentas/Planos de Mina/Grande"))
            menu_minas.addAction(action_minas_grande)
            
            # Aplica CSS básico no menu
            self.tool_menu.setStyleSheet("QMenu { background-color: #2b1b3d; color: white; border: 1px solid #c9a444; } QMenu::item:selected { background-color: #c9a444; color: black; }")
            self.btn_tools.setMenu(self.tool_menu)
            
            self.btn_mute = QPushButton("🔊")
            self.btn_mute.setFixedSize(30, 30)
            self.btn_mute.setObjectName("TitleBtn")
            self.btn_mute.setToolTip("Mutar/Desmutar Som da Aba")
            self.btn_mute.clicked.connect(self.parent.toggle_mute)
            
            self.btn_relog = QPushButton("🔄")
            self.btn_relog.setFixedSize(30, 30)
            self.btn_relog.setObjectName("TitleBtn")
            self.btn_relog.setToolTip("Recarregar Página")
            self.btn_relog.clicked.connect(self.parent.relog)
            
            self.btn_cache = QPushButton("🧹")
            self.btn_cache.setFixedSize(30, 30)
            self.btn_cache.setObjectName("TitleBtn")
            self.btn_cache.setToolTip("Limpar Cache desta Conta")
            self.btn_cache.clicked.connect(self.parent.clear_cache)
            
            self.layout.addWidget(self.btn_tools)
            self.layout.addWidget(self.btn_mute)
            self.layout.addWidget(self.btn_relog)
            self.layout.addWidget(self.btn_cache)
            
            # Espaçador antes de fechar/minimizar
            spacer = QWidget()
            spacer.setFixedWidth(10)
            self.layout.addWidget(spacer)
        
        self.btn_minimize = QPushButton("—")
        self.btn_minimize.setFixedSize(30, 30)
        self.btn_minimize.setObjectName("TitleBtn")
        self.btn_minimize.clicked.connect(self.parent.showMinimized)
        
        self.btn_maximize = QPushButton("🗖")
        self.btn_maximize.setFixedSize(30, 30)
        self.btn_maximize.setObjectName("TitleBtn")
        self.btn_maximize.clicked.connect(self.toggle_maximize)
        
        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(30, 30)
        self.btn_close.setObjectName("TitleBtnClose")
        self.btn_close.clicked.connect(self.parent.close)
        
        self.layout.addWidget(self.btn_minimize)
        self.layout.addWidget(self.btn_maximize)
        self.layout.addWidget(self.btn_close)
        
        self.start_pos = None

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.btn_maximize.setText("🗖")
        else:
            self.parent.showMaximized()
            self.btn_maximize.setText("🗗")

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle_maximize()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.start_pos is not None and not self.parent.isMaximized():
            delta = event.globalPos() - self.start_pos
            self.parent.move(self.parent.pos() + delta)
            self.start_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.start_pos = None

class GameWindow(QMainWindow):
    def __init__(self, email, password, server_url, enable_cache=True):
        super().__init__()
        # Estilo Frameless Gamer (Sem Translucidez para não quebrar a GPU no background)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.email = email
        self.password = password
        self.server_url = server_url
        self.is_muted = False
        
        self.setGeometry(150, 150, 1040, 800)
        
        # Container principal sem margens e sem sombra para otimização máxima
        self.main_card = QWidget()
        self.main_card.setObjectName("MainCard")
        
        self.setCentralWidget(self.main_card)
        
        main_layout = QVBoxLayout(self.main_card)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Barra de Titulo (com os botões utilitários)
        self.title_bar = CustomTitleBar(self, is_game_window=True)
        self.title_bar.title.setText(f"Legend Online - Jogando como: {email}")
        main_layout.addWidget(self.title_bar)
        
        # O Browser
        self.browser = QWebEngineView()
        main_layout.addWidget(self.browser)
        
        # Macros e AutoClicker State
        self.autoclicker_pos = None
        self.autoclicker_active = False
        
        self.formacao_active = False
        self.formacao_queue = []
        self.formacao_combat_time = 5000
        
        self.countdown_val = 0
        self.macro_type = None # 'autoclick' ou 'formacao'
        
        self.timer_countdown = QTimer(self)
        self.timer_countdown.timeout.connect(self.update_countdown)
        
        self.timer_clicker = QTimer(self)
        self.timer_clicker.timeout.connect(self.perform_macro_step)
        
        # Atalho F4 Global na Janela para Parar
        self.shortcut_stop = QShortcut(QKeySequence("F4"), self)
        self.shortcut_stop.activated.connect(self.stop_macros)

        # Configurar Perfil Isolado
        safe_email = "".join(c for c in email if c.isalnum() or c in ('@', '.', '_')).replace('@', '_')
        if not safe_email:
            safe_email = "default_profile"
            
        self.profile = QWebEngineProfile(safe_email, self.browser)
        self.profile.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        
        if enable_cache:
            self.profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
            self.profile.setHttpCacheMaximumSize(1024 * 1024 * 1024)
        else:
            self.profile.setHttpCacheType(QWebEngineProfile.NoCache)
        
        self.page = QWebEnginePage(self.profile, self.browser)
        self.browser.setPage(self.page)

        self.browser.loadFinished.connect(self.inject_login)

        print(f"[{email}] Conectando no servidor: {server_url}")
        self.browser.setUrl(QUrl(server_url))
        
        # Carregar CSS
        try:
            with open("style.qss", "r") as f:
                self.setStyleSheet(f.read())
        except:
            pass

    def start_autoclicker(self):
        if self.autoclicker_active or self.formacao_active or self.timer_countdown.isActive():
            self.stop_macros()
            return
            
        self.macro_type = 'autoclick'
        self.countdown_val = 10
        self.title_bar.title.setText(f"🎯 Posicione o mouse onde deseja clicar em: {self.countdown_val}s")
        self.timer_countdown.start(1000)

    def start_formacao_magica(self):
        if self.autoclicker_active or self.formacao_active or self.timer_countdown.isActive():
            self.stop_macros()
            return
            
        tempo, ok = QInputDialog.getInt(self, "Formação Mágica", "Tempo médio de combate por monstro (segundos):", 5, 1, 60)
        if not ok: return
        
        self.formacao_combat_time = tempo * 1000
        self.macro_type = 'formacao'
        self.countdown_val = 10
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
            
            if self.macro_type == 'autoclick':
                self.autoclicker_pos = center_pos
                self.autoclicker_active = True
                self.title_bar.title.setText(f"🛑 AUTOCLICK ON - Pressione F4 para Parar")
                self.timer_clicker.start(1000) # Clica a cada 1 segundo
            else:
                self.calculate_formacao(center_pos)

    def calculate_formacao(self, center_pos):
        # Base tile size at 1.0 zoom
        base_w, base_h = 104, 52
        
        # Obter zoom atual
        win_w, win_h = 1040, 800
        zoom_w = self.width() / win_w
        zoom_h = self.height() / win_h
        zoom_factor = min(zoom_w, zoom_h)
        
        w = base_w * zoom_factor
        h = base_h * zoom_factor
        cx, cy = center_pos.x(), center_pos.y()
        
        # Matriz da imagem 3
        # y de -2 a 2 (Descendo pra esquerda), x de -2 a 2 (Descendo pra direita)
        priorities = {1: [], 2: [], 3: [], 4: [], 5: []} # 5 = X
        
        matrix = {
            -2: {-2:1, -1:3, 0:3, 1:4, 2:4},
            -1: {-2:2, -1:1, 0:1, 1:3, 2:4},
             0: {-2:2, -1:4, 0:5, 1:2, 2:2},
             1: {-2:4, -1:3, 0:3, 1:2, 2:2},
             2: {-2:4, -1:3, 0:1, 1:1, 2:1}
        }
        
        for y in range(-2, 3):
            for x in range(-2, 3):
                prio = matrix[y][x]
                screen_x = cx + (x - y) * (w / 2)
                screen_y = cy + (x + y) * (h / 2)
                priorities[prio].append(QPoint(int(screen_x), int(screen_y)))
                
        # Enfileirar na ordem 1, 2, 3, 4, 5
        self.formacao_queue = []
        for p in range(1, 6):
            self.formacao_queue.extend(priorities[p])
            
        self.formacao_active = True
        self.title_bar.title.setText(f"🧙‍♂️ FORMAÇÃO ON: Atacando 1/25... (F4 para Parar)")
        
        # Dispara o primeiro hit imediatamente
        self.perform_macro_step()
        self.timer_clicker.start(self.formacao_combat_time)

    def stop_macros(self):
        if self.autoclicker_active or self.formacao_active or self.timer_countdown.isActive():
            self.timer_countdown.stop()
            self.timer_clicker.stop()
            self.autoclicker_active = False
            self.formacao_active = False
            self.title_bar.title.setText(f"Legend Online - Jogando como: {self.email}")
            
    def perform_macro_step(self):
        if not self.autoclicker_active and not self.formacao_active: return
        
        target_widget = self.browser.focusProxy() if self.browser.focusProxy() else self.browser
        target_pos = None
        
        if self.autoclicker_active:
            target_pos = self.autoclicker_pos
        elif self.formacao_active:
            if not self.formacao_queue:
                self.stop_macros()
                return
            target_pos = self.formacao_queue.pop(0)
            restantes = 25 - len(self.formacao_queue)
            self.title_bar.title.setText(f"🧙‍♂️ FORMAÇÃO ON: Atacando {restantes}/25... (F4 para Parar)")
            
        if target_pos:
            event_press = QMouseEvent(QEvent.MouseButtonPress, target_pos, target_pos, Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
            QCoreApplication.postEvent(target_widget, event_press)
            event_release = QMouseEvent(QEvent.MouseButtonRelease, target_pos, target_pos, Qt.LeftButton, Qt.NoButton, Qt.NoModifier)
            QCoreApplication.postEvent(target_widget, event_release)

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        self.page.setAudioMuted(self.is_muted)
        self.title_bar.btn_mute.setText("🔇" if self.is_muted else "🔊")

    def open_image_viewer(self, rel_folder_path):
        abs_path = os.path.abspath(rel_folder_path)
        viewer = ImageViewerDialog(abs_path, self)
        viewer.exec_()

    def relog(self):
        print(f"[{self.email}] Recarregando a página...")
        self.browser.reload()
        
    def clear_cache(self):
        print(f"[{self.email}] Limpando cache do navegador...")
        self.profile.clearHttpCache()
        QMessageBox.information(self, "Cache", "Cache do navegador limpo com sucesso!")

    def inject_login(self, ok):
        if ok and self.email and self.password:
            js_script = f"""
            setTimeout(function() {{
                var emailInput = document.querySelector('input[type="email"]') || document.querySelector('input[name="email"]') || document.querySelector('input[name="login"]') || document.querySelector('input[name="account"]') || document.querySelector('input[name="username"]') || document.querySelector('input[type="text"]');
                var passInput = document.querySelector('input[type="password"]') || document.querySelector('input[name="password"]');
                
                if(emailInput && passInput) {{
                    emailInput.value = '{self.email}';
                    passInput.value = '{self.password}';
                    
                    emailInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    passInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    emailInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    passInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    
                    var btn = document.querySelector('button[type="submit"], input[type="submit"], .btn-login, .login-btn, #btnLogin') || document.evaluate("//*[contains(text(), 'Login')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if(btn && typeof btn.click === 'function') {{
                        btn.click();
                    }} else if (emailInput.form) {{
                        emailInput.form.submit();
                    }}
                    
                    console.log("Credenciais injetadas pelo Custom Launcher!");
                }}
            }}, 1500);
            """
            self.page.runJavaScript(js_script)

    def nativeEvent(self, eventType, message):
        # Intercepta eventos do Windows para permitir redimensionamento pelas bordas em janelas Frameless
        try:
            if eventType == b"windows_generic_MSG":
                import ctypes
                from ctypes.wintypes import MSG
                msg = MSG.from_address(message.__int__())
                if msg.message == 0x0084: # WM_NCHITTEST
                    from PyQt5.QtGui import QCursor
                    pos = self.mapFromGlobal(QCursor.pos())
                    x, y = pos.x(), pos.y()
                    w, h = self.width(), self.height()
                    margin = 8 # Área de detecção da borda em pixels
                    
                    left = x < margin
                    right = x > w - margin
                    top = y < margin
                    bottom = y > h - margin
                    
                    res = 0
                    if top and left: res = 13 # HTTOPLEFT
                    elif top and right: res = 14 # HTTOPRIGHT
                    elif bottom and left: res = 16 # HTBOTTOMLEFT
                    elif bottom and right: res = 17 # HTBOTTOMRIGHT
                    elif top: res = 12 # HTTOP
                    elif bottom: res = 15 # HTBOTTOM
                    elif left: res = 10 # HTLEFT
                    elif right: res = 11 # HTRIGHT
                    
                    if res != 0:
                        return True, res
        except Exception as e:
            pass
        return super().nativeEvent(eventType, message)

    def resizeEvent(self, event):
        # Auto-Zoom Dinâmico
        # Resolução base ideal da interface
        base_width = 1040.0
        base_height = 800.0
        
        current_width = self.width()
        current_height = self.height()
        
        zoom_x = current_width / base_width
        zoom_y = current_height / base_height
        
        # Pega o menor fator para garantir que o jogo caiba inteiro na tela sem cortar
        zoom_factor = min(zoom_x, zoom_y)
        
        # Evita bugs em tamanhos minúsculos limitando o zoom mínimo
        if zoom_factor < 0.2:
            zoom_factor = 0.2
            
        self.page.setZoomFactor(zoom_factor)
        super().resizeEvent(event)

    def closeEvent(self, event):
        dialog = CustomCloseDialog(self)
        dialog.exec_()
        
        if dialog.result_action == "close":
            print(f"[{self.email}] Limpando recursos de memória e fechando...")
            try:
                if hasattr(self, 'page') and self.page:
                    self.page.deleteLater()
                if hasattr(self, 'profile') and self.profile:
                    self.profile.deleteLater()
            except Exception as e:
                print("Erro ao limpar:", e)
            event.accept()
        elif dialog.result_action == "relog":
            self.relog()
            event.ignore()
        else: # Cancel
            event.ignore()

class LauncherHub(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 320, 420)
        
        self.settings = QSettings("CustomLauncher", "LegendOnline")
        self.game_windows = []
        
        self.init_ui()
        self.load_styles()

    def load_styles(self):
        try:
            qss_path = resource_path("style.qss")
            with open(qss_path, "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("Aviso: style.qss não encontrado, rodando sem tema customizado.", e)

    def init_ui(self):
        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(20, 20, 20, 20)
        self.setCentralWidget(wrapper)
        
        self.main_card = QWidget()
        self.main_card.setObjectName("MainCard")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
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
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 20, 30, 30)
        content_layout.setSpacing(15)
        
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        self.saved_accounts = {}
        try:
            accounts_json = self.settings.value("saved_accounts", "{}")
            self.saved_accounts = json.loads(accounts_json)
            # Migração de versão (se ainda for apenas senha, converte para dict)
            for k, v in self.saved_accounts.items():
                if isinstance(v, str):
                    self.saved_accounts[k] = {"password": v, "server": "1252", "nick": ""}
        except:
            self.saved_accounts = {}
            
        # Email and Accounts List Button
        email_container = QWidget()
        email_layout = QHBoxLayout(email_container)
        email_layout.setContentsMargins(0, 0, 0, 0)
        
        self.input_email = QComboBox()
        self.input_email.setEditable(True)
        self.input_email.lineEdit().setPlaceholderText("E-mail")
        self.input_email.addItems(list(self.saved_accounts.keys()))
        self.input_email.setCurrentText(self.settings.value("last_email", ""))
        self.input_email.currentTextChanged.connect(self.on_email_changed)
        
        self.btn_accounts = QPushButton("📋")
        self.btn_accounts.setObjectName("TogglePassBtn") # Reutilizando CSS 
        self.btn_accounts.setFixedSize(35, 35)
        self.btn_accounts.setToolTip("Contas Salvas")
        self.btn_accounts.clicked.connect(self.show_accounts_menu)
        
        email_layout.addWidget(self.input_email)
        email_layout.addWidget(self.btn_accounts)
        
        pass_container = QWidget()
        pass_layout = QHBoxLayout(pass_container)
        pass_layout.setContentsMargins(0, 0, 0, 0)
        
        current_acc = self.saved_accounts.get(self.input_email.currentText(), {})
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setPlaceholderText("Senha")
        self.input_password.setText(current_acc.get("password", ""))
        
        self.btn_toggle_pass = QPushButton("👁")
        self.btn_toggle_pass.setObjectName("TogglePassBtn")
        self.btn_toggle_pass.setFixedSize(35, 35)
        self.btn_toggle_pass.clicked.connect(self.toggle_password_visibility)
        
        pass_layout.addWidget(self.input_password)
        pass_layout.addWidget(self.btn_toggle_pass)
        
        self.input_server = QLineEdit()
        self.input_server.setPlaceholderText("Número do Servidor (ex: 1252)")
        self.input_server.setText(current_acc.get("server", self.settings.value("server", "1252")))
        
        self.input_nick = QLineEdit()
        self.input_nick.setPlaceholderText("Nick no Jogo (Opcional)")
        self.input_nick.setText(current_acc.get("nick", ""))
        
        form_layout.addWidget(email_container)
        form_layout.addWidget(pass_container)
        form_layout.addWidget(self.input_server)
        form_layout.addWidget(self.input_nick)
        
        content_layout.addLayout(form_layout)
        
        # Opções de Cache agora funcionam por debaixo dos panos baseado no QSettings

        
        buttons_layout = QVBoxLayout()
        buttons_layout.setContentsMargins(0, 15, 0, 0)
        buttons_layout.setSpacing(10)
        self.btn_ok = QPushButton("LAUNCH GAME")
        self.btn_ok.setObjectName("LaunchBtn")
        self.btn_ok.setFixedHeight(50)
        self.btn_cancel = QPushButton("EXIT")
        self.btn_cancel.setObjectName("ExitBtn")
        self.btn_cancel.setFixedHeight(40)
        
        self.btn_ok.clicked.connect(self.launch_game)
        self.btn_cancel.clicked.connect(self.close)
        
        buttons_layout.addWidget(self.btn_ok)
        buttons_layout.addWidget(self.btn_cancel)
        content_layout.addLayout(buttons_layout)
        
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
                
                action = QAction(display_text, self)
                action.triggered.connect(lambda checked, e=email: self.input_email.setCurrentText(e))
                menu.addAction(action)
                
        menu.exec_(self.btn_accounts.mapToGlobal(QPoint(0, self.btn_accounts.height())))

    def on_email_changed(self, text):
        if text in self.saved_accounts:
            acc = self.saved_accounts[text]
            self.input_password.setText(acc.get("password", ""))
            self.input_server.setText(acc.get("server", ""))
            self.input_nick.setText(acc.get("nick", ""))
            
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
                "nick": self.input_nick.text().strip()
            }
            self.settings.setValue("saved_accounts", json.dumps(self.saved_accounts))
            self.settings.setValue("last_email", email)
            
        self.settings.setValue("server", server_num)
        
        enable_cache = self.settings.value("enable_cache", True, type=bool)
        
        url_completa = f"https://lobr.creaction-network.com/serverlist/s{server_num}"
        
        gw = GameWindow(email, password, url_completa, enable_cache)
        self.game_windows.append(gw)
        gw.show()

if __name__ == '__main__':
    plugin_path = os.path.abspath("pepflashplayer.dll")

    sys.argv.append(f"--ppapi-flash-path={plugin_path}")
    sys.argv.append("--ppapi-flash-version=32.0.0.371") 
    sys.argv.append("--ignore-gpu-blocklist")
    sys.argv.append("--enable-gpu-rasterization")
    sys.argv.append("--enable-zero-copy")

    app = QApplication(sys.argv)
    QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)

    window = LauncherHub()
    window.show()
    sys.exit(app.exec_())