# schemas.py
# Este archivo define la "forma" de los datos que entran y salen de tu API.
# Esta es la versión corregida y completa.

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date

# --- Esquemas para Autenticación y Usuarios ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None
    rol: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    nombre: str
    apellido: str
    telefono: Optional[str] = None

# ESTA ES LA CLASE QUE FALTABA Y CAUSABA EL ERROR
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    rol: str
    class Config:
        from_attributes = True

# --- Esquemas para Recetas ---
class Ingrediente(BaseModel):
    nombre: str
    medida: Optional[str] = None

class Receta(BaseModel):
    id_trago: str
    nombre: str
    instrucciones: str
    imagen_url: str
    ingredientes: List[Ingrediente]

# --- Esquemas para Venta ---
class DetalleVentaCreate(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)

class VentaCreate(BaseModel):
    detalles: List[DetalleVentaCreate]

class DetalleVentaInfo(BaseModel):
    id_detalle: int
    cantidad: int
    precio_unitario: float
    class Config:
        from_attributes = True

class Venta(BaseModel):
    id_venta: int
    fecha: date
    total: Optional[float]
    usuario: User
    detalles: List[DetalleVentaInfo] = []
    class Config:
        from_attributes = True

# --- Esquemas para Producto, Categoría, Proveedor ---
class ProveedorBase(BaseModel):
    nombre: str
    telefono: Optional[str] = None

class ProveedorCreate(ProveedorBase):
    pass

class Proveedor(ProveedorBase):
    id_proveedor: int
    class Config:
        from_attributes = True

class CategoriaBase(BaseModel):
    nombre_categoria: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id_categoria: int
    class Config:
        from_attributes = True

class ProductoBase(BaseModel):
    nombre: str
    precio: float
    stock: int
    imagen_url: Optional[str] = None # Incluye el campo de la imagen
    categoria_id: Optional[int] = None
    proveedor_id: Optional[int] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    imagen_url: Optional[str] = None
    categoria_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    
class Producto(ProductoBase):
    id_producto: int
    proveedor: Optional[Proveedor] = None
    class Config:
        from_attributes = True
