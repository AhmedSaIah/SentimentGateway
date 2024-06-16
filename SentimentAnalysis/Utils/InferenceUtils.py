import re
from bs4 import BeautifulSoup

def clean_text(text):
    # Remove HTML tags and get plain text
    text = BeautifulSoup(text, "html.parser").get_text()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    # Remove emojis and non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    # Remove float numbers
    text = re.sub(r'\b\d+\.\d+\b', '', text)
    # Normalize whitespaces to a single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text