#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

ROOT="$(realpath "$( dirname "${BASH_SOURCE[0]}" )")"

# clear dist directory
rm -rf "$ROOT/dist"
mkdir -p "$ROOT/dist"

# pack assetimport extensions
#npx -q pyscriptpacker@latest "3.5" "$ROOT/dist/assetimport_blender.py" "assetninja_assetimport" "assetimport_blender" "$ROOT/exts" "$ROOT/libs"
#npx -q pyscriptpacker@latest "2.7" "$ROOT/dist/assetimport_maya.py" "assetninja_assetimport" "assetimport_maya" "$ROOT/exts" "$ROOT/libs"
#npx -q pyscriptpacker@latest "2.7" "$ROOT/dist/assetimport_c4d.pyp" "assetninja_assetimport" "assetimport_c4d" "$ROOT/exts" "$ROOT/libs"
npx -q pyscriptpacker@latest "2.7" "$ROOT/dist/assetimport_clarisse.py" "assetninja_assetimport" "assetimport_clarisse" "$ROOT/exts" "$ROOT/libs"
#npx -q pyscriptpacker@latest "2.7" "$ROOT/dist/assetimport_houdini.py" "assetninja_assetimport" "assetimport_houdini" "$ROOT/exts" "$ROOT/libs"

# pack spaceprobe extensions
npx -q pyscriptpacker@latest "3.5" "$ROOT/dist/spaceprobe_blender.py" "assetninja_spaceprobe" "spaceprobe_blender" "$ROOT/exts" "$ROOT/libs"
