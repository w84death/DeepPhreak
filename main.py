import os
os.environ["QT_QPA_PLATFORM"] = "xcb"

import sys
import json
import requests
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCharFormat, QColor, QFont, QFontDatabase

from styles import CYBERPUNK_STYLE, COLORS
from layout import StartupLayout, ChatLayout
from db_utils import ChatDatabase
import datetime
from avatar_window import AvatarWindow
from file_processor import FileProcessor

MODEL_SIZES = {
    "DeepSeek 1.5b": "deepseek-r1:1.5b",
    "DeepSeek 7b": "deepseek-r:7b",
    "DeepSeek 70b": "deepseek-r:70b"
}

class StartupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create global avatar window
        if not hasattr(QApplication.instance(), 'avatar_window'):
            QApplication.instance().avatar_window = AvatarWindow()
            QApplication.instance().avatar_window.show()
        
        self.db = ChatDatabase()
        self.setWindowTitle("DeepPhreak Main Menu")
        self.setStyleSheet(CYBERPUNK_STYLE)
        
        # Setup layout
        self.ui = StartupLayout()
        self.setCentralWidget(self.ui)
        
        # Initialize model selection before other operations
        self.selected_model = "DeepSeek 1.5b"  # Default model
        self.ui.model_selector.setCurrentText(self.selected_model)
        self.ui.model_selector.currentTextChanged.connect(self.on_model_change)
        
        # Connect other signals
        self.ui.start_button.clicked.connect(self.start_chat)
        self.ui.quit_button.clicked.connect(self.close)
        
        self.resize(700, 400)
        self.center_window()
        self.check_server()
        
        # Create timer to update stats periodically
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(5000)  # Update every 5 seconds
        
        # Initial stats update
        self.update_stats()

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

    def on_model_change(self, model_name):
        self.selected_model = model_name
        self.update_stats()

    def update_stats(self):
        stats = self.db.get_stats()
        stats_text = f"Selected Model: {self.selected_model}\n"
        stats_text += f"Database: {stats['total_messages']} messages"
        if stats['latest_entry']:
            stats_text += f"\nLast entry: {stats['latest_entry']}"
        else:
            stats_text += "\nNo conversations yet"
        
        self.ui.stats_label.setText(stats_text)
        self.ui.stats_label.setStyleSheet("QLabel { color: #00ff9f; font-size: 10pt; }")

    def start_chat(self):
        self.chat_window = ChatWindow(MODEL_SIZES[self.selected_model])
        self.chat_window.show()
        self.close()

class ChatWindow(QMainWindow):
    def __init__(self, model_name="deepseek-r1:1.5b"):
        super().__init__()
        self.model_name = model_name
        self.ollama_url = "http://127.0.0.1:11434/api/generate"
        self.user_color = QColor(COLORS['user'])
        self.bot_color = QColor(COLORS['bot'])
        self.avatar_window = QApplication.instance().avatar_window
        
        # Setup layout
        self.ui = ChatLayout()
        self.setCentralWidget(self.ui)
        self.setStyleSheet(CYBERPUNK_STYLE)
        
        # Connect signals
        self.ui.input_line.returnPressed.connect(self.handle_send)
        self.ui.send_button.clicked.connect(self.handle_send)
        
        # Connect file attachment
        self.ui.attach_button.clicked.connect(self.handle_attachment)
        self.current_attachment = None
        
        self.setWindowTitle("DeepPhreak")
        self.resize(1200, 800)
        self.ui.input_line.setFocus()
        self.db = ChatDatabase()
        self.context_window = 5  # Number of relevant past messages to include

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
        self.db.add_message(speaker, message)

    def clean_think_tags(self, text):
        # Remove content between <think> tags including the tags
        cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        return cleaned.strip()

    def extract_think_content(self, text):
        # Extract content between <think> tags
        think_matches = re.findall(r'<think>(.*?)</think>', text, flags=re.DOTALL)
        return '\n'.join(think_matches).strip()

    def get_relevant_context(self, current_message):
        relevant_messages = self.db.search_similar_messages(current_message)
        if relevant_messages:
            context = "Here are some relevant past conversations:\n"
            for msg in relevant_messages:
                context += f"- {msg[0]}\n"
            return context
        return ""

    def handle_attachment(self):
        file_filter = "Documents (*.pdf *.txt *.docx *.xlsx *.csv)"
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Attach File", "", file_filter
        )
        
        if filepath:
            self.current_attachment = filepath
            filename = os.path.basename(filepath)
            self.ui.attach_button.setText("📎 " + filename)
            self.ui.attach_button.setToolTip(filepath)

    def handle_send(self):
        user_message = self.ui.input_line.text().strip()
        
        # Process attachment if present
        attachment_content = ""
        if self.current_attachment:
            attachment_content = FileProcessor.process_file(self.current_attachment)
            filename = os.path.basename(self.current_attachment)
            self.log_message("System", f"File attached: {filename}")
            self.current_attachment = None
            self.ui.attach_button.setText("📎")
            self.ui.attach_button.setToolTip("Attach file (PDF, TXT, DOCX, XLSX, CSV)")

        if user_message or attachment_content:
            self.log_message("User", user_message)
            self.ui.input_line.clear()
            self.ui.input_line.setFocus()
            self.ui.preview_area.clear()
            
            try:
                self.avatar_window.set_thinking(True)  # Use floating avatar
                # Get relevant context from past conversations
                context = self.get_relevant_context(user_message)
                
                # Construct prompt with context and attachment
                full_prompt = f"""Context from past conversations:
{context}

{"Attached file content:" if attachment_content else ""}
{attachment_content}

Current user message: {user_message}

Please provide a response taking into account the context and attached file content if relevant."""

                accumulated_response = ""
                for chunk in self.stream_ollama(full_prompt):
                    accumulated_response += chunk
                    # Show live response in preview
                    self.ui.preview_area.setText(accumulated_response)
                    self.ui.preview_area.moveCursor(self.ui.preview_area.textCursor().End)
                    QApplication.processEvents()
                
                self.avatar_window.set_thinking(False)  # Return to idle
                # Clean and add complete response to main chat
                cleaned_response = self.clean_think_tags(accumulated_response)
                self.log_message("Bot", cleaned_response)
                
                # Extract and display thinking content
                thinking_content = self.extract_think_content(accumulated_response)
                if thinking_content:
                    self.ui.preview_area.setText("Bot's Thinking Process:\n\n" + thinking_content)
                
            except Exception as e:
                self.avatar_window.set_thinking(False)  # Return to idle on error
                self.append_colored_text(f"Error: {str(e)}", QColor("red"))

    def stream_ollama(self, prompt):
        try:
            payload = {
                "model": self.model_name,
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
    
    # Create and show windows
    window = StartupWindow()
    window.show()
    sys.exit(app.exec_())