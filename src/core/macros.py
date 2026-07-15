import time
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication, QEvent, Qt
from PyQt5.QtGui import QMouseEvent

class MacroWorker(QThread):
    # Emitido para atualizar a barra de título
    status_update = pyqtSignal(str)
    # Emitido para indicar que a macro terminou
    finished = pyqtSignal()
    
    def __init__(self, target_widget, macro_type, params):
        super().__init__()
        self.target_widget = target_widget
        self.macro_type = macro_type  # 'autoclick' ou 'formacao'
        self.params = params
        self.is_running = True
        
    def run(self):
        if self.macro_type == 'autoclick':
            self.run_autoclicker()
        elif self.macro_type == 'formacao':
            self.run_formacao()
            
    def run_autoclicker(self):
        pos = self.params.get('pos')
        interval = self.params.get('interval', 1.0)
        
        self.status_update.emit("🛑 AUTOCLICK ON - Pressione F4 para Parar")
        
        while self.is_running:
            self.send_click(pos)
            # Divide o sleep para checar cancelamento mais rápido
            steps = int(interval * 10)
            for _ in range(steps):
                if not self.is_running:
                    break
                time.sleep(0.1)
                
        self.finished.emit()

    def run_formacao(self):
        queue = self.params.get('queue', [])
        combat_time = self.params.get('combat_time', 5000)
        
        total = len(queue)
        for i, pos in enumerate(queue):
            if not self.is_running:
                break
                
            self.status_update.emit(f"🧙‍♂️ FORMAÇÃO ON: Atacando {i+1}/{total}... (F4 para Parar)")
            self.send_click(pos)
            
            # combat_time é em ms
            wait_time = combat_time / 1000.0
            steps = int(wait_time * 10)
            for _ in range(steps):
                if not self.is_running:
                    break
                time.sleep(0.1)
                
        self.finished.emit()
        
    def send_click(self, pos):
        if not pos: return
        event_press = QMouseEvent(QEvent.MouseButtonPress, pos, pos, Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        QCoreApplication.postEvent(self.target_widget, event_press)
        event_release = QMouseEvent(QEvent.MouseButtonRelease, pos, pos, Qt.LeftButton, Qt.NoButton, Qt.NoModifier)
        QCoreApplication.postEvent(self.target_widget, event_release)
        
    def stop(self):
        self.is_running = False
