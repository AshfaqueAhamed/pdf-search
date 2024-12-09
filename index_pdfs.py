import os
from PyPDF2 import PdfReader
import sqlite3

# Path to the folder containing PDFs
pdf_folder = "pdfs"  

# Connect to the database
conn = sqlite3.connect('database/pdf_index.db')
cursor = conn.cursor()

# Index PDFs
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        filepath = os.path.join(pdf_folder, filename)
        with open(filepath, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

            # Debugging: Check which file is being processed
            print(f"Indexing {filename}")

            # Check if the file already exists in the database
            cursor.execute("SELECT * FROM pdf_index WHERE filename = ?", (filename,))
            existing_entry = cursor.fetchone()

            if existing_entry:
                print(f"File {filename} already indexed. Skipping.")
            else:
                # Insert the file data into the database
                cursor.execute("INSERT INTO pdf_index (filename, content) VALUES (?, ?)", (filename, text))

# Commit changes and close connection
conn.commit()
conn.close()

print("PDF indexing completed!")
