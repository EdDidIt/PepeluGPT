"""
Coordinator for document parsing.
"""

from typing import Any, Dict, List, Union

from core.utils import get_logger
from processing.router import ParserRouter
from processing.validators import validate_file

LOG = get_logger(__name__)


class ParserCoordinator:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.router = ParserRouter(config)

    def parse(self, filepath: str) -> str:
        """
        Parse a file using the appropriate parser.

        Args:
            filepath: Path to the file to parse

        Returns:
            Parsed content as string
        """
        try:
            validate_file(filepath)
            parser = self.router.get_parser(filepath)  # type: ignore
            content: Union[List[str], str] = parser.parse(filepath)  # type: ignore
            
            # Convert content to string if it's a list
            if isinstance(content, list):
                result = "\n".join(content)  # type: ignore
            else:
                result = str(content)  # type: ignore
                
            LOG.debug(f"🟢 Successfully parsed {filepath}")
            return result
        except Exception as e:
            LOG.error(f"🔴 Error parsing {filepath}: {e}")
            return f"🔴 Error parsing file: {str(e)}"
