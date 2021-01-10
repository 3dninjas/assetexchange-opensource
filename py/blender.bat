set PYTHONPATH=%~dp0exts;%~dp0libs
set BLENDER_USER_SCRIPTS=%~dp0exts\assetimport_blender\.dev

echo PYTHONPATH=%PYTHONPATH%
echo BLENDER_USER_SCRIPTS=%BLENDER_USER_SCRIPTS%

"C:\Program Files\Blender Foundation\Blender 2.91\blender.exe" --python-use-system-env --addons assetexchange-assetimport-dev
