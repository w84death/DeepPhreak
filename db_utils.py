import sqlite3
from datetime import datetime
import os

class ChatDatabase:
    def __init__(self, db_path="chat_history.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    speaker TEXT,
                    message TEXT,
                    embedding_json TEXT
                )
            ''')
            conn.commit()

    def add_message(self, speaker, message):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'INSERT INTO messages (speaker, message) VALUES (?, ?)',
                (speaker, message)
            )
            conn.commit()

    def search_similar_messages(self, query, limit=5):
        # Basic keyword search for now
        # TODO: Implement proper embedding-based similarity search
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                '''SELECT message FROM messages 
                   WHERE message LIKE ? 
                   ORDER BY timestamp DESC LIMIT ?''',
                (f'%{query}%', limit)
            )
            return cursor.fetchall()

    def get_stats(self):
        with sqlite3.connect(self.db_path) as conn:
            # Get total count
            count = conn.execute('SELECT COUNT(*) FROM messages').fetchone()[0]
            
            # Get latest entry date
            latest = conn.execute(
                'SELECT timestamp FROM messages ORDER BY timestamp DESC LIMIT 1'
            ).fetchone()
            
            latest_date = latest[0] if latest else None
            
            return {
                'total_messages': count,
                'latest_entry': latest_date
            }
