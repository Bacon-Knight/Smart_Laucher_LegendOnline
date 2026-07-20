import sys
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton

class FramelessWindowMixin:
    def enable_windows_snap(self):
        if sys.platform != 'win32':
            return
        try:
            import ctypes
            HWND = self.winId().__int__()
            user32 = ctypes.windll.user32
            style = user32.GetWindowLongW(HWND, -16)
            # WS_THICKFRAME, WS_MINIMIZEBOX, WS_MAXIMIZEBOX, WS_CAPTION
            style |= 0x00040000 | 0x00020000 | 0x00010000 | 0x00C00000
            user32.SetWindowLongW(HWND, -16, style)
        except Exception as e:
            pass

    def setup_linux_frameless(self):
        if sys.platform != 'win32':
            self.setMouseTracking(True)
            self.installEventFilter(self)

    def get_edge_at(self, pos, margin=8):
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()
        
        edges = 0
        if y <= margin:
            edges |= Qt.TopEdge
        elif y >= h - margin:
            edges |= Qt.BottomEdge
            
        if x <= margin:
            edges |= Qt.LeftEdge
        elif x >= w - margin:
            edges |= Qt.RightEdge
            
        return edges

    def linux_event_filter(self, obj, event):
        if sys.platform == 'win32' or self.isMaximized():
            return False
            
        if event.type() == QEvent.MouseMove:
            if event.buttons() == Qt.NoButton:
                edges = self.get_edge_at(event.pos())
                if edges == (Qt.TopEdge | Qt.LeftEdge) or edges == (Qt.BottomEdge | Qt.RightEdge):
                    self.setCursor(Qt.SizeFDiagCursor)
                elif edges == (Qt.TopEdge | Qt.RightEdge) or edges == (Qt.BottomEdge | Qt.LeftEdge):
                    self.setCursor(Qt.SizeBDiagCursor)
                elif edges & (Qt.TopEdge | Qt.BottomEdge):
                    self.setCursor(Qt.SizeVerCursor)
                elif edges & (Qt.LeftEdge | Qt.RightEdge):
                    self.setCursor(Qt.SizeHorCursor)
                else:
                    self.unsetCursor()
        elif event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            edges = self.get_edge_at(event.pos())
            if edges and hasattr(self, "windowHandle") and self.windowHandle():
                if hasattr(self.windowHandle(), "startSystemResize"):
                    if self.windowHandle().startSystemResize(Qt.Edge(edges)):
                        return True
        return False

    def frameless_native_event(self, eventType, message, title_bar_height=40):
        if sys.platform != 'win32':
            return False, 0
        try:
            if eventType == b"windows_generic_MSG":
                import ctypes
                from ctypes.wintypes import MSG
                msg = MSG.from_address(message.__int__())
                if msg.message == 0x0083: # WM_NCCALCSIZE
                    if msg.wParam:
                        return True, 0
                
                if msg.message == 0x0084: # WM_NCHITTEST
                    pos = self.mapFromGlobal(QCursor.pos())
                    x, y = pos.x(), pos.y()
                    w, h = self.width(), self.height()
                    margin = 8
                    
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
                        
                    if y < title_bar_height:
                        child = self.childAt(pos)
                        if not isinstance(child, QPushButton):
                            return True, 2 # HTCAPTION
                            
        except Exception:
            pass
        return False, 0
