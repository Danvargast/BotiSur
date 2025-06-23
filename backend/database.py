
# database.py
# Configuración de la conexión a la base de datos (Supabase/PostgreSQL).

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# --- IMPORTANTE ---
# Debes crear un archivo .env en la raíz de tu proyecto con tu URL de conexión de Supabase.
# Ejemplo de contenido para el archivo .env:
# DATABASE_URL="postgresql://postgres:[TU_CONTRASEÑA]@[ID_PROYECTO].db.supabase.co:5432/postgres"

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("No se encontró la variable de entorno DATABASE_URL. Asegúrate de crear un archivo .env.")

# Crea el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crea una clase de sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos ORM
Base = declarative_base()