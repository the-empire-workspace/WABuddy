@echo off
SET MAIN_SCRIPT=src\run.py
SET APP_NAME=WABuddy

echo 🔧 Construyendo %APP_NAME%...

:: Limpiar anteriores builds
rmdir /S /Q build
rmdir /S /Q dist
del %APP_NAME%.spec 2>nul

:: Construir ejecutable
pyinstaller ^
  --name "%APP_NAME%" ^
  --onefile ^
  --windowed ^
  "%MAIN_SCRIPT%"

echo ✅ Build completado. Ejecutable disponible en dist\%APP_NAME%.exe
pause
