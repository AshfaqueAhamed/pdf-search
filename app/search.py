 # app/search.py
import sqlite3

def search_keyword(keyword):
    conn = sqlite3.connect('index.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT file_path FROM pdf_index WHERE keyword = ?", (keyword,))
    results = c.fetchall()
    conn.close()
    return results

