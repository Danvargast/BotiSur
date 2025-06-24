# auth.py
# (MODIFICADO)
# Ahora usa 'utils.py' para las contraseñas, rompiendo el ciclo.

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
import os

# Importaciones locales
import crud
import models
import schemas
import utils  # <-- Importa el nuevo archivo de utilidades
from database import get_db

# --- CONFIGURACIÓN DE SEGURIDAD ---
SECRET_KEY = os.getenv("SECRET_KEY", "una-clave-secreta-muy-segura-de-respaldo")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# El esquema de OAuth2 que apunta a la URL de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# --- FUNCIONES DE AUTENTICACIÓN ---
def authenticate_user(db: Session, email: str, password: str) -> models.User | None:
    """Busca un usuario y verifica su contraseña."""
    user = crud.get_user_by_email(db, email=email)
    if not user:
        return None
    # Usa la función de verificación desde utils.py
    if not utils.verify_password(password, user.hashed_password):
        return None
    return user

# --- FUNCIONES DE TOKEN (JWT) ---
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Crea un nuevo token de acceso."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- DEPENDENCIAS DE AUTORIZACIÓN ---
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Decodifica el token y obtiene el usuario actual de la base de datos."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    """Verifica si el usuario está 'activo'."""
    return current_user

def get_current_admin_user(current_user: models.User = Depends(get_current_active_user)):
    """Verifica que el usuario actual sea un administrador."""
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador para esta operación."
        )
    return current_user