from typing import Dict, Any
import fitz  # type: ignore # PyMuPDF

def parse(filepath: str) -> Dict[str, Any]:
    try:
        # Open PDF with PyMuPDF
        doc = fitz.open(filepath)  # type: ignore
        content = ""
        
        # Extract text from all pages
        for page_num in range(len(doc)):  # type: ignore
            page = doc.load_page(page_num)  # type: ignore
            page_text = page.get_text("text")  # type: ignore
            if isinstance(page_text, str):
                content += page_text
            content += "\n"  # Add page break
        
        doc.close()  # type: ignore
        
        return {
            "status": "success",
            "filename": filepath,
            "content": content.strip(),
            "error": None
        }
    except Exception as e:
        return {
            "status": "error",
            "filename": filepath,
            "content": None,
            "error": str(e)
        }