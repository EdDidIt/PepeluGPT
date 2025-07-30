from typing import Dict, Optional, Any

def parse(filepath: str) -> Dict[str, Optional[Any]]:
    try:
        # Read text file with different encoding fallbacks
        encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
        content = ""
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as file:
                    content = file.read()
                break
            except UnicodeDecodeError:
                continue
        
        if not content:
            raise Exception("Could not decode file with any supported encoding")
        
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