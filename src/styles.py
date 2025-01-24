CYBERPUNK_STYLE = """
QMainWindow, QWidget {
    background-color: #0a0a0f;
    color: #00ff9f;
}
QTextEdit {
    background-color: #1a1a24;
    color: #00ff9f;
    border: 1px solid #00ff9f;
    border-radius: 5px;
    padding: 5px;
    selection-background-color: #ff00ff40;
}
QLineEdit {
    background-color: #1a1a24;
    color: #00ff9f;
    border: 2px solid #00ff9f;
    border-radius: 5px;
    padding: 5px;
    selection-background-color: #ff00ff40;
}
QPushButton {
    background-color: #1a1a24;
    color: #00ff9f;
    border: 2px solid #00ff9f;
    border-radius: 5px;
    padding: 8px 15px;
}
QPushButton:hover {
    background-color: #00ff9f;
    color: #0a0a0f;
}
QPushButton:pressed {
    background-color: #ff00ff;
    border-color: #ff00ff;
}
QSplitter::handle {
    background-color: #00ff9f;
    width: 2px;
}
QTextEdit#chatHistory {
    background-color: #1a1a24;
    color: #00ff9f;
    border: 1px solid #00ff9f;
    border-radius: 5px;
    padding: 5px;
    selection-background-color: #ff00ff40;
    font-size: 12pt;
}
QTextEdit#previewArea {
    background-color: #1a1a24;
    color: #ff00ff;
    border: 1px solid #ff00ff;
    border-radius: 5px;
    padding: 5px;
    selection-background-color: #ff00ff40;
}
"""

LOGO = """
██████╗ ███████╗███████╗██████╗ ██████╗ ██╗  ██╗██████╗ ███████╗ █████╗ ██╗  ██╗
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██║  ██║██╔══██╗██╔════╝██╔══██╗██║ ██╔╝
██║  ██║█████╗  █████╗  ██████╔╝██████╔╝███████║██████╔╝█████╗  ███████║█████╔╝ 
██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔═══╝ ██╔══██║██╔══██╗██╔══╝  ██╔══██║██╔═██╗ 
██████╔╝███████╗███████╗██║     ██║     ██║  ██║██║  ██║███████╗██║  ██║██║  ██╗
╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
         DESIGNED BY KRZYSZTOF KRYSTIAN JANKOWSKI ═ CODED BY LLMs
"""

COLORS = {
    'user': "#00ff9f",  # Neon green
    'bot': "#ff00ff",   # Neon pink
    'error': "#ff0000", # Red
}
