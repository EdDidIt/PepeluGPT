import xml.etree.ElementTree as ET
from typing import Any, Dict, List


class XMLParser:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    def parse(self, filepath: str) -> List[str]:
        tree = ET.parse(filepath)
        root = tree.getroot()
        return [ET.tostring(root, encoding="unicode")]
