import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('risk_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (timestamp TEXT, content TEXT, score INTEGER, level TEXT)''')
    conn.commit()
    conn.close()

def save_result(content, score, level):
    conn = sqlite3.connect('risk_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO history VALUES (?, ?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), content[:100], score, level))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('risk_history.db')
    c = conn.cursor()
    c.execute("SELECT * FROM history ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    return data

def clear_db():
    conn = sqlite3.connect('risk_history.db')
    c = conn.cursor()
    c.execute("DELETE FROM history")
    conn.commit()
    conn.close()