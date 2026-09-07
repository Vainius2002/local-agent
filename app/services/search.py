from pathlib import Path
from app.config import WORKSPACE_PATH

WORKSPACE = Path(WORKSPACE_PATH)

IGNORED_DIRS = [
    "venv",
    ".git",
    "__pycache__",
    "node_modules",
    ".pytest_cache"
]

def search_files(query):
    result = []

    for path in WORKSPACE.rglob("*"):
        if any(part in path.parts for part in IGNORED_DIRS):
            continue

        if query in path.name:
            result.append(str(path))

        if len(result) >= 50:
            print("Resulting paths are more than 50. Returning first 50 to save tokens:\n")

    return result