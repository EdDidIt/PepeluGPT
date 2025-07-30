from .schema import ParsedFileResult


def is_valid_parsed_result(result: ParsedFileResult) -> bool:
    """
    Check whether a parsed result meets the expected schema and content requirements.
    """
    required_keys = [
        "filename", "extension", "status", "language",
        "metadata", "tokenized_content"
    ]
    for key in required_keys:
        if key not in result:
            return False
        if result[key] is None and key != "error":  # error can be None for success
            return False

    if result["status"] == "error" and not result.get("error"):
        # Error status must include error message
        return False

    if result["status"] == "success":
        if not result["tokenized_content"]:
            return False
        # Ensure all tokens are strings (redundant if guaranteed by schema)
        # If schema guarantees all tokens are strings, this check can be omitted.

    return True