from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                           QLineEdit, QPushButton, QSplitter, QLabel,
                           QComboBox)
from PyQt5.QtCore import Qt
from src.styles import LOGO

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
        
        # Model selector
        model_layout = QHBoxLayout()
        self.model_label = QLabel("Model Size:")
        self.model_selector = QComboBox()
        self.model_selector.addItems(["DeepSeek 1.5b", "DeepSeek 7b", "DeepSeek 70b"])
        self.model_selector.setStyleSheet("""
            QComboBox {
                color: #00ff9f;
                background-color: #1a1a1a;
                border: 1px solid #00ff9f;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                width: 8px;
                height: 8px;
                background: none;
                border-left: 2px solid #00ff9f;
                border-bottom: 2px solid #00ff9f;
                margin-right: 8px;
                subcontrol-position: center right;
                subcontrol-origin: padding;
            }
        """)
        model_layout.addWidget(self.model_label)
        model_layout.addWidget(self.model_selector)
        layout.addLayout(model_layout)
        
        # Status
        self.status_label = QLabel("Checking Ollama server status...")
        layout.addWidget(self.status_label)
        
        # Add stats label
        self.stats_label = QLabel()
        self.stats_label.setAlignment(Qt.AlignCenter)
        
        # Add to layout (assuming you have a vertical layout)
        self.layout().addWidget(self.stats_label)
        # Add some spacing
        self.layout().addSpacing(10)
        
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

        # Input area with file attachment
        input_layout = QHBoxLayout()
        
        self.attach_button = QPushButton("📎")
        self.attach_button.setMaximumWidth(40)
        self.attach_button.setToolTip("Attach file (PDF, TXT, DOCX, XLSX, CSV)")
        input_layout.addWidget(self.attach_button)
        
        self.input_line = QLineEdit()
        input_layout.addWidget(self.input_line)
        
        self.send_button = QPushButton("Send")
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
