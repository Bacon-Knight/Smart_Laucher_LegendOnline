from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QMenu, QAction
from PyQt5.QtCore import Qt

class CustomTitleBar(QWidget):
    def __init__(self, parent=None, is_game_window=False):
        super().__init__(parent)
        self.parent = parent
        self.is_game_window = is_game_window
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(8, 0, 8, 0)
        self.setFixedHeight(28)
        
        import os
        from PyQt5.QtGui import QIcon, QPixmap
        from src.core.config import resource_path
        
        icon_path = resource_path("bacon_knight.ico")
        if os.path.exists(icon_path):
            self.icon_label = QLabel()
            self.icon_label.setPixmap(QIcon(icon_path).pixmap(18, 18))
            self.layout.addWidget(self.icon_label)

        self.title = QLabel("Launcher By Bacon Knight")
        self.title.setObjectName("TitleLabel")
        self.layout.addWidget(self.title)
        self.layout.addStretch()
        
        if self.is_game_window:
            self.btn_tools = QPushButton("🛠")
            self.btn_tools.setFixedSize(22, 22)
            self.btn_tools.setObjectName("TitleBtn")
            self.btn_tools.setToolTip("Ferramentas e Macros")
            
            self.tool_menu = QMenu(self.btn_tools)
            
            action_autoclick = QAction("Iniciar AutoClicker (F4)", self)
            action_autoclick.triggered.connect(self.parent.start_autoclicker)
            self.tool_menu.addAction(action_autoclick)
            
            action_formacao = QAction("Formação Mágica (Macro 5x5)", self)
            action_formacao.triggered.connect(self.parent.start_formacao_magica)
            self.tool_menu.addAction(action_formacao)
            
            action_crise = QAction("Plano de Crise", self)
            action_crise.triggered.connect(lambda: self.parent.open_image_viewer("Ferramentas/Planos de Crise"))
            self.tool_menu.addAction(action_crise)
            
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
            
            menu_quality = self.tool_menu.addMenu("Qualidade Flash ▶")
            
            action_q_low = QAction("🔴 Baixa (Máximo Desempenho)", self)
            action_q_low.triggered.connect(lambda: getattr(self.parent, 'controller', None) and self.parent.controller.set_flash_quality("low"))
            menu_quality.addAction(action_q_low)
            
            action_q_med = QAction("🟡 Média (Intermediário)", self)
            action_q_med.triggered.connect(lambda: getattr(self.parent, 'controller', None) and self.parent.controller.set_flash_quality("medium"))
            menu_quality.addAction(action_q_med)
            
            action_q_high = QAction("🟢 Alta (Visual Completo)", self)
            action_q_high.triggered.connect(lambda: getattr(self.parent, 'controller', None) and self.parent.controller.set_flash_quality("high"))
            menu_quality.addAction(action_q_high)

            self.tool_menu.setStyleSheet("QMenu { background-color: #2b1b3d; color: white; border: 1px solid #c9a444; } QMenu::item:selected { background-color: #c9a444; color: black; }")
            self.btn_tools.setMenu(self.tool_menu)
            
            self.btn_mute = QPushButton("🔊")
            self.btn_mute.setFixedSize(22, 22)
            self.btn_mute.setObjectName("TitleBtn")
            self.btn_mute.setToolTip("Mutar/Desmutar Som da Aba")
            self.btn_mute.clicked.connect(self.parent.toggle_mute)
            
            self.btn_relog = QPushButton("🔄")
            self.btn_relog.setFixedSize(22, 22)
            self.btn_relog.setObjectName("TitleBtn")
            self.btn_relog.setToolTip("Recarregar Página")
            self.btn_relog.clicked.connect(self.parent.relog)
            
            self.btn_cache = QPushButton("🧹")
            self.btn_cache.setFixedSize(22, 22)
            self.btn_cache.setObjectName("TitleBtn")
            self.btn_cache.setToolTip("Forçar Recarregamento (Única forma de limpar a RAM)")
            self.btn_cache.clicked.connect(self.parent.fast_relog)
            
            self.btn_float = QPushButton("⚡")
            self.btn_float.setFixedSize(22, 22)
            self.btn_float.setObjectName("TitleBtn")
            self.btn_float.setToolTip("Painel Flutuante de Macros")
            self.btn_float.clicked.connect(self.parent.toggle_floating_panel)

            self.btn_tray = QPushButton("🔽")
            self.btn_tray.setFixedSize(22, 22)
            self.btn_tray.setObjectName("TitleBtn")
            self.btn_tray.setToolTip("Ocultar na Bandeja (System Tray)")
            self.btn_tray.clicked.connect(self.parent.hide)
            
            self.layout.addWidget(self.btn_tools)
            self.layout.addWidget(self.btn_mute)
            self.layout.addWidget(self.btn_relog)
            self.layout.addWidget(self.btn_cache)
            self.layout.addWidget(self.btn_float)
            self.layout.addWidget(self.btn_tray)

            spacer = QWidget()
            spacer.setFixedWidth(4)
            self.layout.addWidget(spacer)
        
        self.btn_minimize = QPushButton("—")
        self.btn_minimize.setFixedSize(22, 22)
        self.btn_minimize.setObjectName("TitleBtn")
        self.btn_minimize.clicked.connect(self.parent.showMinimized)
        
        self.btn_maximize = QPushButton("🗖")
        self.btn_maximize.setFixedSize(22, 22)
        self.btn_maximize.setObjectName("TitleBtn")
        self.btn_maximize.clicked.connect(self.toggle_maximize)
        
        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(22, 22)
        self.btn_close.setObjectName("TitleBtnClose")
        self.btn_close.clicked.connect(self.parent.close)
        
        self.layout.addWidget(self.btn_minimize)
        self.layout.addWidget(self.btn_maximize)
        self.layout.addWidget(self.btn_close)
        
        self.drag_offset = None

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
            if self.parent.isMaximized():
                return
            if hasattr(self.parent, "windowHandle") and self.parent.windowHandle():
                if hasattr(self.parent.windowHandle(), "startSystemMove"):
                    if self.parent.windowHandle().startSystemMove():
                        return
            self.drag_offset = event.globalPos() - self.parent.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if getattr(self, 'drag_offset', None) is not None and not self.parent.isMaximized():
            self.parent.move(event.globalPos() - self.drag_offset)

    def mouseReleaseEvent(self, event):
        self.drag_offset = None
