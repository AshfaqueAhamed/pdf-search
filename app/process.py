 # app/process.py
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

def get_keywords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    return Counter(filtered_words).most_common(20)  # Top 20 keywords

