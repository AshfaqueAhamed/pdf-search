import sqlite3

# Connect to the database
conn = sqlite3.connect('database/pdf_index.db')
cursor = conn.cursor()

# Execute a query to fetch all rows from the pdf_index table
cursor.execute("SELECT * FROM pdf_index")
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the connection
conn.close()
