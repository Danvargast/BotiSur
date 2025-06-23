# main.py
# Archivo principal de la aplicación FastAPI

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
import datetime

# Importaciones locales
import crud
import models
import schemas
from database import SessionLocal, engine

# Crea las tablas en la base de datos (si no existen)
models.Base.metadata.create_all(bind=engine)

# Inicializa la aplicación FastAPI
app = FastAPI(
    title="BotiSur Backend",
    description="Backend para la botillería online BotiSur, usando FastAPI y Supabase.",
    version="0.3.0"
)

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
    "https://danvargast.github.io",
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

# --- Endpoints para Ventas ---

@app.post("/ventas/", response_model=schemas.Venta, summary="Crear una nueva venta")
def create_sale(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva venta, valida y actualiza el stock de productos.
    - **cliente_id**: ID del cliente que realiza la compra.
    - **empleado_id**: (Opcional) ID del empleado que gestiona la venta.
    - **detalles**: Lista de productos y cantidades a vender.
    """
    try:
        return crud.create_venta(db=db, venta=venta)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/ventas/", response_model=list[schemas.Venta], summary="Obtener historial de ventas")
def read_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista de todas las ventas realizadas.
    """
    ventas = crud.get_ventas(db, skip=skip, limit=limit)
    return ventas


# --- Endpoints para Productos ---

@app.post("/productos/", response_model=schemas.Producto, summary="Crear un nuevo producto")
def create_product(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.create_producto(db=db, producto=producto)

@app.get("/productos/", response_model=list[schemas.Producto], summary="Obtener una lista de productos")
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    productos = crud.get_productos(db, skip=skip, limit=limit)
    return productos

@app.get("/productos/{producto_id}", response_model=schemas.Producto, summary="Obtener un producto por su ID")
def read_product(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@app.put("/productos/{producto_id}", response_model=schemas.Producto, summary="Actualizar un producto existente")
def update_product(producto_id: int, producto: schemas.ProductoUpdate, db: Session = Depends(get_db)):
    db_producto = crud.update_producto(db=db, producto_id=producto_id, producto_update=producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado para actualizar")
    return db_producto

@app.delete("/productos/{producto_id}", response_model=schemas.Producto, summary="Eliminar un producto")
def delete_product(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.delete_producto(db=db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado para eliminar")
    return db_producto

# --- Endpoints para soporte: Categorías, Proveedores, Clientes ---

@app.post("/categorias/", response_model=schemas.Categoria, summary="Crear una nueva categoría")
def create_category(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud.create_categoria(db=db, categoria=categoria)

@app.get("/categorias/", response_model=list[schemas.Categoria], summary="Obtener todas las categorías")
def read_categories(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.get_categorias(db, skip=skip, limit=limit)

@app.post("/proveedores/", response_model=schemas.Proveedor, summary="Crear un nuevo proveedor")
def create_provider(proveedor: schemas.ProveedorCreate, db: Session = Depends(get_db)):
    return crud.create_proveedor(db=db, proveedor=proveedor)

@app.get("/proveedores/", response_model=list[schemas.Proveedor], summary="Obtener todos los proveedores")
def read_providers(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.get_proveedores(db, skip=skip, limit=limit)

@app.post("/clientes/", response_model=schemas.Cliente, summary="Crear un nuevo cliente")
def create_client(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return crud.create_cliente(db=db, cliente=cliente)

@app.get("/clientes/", response_model=list[schemas.Cliente], summary="Obtener todos los clientes")
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_clientes(db, skip=skip, limit=limit)

# Punto de entrada para ejecutar la aplicación con uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)