#!/usr/bin/env bash

set -euo pipefail

echo "Generating UI Files"

uv run --group crowd-anki-dev pyuic5 ui_files/config.ui -o crowd_anki/config/config_ui_qt5.py
uv run --group crowd-anki-dev pyuic5 ui_files/import.ui -o crowd_anki/importer/import_ui_qt5.py

uv run --group crowd-anki-dev pyuic6 ui_files/config.ui -o crowd_anki/config/config_ui_qt6.py
uv run --group crowd-anki-dev pyuic6 ui_files/import.ui -o crowd_anki/importer/import_ui_qt6.py
