import sqlite3
import os
from src.config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            translated_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history_translation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            translated_text TEXT,
            bleu REAL,
            rouge REAL,
            meteor REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dataset (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            indonesia TEXT,
            english TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_translation(input_text: str, translated_text: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO translations (input_text, translated_text) VALUES (?, ?)",
        (input_text, translated_text)
    )
    conn.commit()
    conn.close()

def add_history(input_text: str, translated_text: str, bleu: float, rouge: float, meteor: float):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history_translation (input_text, translated_text, bleu, rouge, meteor) VALUES (?, ?, ?, ?, ?)",
        (input_text, translated_text, bleu, rouge, meteor)
    )
    conn.commit()
    conn.close()

def get_history(limit: int = 50):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history_translation ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def clear_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history_translation")
    conn.commit()
    conn.close()

def delete_history_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history_translation WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def get_total_history_count():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM history_translation")
    count = cursor.fetchone()[0]
    conn.close()
    return count
