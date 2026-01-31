#!/usr/bin/env bash
set -euo pipefail

# Export locked CrowdAnki runtime deps (excluding the workspace itself) and vendor them.
tmp_requirements=$(mktemp)
trap 'rm -f "$tmp_requirements"' EXIT

uv export \
  --only-group crowd-anki \
  --no-default-groups \
  --no-dev \
  --no-emit-project \
  --no-emit-workspace \
  --locked \
  --output-file "$tmp_requirements"

# PYYAML_FORCE_LIBYAML prevents linking against libyaml bindings.
# (--without-libyaml doesn't work). See: https://github.com/yaml/pyyaml/issues/716
PYYAML_FORCE_LIBYAML=0 uv pip install \
  --require-hashes \
  --no-binary dulwich \
  --config-settings-package dulwich:--global-option=--pure \
  --target crowd_anki/dist \
  -r "$tmp_requirements"

# Check for Linux shared object files.  This won't work on Windows and might not work on macOS.
if [ -n "$(find crowd_anki/dist/ -name '*.so')" ]; then
    echo "Found compiled .so file.  Build is not pure python!"
    exit 1
fi
