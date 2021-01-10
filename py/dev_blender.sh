#!/bin/bash

# strict mode
set -euo pipefail
IFS=$'\n\t'

# parameter
ADDON_MODULE="${1:-assetimport_blender}"
BLENDER_PATH="${2:-blender}"

echo "$0 '${ADDON_MODULE}' '${BLENDER_PATH}'"

# environment
ROOT_PATH="$(realpath "$( dirname "${BASH_SOURCE[0]}" )")"

export PYTHONPATH="${ROOT_PATH}/exts:${ROOT_PATH}/libs"
export BLENDER_USER_CONFIG="${ROOT_PATH}/exts/${ADDON_MODULE}/.dev/config"
export BLENDER_USER_SCRIPTS="${ROOT_PATH}/exts/${ADDON_MODULE}/.dev/scripts"

echo "PYTHONPATH=$PYTHONPATH"
echo "BLENDER_USER_CONFIG=$BLENDER_USER_CONFIG"
echo "BLENDER_USER_SCRIPTS=$BLENDER_USER_SCRIPTS"

# run blender
"$BLENDER_PATH" --python-use-system-env --addons "${ADDON_MODULE}_dev"
