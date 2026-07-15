from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QMenu, QAction
from PyQt5.QtCore import Qt

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
        
        if self.is_game_window:
            self.btn_tools = QPushButton("🛠")
            self.btn_tools.setFixedSize(30, 30)
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
            
            self.btn_tray = QPushButton("🔽")
            self.btn_tray.setFixedSize(30, 30)
            self.btn_tray.setObjectName("TitleBtn")
            self.btn_tray.setToolTip("Ocultar na Bandeja (System Tray)")
            self.btn_tray.clicked.connect(self.parent.hide)
            
            self.layout.addWidget(self.btn_tools)
            self.layout.addWidget(self.btn_mute)
            self.layout.addWidget(self.btn_relog)
            self.layout.addWidget(self.btn_cache)
            self.layout.addWidget(self.btn_tray)
            
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
