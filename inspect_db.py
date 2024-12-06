import sqlite3

# Connect to the database
conn = sqlite3.connect('database/pdf_index.db')
cursor = conn.cursor()

# Check the table structure
cursor.execute("PRAGMA table_info(pdf_index)")
columns = cursor.fetchall()

# Print column information
print("Table schema:")
for column in columns:
    print(column)

# Close connection
conn.close()
