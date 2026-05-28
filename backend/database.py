import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Construir la ruta al archivo .env de forma segura en Windows
# __file__ es este archivo (database.py)
# parent es la carpeta backend/
# parent.parent es la carpeta raiz (incapacidades-extractor/)
env_path = Path(__file__).resolve().parent.parent / '.env'

# 2. Cargar el archivo .env
load_dotenv(dotenv_path=env_path)

# 3. Leer la variable de entorno
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# --- COMPROBACIÓN DE SEGURIDAD ---
if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError(f"""
    No se encontró la variable DATABASE_URL.
    Asegúrate de que el archivo .env exista en esta ruta: {env_path}
    Y que contenga la línea DATABASE_URL=postgresql://...
    """)
# ----------------------------------

# Creamos el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Configuramos la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para crear los modelos (tablas)
Base = declarative_base()

# Función que usaremos en la API para obtener la conexión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()