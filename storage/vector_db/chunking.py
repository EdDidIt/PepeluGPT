import re
from typing import List, Dict, Any, Tuple

def chunk_document(content: str, filename: str, max_chunk_size: int = 512) -> Tuple[List[str], List[Dict[str, Any]]]:
    paragraphs = content.split('\n\n')
    chunks: List[str] = []
    metadata: List[Dict[str, Any]] = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if len(para) <= max_chunk_size:
            chunks.append(para)
        else:
            sentences = re.split(r'(?<=[.!?]) +', para)
            current_chunk = ""

            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                if len(current_chunk + sentence) > max_chunk_size and current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    current_chunk += " " + sentence if current_chunk else sentence

            if current_chunk.strip():
                chunks.append(current_chunk.strip())

    for i, chunk in enumerate(chunks):
        metadata.append({
            "filename": filename,
            "chunk_id": i,
            "content": chunk,
            "length": len(chunk)
        })

    return chunks, metadata