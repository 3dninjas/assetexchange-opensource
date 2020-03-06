#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

ROOT="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"

# params
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <tool> <product-name> <target-file>"
    exit 1
fi

TOOL="$1"
PRODUCT_NAME="$2"
TARGET_FILE="$3"

# pack assetexchange library for embedding
case "$TOOL" in
blender) npx -q pyscriptpacker@latest "3.5" "$TARGET_FILE" "$PRODUCT_NAME" "assetexchange_blender" "$ROOT/libs" ;;
maya) npx -q pyscriptpacker@latest "2.7" "$TARGET_FILE" "$PRODUCT_NAME" "assetexchange_maya" "$ROOT/libs" ;;
c4d) npx -q pyscriptpacker@latest "2.7" "$TARGET_FILE" "$PRODUCT_NAME" "assetexchange_c4d" "$ROOT/libs" ;;
*)
    echo "Unknown tool name!"
    exit 1
    ;;
esac
