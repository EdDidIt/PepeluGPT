from typing import TypedDict, Optional, List, Dict


class ParsedFileResult(TypedDict):
    filename: str
    extension: str
    status: str               # "success" or "error"
    error: Optional[str]      # Description of error if any
    language: str             # Detected language code (e.g. "en")
    metadata: Dict[str, str]  # File metadata like length, author
    summary: Optional[str]    # Optional summary if file is large
    tokenized_content: List[str]  # GPT-ready tokens