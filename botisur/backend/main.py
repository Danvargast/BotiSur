# main.py (con el router de recetas funcional)

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List, Optional
import uvicorn
import httpx  # Asegúrate de que httpx esté en requirements.txt

# Importaciones locales
import crud
import models
import schemas
import auth
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BotiSur Backend",
    description="Backend para la botillería online BotiSur, usando FastAPI y Supabase.",
    version="1.2.0" # Versión actualizada
)

# --- Configuración de CORS ---
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
    "https://danvargast.github.io",
    "null",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Routers de Autenticación, Ventas, Público (sin cambios) ---
# (El código de los otros routers que ya funcionan va aquí, no es necesario volver a pegarlo)
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

router_public = APIRouter(tags=["Público"])
@router_public.get("/productos/", response_model=List[schemas.Producto], summary="Obtener lista de productos")
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_productos(db, skip=skip, limit=limit)
app.include_router(router_public)


# --- Router de Recetas (API Externa) - AHORA ES FUNCIONAL ---
router_recetas = APIRouter(prefix="/recetas", tags=["Recetas de Cócteles"])

API_BASE_URL = "https://www.thecocktaildb.com/api/json/v1/1"

def parse_cocktail_details(drink: dict) -> schemas.Receta:
    """
    Función de ayuda para transformar la respuesta de la API externa
    en nuestro esquema de Pydantic 'schemas.Receta'.
    """
    ingredientes = []
    for i in range(1, 16):  # La API tiene hasta 15 ingredientes (strIngredient1, strIngredient2, etc.)
        nombre_ingrediente = drink.get(f"strIngredient{i}")
        medida = drink.get(f"strMeasure{i}")
        if nombre_ingrediente: # Si el ingrediente existe
            ingredientes.append(schemas.Ingrediente(
                nombre=nombre_ingrediente.strip(),
                medida=medida.strip() if medida else ""
            ))
        else:
            break # Si no hay más ingredientes, detenemos el bucle
            
    return schemas.Receta(
        id_trago=drink['idDrink'],
        nombre=drink['strDrink'],
        instrucciones=drink['strInstructions'],
        imagen_url=drink['strDrinkThumb'],
        ingredientes=ingredientes
    )

@router_recetas.get("/{ingrediente}", response_model=List[schemas.Receta], summary="Buscar recetas de cócteles por ingrediente")
async def buscar_recetas_por_ingrediente(ingrediente: str):
    """
    Busca recetas que contengan un ingrediente específico.
    Primero busca todos los cócteles por ingrediente y luego obtiene los detalles de cada uno.
    """
    async with httpx.AsyncClient() as client:
        try:
            # 1. Buscar todos los cócteles que contienen el ingrediente
            search_url = f"{API_BASE_URL}/filter.php?i={ingrediente}"
            response = await client.get(search_url)
            response.raise_for_status() # Lanza un error si la respuesta no es 200 OK
            
            data = response.json()
            if not data or 'drinks' not in data or data['drinks'] is None:
                return [] # No se encontraron bebidas

            cocktail_list = data['drinks']
            
            # 2. Obtener los detalles de cada cóctel encontrado (hasta un límite para no sobrecargar)
            detailed_recipes = []
            for cocktail_summary in cocktail_list[:12]: # Limitamos a 12 resultados para no demorar tanto
                cocktail_id = cocktail_summary['idDrink']
                detail_url = f"{API_BASE_URL}/lookup.php?i={cocktail_id}"
                detail_response = await client.get(detail_url)
                detail_data = detail_response.json()

                if detail_data and detail_data['drinks']:
                    parsed_recipe = parse_cocktail_details(detail_data['drinks'][0])
                    detailed_recipes.append(parsed_recipe)
            
            return detailed_recipes

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Error al comunicarse con la API de cócteles.")
        except Exception:
            raise HTTPException(status_code=500, detail="Ocurrió un error inesperado al procesar la solicitud de recetas.")

app.include_router(router_recetas)


# Punto de entrada para ejecutar la aplicación con uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)