from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from src.avatar_widget import AvatarWidget

class AvatarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.avatar = AvatarWidget()
        self.setCentralWidget(self.avatar)
        
        # Window properties
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint |
            Qt.Tool  # Helps with taskbar integration
        )
        
        # Enable mouse tracking for dragging
        self.oldPos = None
        
        # Size and position
        self.resize(200, 150)
        self.move(100, 100)  # Initial position
        
        # Style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.oldPos:
            delta = event.globalPos() - self.oldPos
            self.move(self.pos() + delta)
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.oldPos = None

    def set_thinking(self, is_thinking):
        self.avatar.set_thinking(is_thinking)
