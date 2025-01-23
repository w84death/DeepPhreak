from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QTimer
from ascii_frames import IDLE_FRAMES, THINKING_FRAMES

class AvatarWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setMaximumHeight(150)
        self.setMaximumWidth(200)
        
        # Setup animation
        self.current_frame = 0
        self.frames = IDLE_FRAMES
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.next_frame)
        self.animation_timer.start(800)  # Slower animation for idle frames
        
        # Style
        self.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                color: #00ff9f;
                border: 1px solid #00ff9f;
                font-family: monospace;
                font-size: 12pt;
            }
        """)
        
        self.show_frame()

    def next_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.show_frame()

    def show_frame(self):
        self.setText(self.frames[self.current_frame])

    def set_thinking(self, is_thinking):
        self.frames = THINKING_FRAMES if is_thinking else IDLE_FRAMES
        self.current_frame = 0
        self.show_frame()
        # Adjust animation speed based on state
        self.animation_timer.setInterval(500 if is_thinking else 800)
