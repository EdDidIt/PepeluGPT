from bs4 import BeautifulSoup

def parse(filepath):
    try:
        # Read XML file
        with open(filepath, 'r', encoding='utf-8') as file:
            xml_content = file.read()
        
        # Parse with BeautifulSoup using xml parser
        soup = BeautifulSoup(xml_content, 'xml')
        
        # Extract text content from all elements
        content = ""
        
        # Get all text content, preserving element structure
        for element in soup.find_all(text=True):
            if element and isinstance(element, str):
                text = element.strip()
                if text and text not in ['\n', '\t']:
                    content += text + "\n"
        
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