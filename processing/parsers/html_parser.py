from bs4 import BeautifulSoup
from typing import Any, Dict, List


class HTMLParser:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    def parse(self, filepath: str) -> List[str]:
        with open(filepath, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        return [soup.get_text()]
