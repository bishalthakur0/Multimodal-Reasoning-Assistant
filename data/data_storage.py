import sqlite3
import json
from datetime import datetime

class DataStorage:
    def __init__(self, db_path="./data/queries.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                text_query TEXT,
                image_present INTEGER NOT NULL,
                response TEXT,
                feedback TEXT
            )
        """)
        conn.commit()
        conn.close()

    def log_query(self, text_query: str, image_present: bool, response: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO queries (timestamp, text_query, image_present, response)
            VALUES (?, ?, ?, ?)
        """, (timestamp, text_query, int(image_present), response))
        conn.commit()
        conn.close()

    def add_feedback(self, query_id: int, feedback: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE queries SET feedback = ? WHERE id = ?
        """, (feedback, query_id))
        conn.commit()
        conn.close()

    def get_all_queries(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM queries")
        queries = cursor.fetchall()
        conn.close()
        return queries