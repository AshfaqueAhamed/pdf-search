# main.py
from app.extract import extract_text_from_pdf
from app.process import get_keywords
from app.index import create_index

pdf_path = 'static/your_pdf_file.pdf'  # Path to your PDF file

text = extract_text_from_pdf(pdf_path)
keywords = get_keywords(text)
create_index(keywords, pdf_path)
 
