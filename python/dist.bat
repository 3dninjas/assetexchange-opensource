@echo off

rem change to script directory
cd %~dp0 || goto :error

rem clear dist directory
if exist ".\dist" rmdir /S /Q ".\dist" || goto :error
if not exist ".\dist" mkdir ".\dist" || goto :error

rem pack extensions
call npx -q pyscriptpacker@latest 3.5 ".\dist\assetimport_blender.py" "assetimport_blender" ".\extensions" ".\libraries" || goto :error
call npx -q pyscriptpacker@latest 3.5 ".\dist\spaceprobe_blender.py" "spaceprobe_blender" ".\extensions" ".\libraries" || goto :error

call npx -q pyscriptpacker@latest 2.7 ".\dist\assetimport_maya.py" "assetimport_maya" ".\extensions" ".\libraries" || goto :error

rem error and success handling
goto :EOF
:error
exit /b %errorlevel%
