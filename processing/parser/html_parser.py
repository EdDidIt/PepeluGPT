from typing import Dict, Any
from bs4 import BeautifulSoup  # type: ignore

def parse(filepath: str) -> Dict[str, Any]:
    try:
        # Read HTML file
        with open(filepath, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract text content, preserving some structure
        content = ""
        
        # Extract title if present
        title = soup.find('title')
        if title:
            title_text = title.get_text()  # type: ignore
            content += f"Title: {title_text.strip()}\n\n"
        
        # Remove script and style elements
        for script in soup(["script", "style"]):  # type: ignore
            script.extract()  # type: ignore
        
        # Get text content
        text = soup.get_text()  # type: ignore
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        content += '\n'.join(chunk for chunk in chunks if chunk)
        
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