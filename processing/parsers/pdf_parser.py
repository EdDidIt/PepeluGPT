"""
PDF document extraction using PyMuPDF.
"""

import fitz  # PyMuPDF  # type: ignore
from typing import Any, Dict, List


class PDFParser:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    def parse(self, filepath: str) -> List[str]:
        doc = fitz.open(filepath)  # type: ignore
        text: str = ""
        for page in doc:
            text += page.get_text()  # type: ignore
        # TODO: chunk & return list
        return [text]
