import os
from langdetect import detect
from nltk.tokenize import word_tokenize
import re

def preprocess(text, env):
    if env.get("lowercase"):
        text = text.lower()
    if env.get("strip_html"):
        text = re.sub(r"<.*?>", "", text)
    return word_tokenize(text)

def detect_language(text):
    try:
        return detect(text)
    except Exception:
        return "unknown"

def summarize(text, env):
    if len(text) < env.get("summary_threshold", 1000):
        return None  # Skip tiny files
    # Placeholder: connect to LLM or use extractive summarizer
    return text[:500] + "..."

def extract_metadata(file_path, content):
    return {
        "filename": os.path.basename(file_path),
        "length": len(content),
        "extension": os.path.splitext(file_path)[1]
        # Expand with real metadata per format later
    }