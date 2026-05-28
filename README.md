Extractor de Incapacidades (Versión Texto Digital)
Aplicativo web para subir incapacidades en formato PDF, extraer automáticamente la información del empleado y exportar los datos a Excel.

Stack Tecnológico:
Backend: Python, FastAPI, SQLAlchemy
Base de Datos: PostgreSQL (Neon)
Frontend: HTML, Tailwind CSS, JavaScript
Procesamiento PDF: PyMuPDF
Limitación
Esta versión solo procesa PDFs digitales (aquellos donde se puede seleccionar el texto). Si se sube un PDF escaneado (imagen), el sistema lo rechazará indicando que requiere instalación externa de Tesseract/Poppler.

Instalación y Uso:
Clonar el repositorio.
Crear entorno virtual e instalar dependencias:
cd backendpython -m venv .venv.venv\Scripts\activatepip install -r requirements.txt
Crear archivo .env en la raíz con la variable DATABASE_URL.
Ejecutar servidor: python -m uvicorn main:app --reload
Abrir frontend/index.html en el navegador.

