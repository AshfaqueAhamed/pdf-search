 # app/index.py
import sqlite3

def create_index(keywords, file_path):
    conn = sqlite3.connect('index.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS pdf_index (keyword TEXT, file_path TEXT)")
    for keyword, _ in keywords:
        c.execute("INSERT INTO pdf_index (keyword, file_path) VALUES (?, ?)", (keyword, file_path))
    conn.commit()
    conn.close()

