import os
from typing import Dict, List, Any, Optional
from langdetect import detect  # type: ignore
from nltk.tokenize import word_tokenize  # type: ignore
import re

def preprocess(text: str, env: Dict[str, Any]) -> List[str]:
    if env.get("lowercase"):
        text = text.lower()
    if env.get("strip_html"):
        text = re.sub(r"<.*?>", "", text)
    return word_tokenize(text)

def detect_language(text: str) -> str:
    try:
        return detect(text)  # type: ignore
    except Exception:
        return "unknown"

def summarize(text: str, env: Dict[str, Any]) -> Optional[str]:
    if len(text) < env.get("summary_threshold", 1000):
        return None  # Skip tiny files
    # Placeholder: connect to LLM or use extractive summarizer
    return text[:500] + "..."

def extract_metadata(file_path: str, content: str) -> Dict[str, Any]:
    return {
        "filename": os.path.basename(file_path),
        "length": len(content),
        "extension": os.path.splitext(file_path)[1]
        # Expand with real metadata per format later
    }