#!/usr/bin/env bash
# Launch Anki with a custom base/profile directory.

set -euo pipefail

# change this to the directory that contain profile data,
SCRIPT_DIR="$(cd -- "$(dirname "$0")" && pwd)"
BASE="${ANKI_BASE:-${SCRIPT_DIR}/_data}"

# use the system/global Anki base & profile (no -b/-p flags),
USE_GLOBAL=0
if [[ "${1:-}" == "--global" ]]; then
  USE_GLOBAL=1
  shift
fi

if (( USE_GLOBAL )); then
  cmd=(uv run anki)
else
  cmd=(uv run anki -b "$BASE")
fi

cmd+=("$@")

exec "${cmd[@]}"
