"""
Router for selecting appropriate parsers based on file type.
"""

import os
from pathlib import Path
from typing import Any, Dict

from core.utils import get_logger

LOG = get_logger(__name__)


class ParserRouter:
    """
    Routes files to appropriate parsers based on file extension or content type.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self._parsers: Dict[str, Any] = {}
        self._setup_parsers()

    def _setup_parsers(self) -> None:
        """Initialize available parsers."""
        # Import the actual parser implementations
        from processing.parsers.docx_parser import DOCXParser
        from processing.parsers.html_parser import HTMLParser as ActualHTMLParser
        from processing.parsers.pdf_parser import PDFParser as ActualPDFParser
        from processing.parsers.pptx_parser import PPTXParser
        from processing.parsers.txt_parser import TXTParser
        from processing.parsers.xls_parser import XLSParser
        from processing.parsers.xlsx_parser import XLSXParser
        from processing.parsers.xml_parser import XMLParser as ActualXMLParser

        self._parsers = {
            ".txt": TXTParser(self.config),
            ".md": TXTParser(self.config),
            ".pdf": ActualPDFParser(self.config),
            ".docx": DOCXParser(self.config),
            ".xlsx": XLSXParser(self.config),
            ".xls": XLSParser(self.config),
            ".xml": ActualXMLParser(self.config),
            ".html": ActualHTMLParser(self.config),
            ".pptx": PPTXParser(self.config),
            "default": TXTParser(self.config),
        }

    def get_parser(self, filepath: str) -> Any:
        """
        Get appropriate parser for the given file.

        Args:
            filepath: Path to the file to parse

        Returns:
            Parser instance suitable for the file type
        """
        file_ext = Path(filepath).suffix.lower()
        parser = self._parsers.get(file_ext, self._parsers["default"])  # type: ignore
        LOG.debug(f"Selected parser {type(parser).__name__} for {filepath}")  # type: ignore
        return parser  # type: ignore


class BaseParser:
    """Base parser class that all parsers should inherit from."""

    def parse(self, filepath: str) -> str:
        """
        Parse the file and return content as string.

        Args:
            filepath: Path to the file to parse

        Returns:
            Parsed content as string
        """
        raise NotImplementedError("🔵 Subclasses must implement parse method")


class TextParser(BaseParser):
    """Parser for plain text files."""

    def parse(self, filepath: str) -> str:
        """Parse text file."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            LOG.debug(f"🔵 Parsed text file: {filepath} ({len(content)} chars)")
            return content
        except UnicodeDecodeError:
            # Fallback to latin-1 encoding
            with open(filepath, "r", encoding="latin-1") as f:
                content = f.read()
            LOG.debug(
                f"🔵 Parsed text file with latin-1: {filepath} ({len(content)} chars)"
            )
            return content
        except Exception as e:
            LOG.error(f"🔴 Error parsing text file {filepath}: {e}")
            return f"🔴 Error parsing file: {str(e)}"


class PDFParser(BaseParser):
    """Parser for PDF files."""

    def parse(self, filepath: str) -> str:
        """Parse PDF file."""
        # For now, return a placeholder
        # In a real implementation, you'd use libraries like PyPDF2 or pdfplumber
        try:
            file_size = os.path.getsize(filepath)
            return f"🔵 PDF file content placeholder - {filepath} ({file_size} bytes)"
        except Exception as e:
            LOG.error(f"🔴 Error parsing PDF file {filepath}: {e}")
            return f"🔴 Error parsing PDF file: {str(e)}"


class DocumentParser(BaseParser):
    """Parser for Word documents."""

    def parse(self, filepath: str) -> str:
        """Parse Word document."""
        # For now, return a placeholder
        # In a real implementation, you'd use python-docx
        try:
            file_size = os.path.getsize(filepath)
            return (
                f"🔵 Word document content placeholder - {filepath} ({file_size} bytes)"
            )
        except Exception as e:
            LOG.error(f"🔴 Error parsing Word document {filepath}: {e}")
            return f"🔴 Error parsing Word document: {str(e)}"


class SpreadsheetParser(BaseParser):
    """Parser for Excel spreadsheets."""

    def parse(self, filepath: str) -> str:
        """Parse Excel spreadsheet."""
        # For now, return a placeholder
        # In a real implementation, you'd use openpyxl or pandas
        try:
            file_size = os.path.getsize(filepath)
            return f"🔵 Excel spreadsheet content placeholder - {filepath} ({file_size} bytes)"
        except Exception as e:
            LOG.error(f"🔴 Error parsing Excel spreadsheet {filepath}: {e}")
            return f"🔴 Error parsing Excel spreadsheet: {str(e)}"


class XMLParser(BaseParser):
    """Parser for XML files."""

    def parse(self, filepath: str) -> str:
        """Parse XML file."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            LOG.debug(f"🔵 Parsed XML file: {filepath} ({len(content)} chars)")
            return content
        except Exception as e:
            LOG.error(f"🔴 Error parsing XML file {filepath}: {e}")
            return f"🔴 Error parsing XML file: {str(e)}"


class HTMLParser(BaseParser):
    """Parser for HTML files."""

    def parse(self, filepath: str) -> str:
        """Parse HTML file."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            LOG.debug(f"🔵 Parsed HTML file: {filepath} ({len(content)} chars)")
            return content
        except Exception as e:
            LOG.error(f"🔴 Error parsing HTML file {filepath}: {e}")
            return f"🔴 Error parsing HTML file: {str(e)}"
