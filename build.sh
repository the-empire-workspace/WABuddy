#!/bin/bash

# Nombre del archivo principal (ajusta si es diferente)
MAIN_SCRIPT="src/run.py"
APP_NAME="WABuddy"

# Activar entorno virtual si es necesario
# source venv/bin/activate

echo "🔧 Construyendo $APP_NAME..."

# Limpiar anteriores builds
rm -rf build dist *.spec

# Construir con PyInstaller
pyinstaller \
  --name "$APP_NAME" \
  --onefile \
  --windowed \
  "$MAIN_SCRIPT"

# Resultado final en dist/
echo "✅ Build completado. Revisa la carpeta dist/"
