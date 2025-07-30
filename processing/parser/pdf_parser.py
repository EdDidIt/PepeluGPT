import fitz  # PyMuPDF

def parse(filepath):
    try:
        # Open PDF with PyMuPDF
        doc = fitz.open(filepath)
        content = ""
        
        # Extract text from all pages
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            content += page.get_text("text")
            content += "\n"  # Add page break
        
        doc.close()
        
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