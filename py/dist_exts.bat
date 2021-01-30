@echo off

rem change to script directory
cd %~dp0 || goto :error

rem clear dist directory
if exist ".\dist" rmdir /S /Q ".\dist" || goto :error
if not exist ".\dist" mkdir ".\dist" || goto :error

rem pack assetimport extensions
call npx -q pyscriptpacker@latest "3.5" ".\dist\assetimport_blender.py" "assetninja_assetimport" "assetimport_blender" ".\exts" ".\libs" || goto :error
call npx -q pyscriptpacker@latest "2.7" ".\dist\assetimport_maya.py" "assetninja_assetimport" "assetimport_maya" ".\exts" ".\libs" || goto :error
call npx -q pyscriptpacker@latest "3.5" ".\dist\assetimport_c4d.pyp" "assetninja_assetimport" "assetimport_c4d" ".\exts" ".\libs" || goto :error
call npx -q pyscriptpacker@latest "2.7" ".\dist\assetimport_clarisse.py" "assetninja_assetimport" "assetimport_clarisse" ".\exts" ".\libs" || goto :error
call npx -q pyscriptpacker@latest "2.7" ".\dist\assetimport_houdini.py" "assetninja_assetimport" "assetimport_houdini" ".\exts" ".\libs" || goto :error

rem pack spaceprobe extensions
call npx -q pyscriptpacker@latest "3.5" ".\dist\spaceprobe_blender.py" "assetninja_spaceprobe" "spaceprobe_blender" ".\exts" ".\libs" || goto :error

rem error and success handling
goto :EOF
:error
exit /b %errorlevel%
