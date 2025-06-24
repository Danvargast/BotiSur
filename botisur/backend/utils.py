# utils.py
# (NUEVO ARCHIVO)
# Contiene funciones de utilidad para evitar dependencias circulares.

from passlib.context import CryptContext

# Contexto de contraseñas para encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña plana coincide con el hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera un hash de la contraseña."""
    return pwd_context.hash(password)
