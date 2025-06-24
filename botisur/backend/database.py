
# database.py
# Configuración de la conexión a la base de datos (Supabase/PostgreSQL).

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# --- IMPORTANTE ---
# Debes crear un archivo .env en la raíz de tu proyecto con tu URL de conexión de Supabase.
# Ejemplo de contenido para el archivo .env:
# DATABASE_URL="postgresql://postgres:[TU_CONTRASEÑA]@[ID_PROYECTO].db.supabase.co:5432/postgres"
# SECRET_KEY="[TU_CLAVE_SECRETA_GENERADA_CON_OPENSSL]"

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

if not DATABASE_URL or not SECRET_KEY:
    raise Exception("Asegúrate de que las variables DATABASE_URL y SECRET_KEY estén en el archivo .env.")

# Crea el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crea una clase de sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos ORM
Base = declarative_base()

# Dependencia de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()