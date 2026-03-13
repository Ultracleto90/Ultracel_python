@echo off
echo 🔧 Empaquetando aplicación Ultracel...

REM Archivo principal
set MAIN_SCRIPT=Login.py

REM Nombre del ejecutable
set APP_NAME=Ultracel

REM Carpeta de recursos
set ASSETS=assets

REM Ícono personalizado (opcional)
set ICON=%ASSETS%\icono.ico

REM Ejecutar PyInstaller
pyinstaller --onefile --windowed ^
--name %APP_NAME% ^
--add-data "%ASSETS%\*;%ASSETS%" ^
%MAIN_SCRIPT%

echo ✅ Empaquetado completo. Ejecutable disponible en la carpeta "dist".
pause