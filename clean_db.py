import sqlite3
import os

# Path to the folder containing PDFs
pdf_folder = "pdfs"

# Connect to the database
conn = sqlite3.connect('database/pdf_index.db')
cursor = conn.cursor()

# Get a list of all filenames currently in the `pdfs` folder
current_files = set(os.listdir(pdf_folder))

# Fetch all filenames in the database
cursor.execute("SELECT filename FROM pdf_index")
db_files = {row[0] for row in cursor.fetchall()}

# Identify files that are in the database but no longer in the `pdfs` folder
files_to_delete = db_files - current_files

# Delete entries for those files from the database
for filename in files_to_delete:
    cursor.execute("DELETE FROM pdf_index WHERE filename = ?", (filename,))
    print(f"Removed {filename} from the database.")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database cleaned successfully.")
