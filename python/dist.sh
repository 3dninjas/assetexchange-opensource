#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

ROOT="$(realpath "$( dirname "${BASH_SOURCE[0]}" )")"

# check tools
if ! which pyscriptpacker > /dev/null;
then
    echo "Install pyscriptpacker: npm install -g pyscriptpacker"
    exit 1
fi

# clear dist directory
rm -rf "$ROOT/dist"
mkdir -p "$ROOT/dist"

# pack extensions
pyscriptpacker "$ROOT/dist/assetimport_blender.py" "$ROOT/extensions/assetimport_blender" "$ROOT/libraries"
