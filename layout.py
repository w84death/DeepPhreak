from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, 
                           QLineEdit, QPushButton, QSplitter, QLabel)
from PyQt5.QtCore import Qt
from styles import LOGO

class StartupLayout(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Logo
        self.logo = QTextEdit()
        self.logo.setReadOnly(True)
        self.logo.setPlainText(LOGO)
        self.logo.setStyleSheet("QTextEdit { border: none; font-family: monospace; }")
        self.logo.setMaximumHeight(200)
        layout.addWidget(self.logo)
        
        # Status
        self.status_label = QLabel("Checking Ollama server status...")
        layout.addWidget(self.status_label)
        
        # Buttons
        self.start_button = QPushButton("Start Chatting")
        self.start_button.setEnabled(False)
        layout.addWidget(self.start_button)
        
        self.quit_button = QPushButton("Quit")
        layout.addWidget(self.quit_button)

class ChatLayout(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Create splitter for chat and preview
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Chat history
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setObjectName("chatHistory")
        chat_layout.addWidget(self.chat_history)
        
        # Right panel - Live preview
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        self.preview_area = QTextEdit()
        self.preview_area.setReadOnly(True)
        self.preview_area.setObjectName("previewArea")
        preview_layout.addWidget(self.preview_area)
        
        # Add widgets to splitter
        splitter.addWidget(chat_widget)
        splitter.addWidget(preview_widget)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)

        # Input area
        self.input_line = QLineEdit()
        layout.addWidget(self.input_line)

        self.send_button = QPushButton("Send")
        layout.addWidget(self.send_button)
