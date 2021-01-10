#!/bin/bash
set -e

THIS_PATH="$(realpath "$( dirname "${BASH_SOURCE[0]}" )")"

export PYTHONPATH="${THIS_PATH}/exts:${THIS_PATH}/libs"
export BLENDER_USER_SCRIPTS="${THIS_PATH}/exts/assetimport_blender/.dev"

echo "PYTHONPATH=$PYTHONPATH"
echo "BLENDER_USER_SCRIPTS=$BLENDER_USER_SCRIPTS"

blender --python-use-system-env --addons assetexchange-assetimport-dev
