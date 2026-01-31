import os

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "_data"))

AUTO_DISCOVER = False

RELEASE_PATHS = [
    "crowd-anki/crowd_anki",
]

# Optional shell commands to run before packaging (e.g., build or vendoring steps).
# Each entry is executed with `shell=True` in order.
SCRIPTS = [
    "./crowd-anki/generate_ui.sh",
    "./crowd-anki/fetch_dependencies.sh",
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
