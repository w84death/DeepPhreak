import os
os.environ["QT_QPA_PLATFORM"] = "xcb"

import sys
import json
import requests
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCharFormat, QColor, QFont, QFontDatabase

from styles import CYBERPUNK_STYLE, COLORS
from layout import StartupLayout, ChatLayout

class StartupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeepPhreak Startup")
        self.setStyleSheet(CYBERPUNK_STYLE)
        
        # Setup layout
        self.ui = StartupLayout()
        self.setCentralWidget(self.ui)
        
        # Connect signals
        self.ui.start_button.clicked.connect(self.start_chat)
        self.ui.quit_button.clicked.connect(self.close)
        
        self.resize(700, 400)
        self.center_window()
        self.check_server()

    def center_window(self):
        frame = self.frameGeometry()
        center = QApplication.desktop().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())

    def check_server(self):
        try:
            response = requests.get("http://127.0.0.1:11434/api/version")
            if response.status_code == 200:
                self.ui.status_label.setText("✓ Ollama server is running")
                self.ui.status_label.setStyleSheet("QLabel { color: #00ff9f; }")
                self.ui.start_button.setEnabled(True)
            else:
                raise Exception("Server returned status code: " + str(response.status_code))
        except Exception as e:
            self.ui.status_label.setText("✗ Cannot connect to Ollama server")
            self.ui.status_label.setStyleSheet("QLabel { color: #ff0000; }")
            QTimer.singleShot(2000, self.check_server)  # Retry after 2 seconds

    def start_chat(self):
        self.chat_window = ChatWindow()
        self.chat_window.show()
        self.close()

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ollama_url = "http://127.0.0.1:11434/api/generate"
        self.user_color = QColor(COLORS['user'])
        self.bot_color = QColor(COLORS['bot'])
        
        # Setup layout
        self.ui = ChatLayout()
        self.setCentralWidget(self.ui)
        self.setStyleSheet(CYBERPUNK_STYLE)
        
        # Connect signals
        self.ui.input_line.returnPressed.connect(self.handle_send)
        self.ui.send_button.clicked.connect(self.handle_send)
        
        self.setWindowTitle("DeepPhreak")
        self.resize(1200, 800)
        self.ui.input_line.setFocus()

    def append_colored_text(self, text, color):
        cursor = self.ui.chat_history.textCursor()
        text_format = QTextCharFormat()
        text_format.setForeground(color)
        cursor.movePosition(cursor.End)
        cursor.insertText(text + "\n", text_format)
        self.ui.chat_history.setTextCursor(cursor)
        self.ui.chat_history.ensureCursorVisible()

    def log_message(self, speaker, message):
        color = self.user_color if speaker == "User" else self.bot_color
        self.append_colored_text(f"{speaker}: {message}", color)
        with open(f"logs/20230101_chat.log", "a") as log_file:  # replace with date-based filename
            log_file.write(f"{speaker}: {message}\n")

    def clean_think_tags(self, text):
        # Remove content between <think> tags including the tags
        cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        return cleaned.strip()

    def extract_think_content(self, text):
        # Extract content between <think> tags
        think_matches = re.findall(r'<think>(.*?)</think>', text, flags=re.DOTALL)
        return '\n'.join(think_matches).strip()

    def handle_send(self):
        user_message = self.ui.input_line.text().strip()
        if user_message:
            self.log_message("User", user_message)
            self.ui.input_line.clear()
            self.ui.input_line.setFocus()
            self.ui.preview_area.clear()
            
            try:
                accumulated_response = ""
                for chunk in self.stream_ollama(user_message):
                    accumulated_response += chunk
                    # Show live response in preview
                    self.ui.preview_area.setText(accumulated_response)
                    self.ui.preview_area.moveCursor(self.ui.preview_area.textCursor().End)
                    QApplication.processEvents()
                
                # Clean and add complete response to main chat
                cleaned_response = self.clean_think_tags(accumulated_response)
                self.log_message("Bot", cleaned_response)
                
                # Extract and display thinking content
                thinking_content = self.extract_think_content(accumulated_response)
                if thinking_content:
                    self.ui.preview_area.setText("Bot's Thinking Process:\n\n" + thinking_content)
                
            except Exception as e:
                self.append_colored_text(f"Error: {str(e)}", QColor("red"))

    def stream_ollama(self, prompt):
        try:
            payload = {
                "model": "deepseek-r1:1.5b",
                "prompt": prompt,
                "stream": True
            }
            response = requests.post(self.ollama_url, json=payload, stream=True)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    if 'response' in json_response:
                        yield json_response['response']
                    if json_response.get('done', False):
                        break
                        
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
            yield f"Error: {str(e)}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load custom font
    font_id = QFontDatabase.addApplicationFont("font.otf")
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family, 10))
    
    window = StartupWindow()
    window.show()
    sys.exit(app.exec_())