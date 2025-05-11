Claro, aquí tienes el contenido listo para copiar y pegar directamente en tu archivo `README.md`:

```markdown
# 🤖 WABuddy

**WABuddy** es una aplicación de escritorio construida con **Python y PyQt5** que permite automatizar el envío de mensajes personalizados a través de WhatsApp, generados mediante **inteligencia artificial (OpenAI)**, a partir de datos cargados desde un archivo Excel.

---

## ✨ Funcionalidades

- Carga de archivos Excel con columnas: `Nombre`, `DNI`, `Telefono`, `Orden`, `Grupo`.
- Generación de mensajes únicos y personalizados usando OpenAI GPT.
- Envío progresivo de mensajes vía WhatsApp, utilizando un `QThreadPool`.
- Interfaz gráfica intuitiva con barra de progreso y tabla dinámica.
- Exportación de resultados a un nuevo archivo Excel.

---

## ⚙️ Requisitos

- Python 3.8 o superior
- Cuenta con clave de API de OpenAI
- Sistema operativo: Windows, macOS o Linux

---

## 🔐 Configuración del entorno

1. Crea un entorno virtual:

```bash
python -m venv venv
````

2. Actívalo:

* En Windows:

```bash
venv\Scripts\activate
```

* En macOS/Linux:

```bash
source venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
OPENAI_API_KEY=tu_clave_de_openai_aquí
```

---

## 🧪 Ejecutar la aplicación

```bash
python run.py
```

---

## 🛠 Generar el archivo ejecutable (.exe)

Si deseas compilar la aplicación a un ejecutable para Windows:

1. Instala **PyInstaller**:

```bash
pip install pyinstaller
```

2. Ejecuta el siguiente comando desde la raíz del proyecto:

```bash
pyinstaller --noconfirm --onefile --windowed run.py
```

Esto generará un `.exe` dentro de la carpeta `dist/`.

---

## 📄 Licencia

MIT License. Puedes utilizar y modificar este proyecto libremente.

---

## 💡 Autor

Desarrollado por [The Empire Tech](https://theempire.tech)
