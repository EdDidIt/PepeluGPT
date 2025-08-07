import os


def validate_file(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"🔴 File not found: {path}")
    if not os.path.isfile(path):
        raise ValueError(f"🟡 Not a file: {path}")
