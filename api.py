from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/')
def home():
    return render_template('index.html')  # Serve the UI

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    # Resolve absolute path for the database file
    db_path = os.path.join(os.path.dirname(__file__), "database/pdf_index.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Search query
    query = "SELECT filename, content FROM pdf_index WHERE content LIKE ?"
    cursor.execute(query, (f"%{keyword}%",))
    results = cursor.fetchall()
    conn.close()

    # Format results as JSON
    response = [{"filename": row[0], "snippet": row[1][:200]} for row in results]
    return jsonify({"results": response})

@app.route('/pdfs/<path:filename>', methods=['GET'])
def serve_pdf(filename):
    # Serve the PDF file from the 'pdfs' directory
    pdfs_path = os.path.join(os.path.dirname(__file__), "pdfs")
    return send_from_directory(pdfs_path, filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

