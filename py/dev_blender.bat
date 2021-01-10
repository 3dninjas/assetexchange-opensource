@echo off

rem parameter
SET "ADDON_MODULE=%~1"
IF "%ADDON_MODULE%" == "" SET "ADDON_MODULE=assetimport_blender"

SET "BLENDER_PATH=%~2"
IF "%BLENDER_PATH%" == "" SET "BLENDER_PATH=blender.exe"

echo %0 %ADDON_MODULE% %BLENDER_PATH%

rem environment
set PYTHONPATH=%~dp0exts;%~dp0libs
set BLENDER_USER_CONFIG=%~dp0exts\%ADDON_MODULE%\.dev\config
set BLENDER_USER_SCRIPTS=%~dp0exts\%ADDON_MODULE%\.dev\scripts

echo PYTHONPATH=%PYTHONPATH%
echo BLENDER_USER_CONFIG=%BLENDER_USER_CONFIG%
echo BLENDER_USER_SCRIPTS=%BLENDER_USER_SCRIPTS%

rem run blender
"%BLENDER_PATH%" --python-use-system-env --addons %ADDON_MODULE%_dev
