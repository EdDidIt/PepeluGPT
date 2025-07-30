from pptx import Presentation

def parse(filepath):
    try:
        # Load the PowerPoint presentation
        prs = Presentation(filepath)
        content = ""
        
        # Extract text from all slides
        for slide_num, slide in enumerate(prs.slides, 1):
            content += f"=== Slide {slide_num} ===\n"
            
            # Extract text from all shapes in the slide
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    content += shape.text + "\n"
            content += "\n"
        
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