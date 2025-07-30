import os
import logging
from typing import Dict, List, Any, Optional, Callable
from tqdm import tqdm
from .parser import (
    docx_parser, pdf_parser, html_parser, xml_parser,
    pptx_parser, txt_parser, xls_parser, xlsx_parser
)
from .parser.utils import preprocess, detect_language, summarize, extract_metadata
from .validators import is_valid_parsed_result
from .schema import ParsedFileResult

# Type aliases for better readability
ParseResult = Dict[str, Any]
EnvConfig = Dict[str, Any]
ParserFunction = Callable[[str], ParseResult]
FileList = List[str]
TagList = List[str]

# Logging setup
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'parser_status.log')
logging.basicConfig(filename=log_file, level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')

EXT_TO_PARSER: Dict[str, ParserFunction] = {
    '.docx': docx_parser.parse,  # type: ignore
    '.pdf': pdf_parser.parse,  # type: ignore
    '.html': html_parser.parse,  # type: ignore
    '.xml': xml_parser.parse,  # type: ignore
    '.pptx': pptx_parser.parse,  # type: ignore
    '.txt': txt_parser.parse,  # type: ignore
    '.xls': xls_parser.parse,  # type: ignore
    '.xlsx': xlsx_parser.parse  # type: ignore
}

def tag_failure(result: ParseResult) -> Optional[TagList]:
    tags: TagList = []
    if result['status'] != 'success':
        tags.append('parse-error')
    if not result.get('tokenized_content'):
        tags.append('tokenization-error')
    if not result.get('language') or result['language'] == 'unknown':
        tags.append('lang-detect-failed')
    if not result.get('metadata'):
        tags.append('metadata-missing')
    return tags if tags else None

def parse_file(file_path: str, env_config: EnvConfig, max_retries: int = 1) -> Optional[ParseResult]:
    ext: str = os.path.splitext(file_path)[1].lower()
    parser_func: Optional[ParserFunction] = EXT_TO_PARSER.get(ext)

    if not parser_func:
        msg: str = f"Unsupported file type: {ext}"
        logging.error(msg)
        return {"status": "error", "filename": file_path, "content": None, "error": msg}

    logging.info(f"Parsing started: {file_path}")

    attempt: int = 0
    result: Optional[ParseResult] = None
    while attempt <= max_retries:
        try:
            result = parser_func(file_path)
            content: Any = result.get("content")

            if result["status"] == "success" and content:
                tokenized: List[str] = preprocess(content, env_config)
                meta: Dict[str, Any] = extract_metadata(file_path, content)
                lang: str = detect_language(content)
                summary: Optional[str] = summarize(content, env_config)

                result.update({
                    "language": lang,
                    "summary": summary,
                    "metadata": meta,
                    "tokenized_content": tokenized
                })

            # Validation and failure tagging
            parsed_result_obj: ParsedFileResult = ParsedFileResult(result)  # type: ignore
            if is_valid_parsed_result(parsed_result_obj):
                logging.info(f"🟢 Valid parsed file: {file_path}")
                return result
            else:
                tags: Optional[TagList] = tag_failure(result)
                logging.warning(f"Validation failed: {file_path} [{', '.join(tags or ['unknown'])}]")

        except Exception as e:
            error_msg: str = f"Exception while parsing {file_path}: {str(e)}"
            logging.error(error_msg)
            return {
                "status": "error",
                "filename": file_path,
                "content": None,
                "error": error_msg
            }

        attempt += 1
        logging.info(f"🔁 Retrying ({attempt}/{max_retries}) for: {file_path}")

    return result


def parse_files(file_list: FileList, env_config: EnvConfig) -> List[Optional[ParseResult]]:
    results: List[Optional[ParseResult]] = []
    for file_path in tqdm(file_list, desc="Parsing files"):
        result: Optional[ParseResult] = parse_file(file_path, env_config, max_retries=env_config.get("max_retries", 1))
        results.append(result)
    return results
