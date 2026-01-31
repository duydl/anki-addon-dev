import os

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "_data"))

# Define addons with their specific build scripts
ADDONS = [
    {
        "path": "crowd-anki/crowd_anki",
        "scripts": [
            "cd crowd-anki && bash generate_ui.sh",
            "cd crowd-anki && bash fetch_dependencies.sh"
        ]
    }
]

# Files/directories to exclude from the release zip; supports fnmatch patterns.
# Applied to path components and full relative paths (e.g., "__pycache__", "*.pyc").
IGNORE_PATTERNS = [
    "meta.json",
    "README.md",
    "__pycache__",
    "*.pyc",
    "*.pyo",
    ".DS_Store",
]
