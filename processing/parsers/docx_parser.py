from docx import Document
from typing import Any, Dict, List


class DOCXParser:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    def parse(self, filepath: str) -> List[str]:
        doc = Document(filepath)
        paragraphs = [p.text for p in doc.paragraphs]
        return paragraphs
