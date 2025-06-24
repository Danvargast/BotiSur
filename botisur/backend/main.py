# main.py
# Archivo principal de la aplicación FastAPI

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
import uvicorn
import httpx # Nueva dependencia para llamadas a APIs externas

# Importaciones locales
import crud
import models
import schemas
import auth
from database import SessionLocal, engine

# Crea las tablas en la base de datos (si no existen)
models.Base.metadata.create_all(bind=engine)

# Inicializa la aplicación FastAPI
app = FastAPI(
    title="BotiSur Backend",
    description="Backend para la botillería online BotiSur, usando FastAPI y Supabase.",
    version="1.1.0"
)

# --- Configuración de CORS (MODIFICADO) ---
# Se ha añadido "null" a la lista de orígenes permitidos
# para aceptar peticiones desde archivos locales (file://).
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
    "https://danvargast.github.io",
    "null", # <--- ESTA ES LA LÍNEA NUEVA
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Router de Autenticación ---
router_auth = APIRouter(prefix="/auth", tags=["Autenticación"])

@router_auth.post("/register", response_model=schemas.User, summary="Registrar un nuevo cliente")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    return crud.create_user(db=db, user=user)

@router_auth.post("/login", response_model=schemas.Token, summary="Iniciar sesión")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Correo electrónico o contraseña incorrectos", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.email, "rol": user.rol}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router_auth.get("/me", response_model=schemas.User, summary="Obtener datos del usuario actual")
def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user

app.include_router(router_auth)


# --- Router de Ventas ---
router_ventas = APIRouter(prefix="/ventas", tags=["Ventas"])

@router_ventas.post("/", response_model=schemas.Venta, summary="Crear una nueva venta (para el usuario autenticado)")
def create_sale(venta: schemas.VentaCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    try:
        return crud.create_venta(db=db, venta=venta, usuario_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router_ventas.get("/", response_model=List[schemas.Venta], summary="Obtener historial de ventas")
def read_sales(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    if current_user.rol == "admin":
        return crud.get_ventas(db)
    else:
        return crud.get_ventas_by_user(db, usuario_id=current_user.id)

app.include_router(router_ventas)


# --- Router de Administración (Productos, Categorías, Proveedores) ---
router_admin = APIRouter(prefix="/admin", tags=["Administración"], dependencies=[Depends(auth.get_current_admin_user)])

@router_admin.post("/productos/", response_model=schemas.Producto, summary="[Admin] Crear un nuevo producto")
def create_product(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.create_producto(db=db, producto=producto)

# ... (otros endpoints de admin)

app.include_router(router_admin)


# --- Router de Recetas (API Externa) ---
router_recetas = APIRouter(prefix="/recetas", tags=["Recetas de Cócteles"])

def parse_cocktail_details(drink: dict) -> schemas.Receta:
    # ... (código sin cambios)
    return schemas.Receta() # Placeholder

@router_recetas.get("/{ingrediente}", response_model=List[schemas.Receta], summary="Buscar recetas de cócteles por ingrediente")
async def buscar_recetas_por_ingrediente(ingrediente: str):
    # ... (código sin cambios)
    return [] # Placeholder

app.include_router(router_recetas)


# --- Endpoints Públicos (no requieren login) ---
router_public = APIRouter(tags=["Público"])

@router_public.get("/productos/", response_model=List[schemas.Producto], summary="Obtener lista de productos")
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_productos(db, skip=skip, limit=limit)

# ... (otros endpoints públicos)

app.include_router(router_public)


# Punto de entrada para ejecutar la aplicación con uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
