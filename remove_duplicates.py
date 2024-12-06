import sqlite3

# Connect to the database
conn = sqlite3.connect('database/pdf_index.db')
cursor = conn.cursor()

# Delete duplicate rows based on filename
cursor.execute('''
DELETE FROM pdf_index
WHERE rowid NOT IN (
    SELECT MIN(rowid) FROM pdf_index GROUP BY filename
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Duplicates removed successfully.")
