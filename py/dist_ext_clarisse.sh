#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

ROOT="$(realpath "$( dirname "${BASH_SOURCE[0]}" )")"

# clear dist directory
rm -rf "$ROOT/dist"
mkdir -p "$ROOT/dist"

# pack assetimport extensions
npx -q pyscriptpacker@latest "2.7" "$ROOT/dist/assetimport_clarisse.pyp" "assetninja_assetimport" "assetimport_clarisse" "$ROOT/exts" "$ROOT/libs"
