#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

ROOT="$(realpath "$( dirname "${BASH_SOURCE[0]}" )")"

# clear dist directory
rm -rf "$ROOT/dist"
mkdir -p "$ROOT/dist"

# pack extensions
npx -q pyscriptpacker@latest 3.5 "$ROOT/dist/assetimport_blender.py" "$ROOT/extensions/assetimport_blender" "$ROOT/libraries"
npx -q pyscriptpacker@latest 3.5 "$ROOT/dist/spaceprobe_blender.py" "$ROOT/extensions/spaceprobe_blender" "$ROOT/libraries"
