import sqlite3

# Connect to the database 
conn = sqlite3.connect('database/pdf_index.db')
cursor = conn.cursor()

# Create the table with the correct schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS pdf_index (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    content TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("Database initialized successfully!")
