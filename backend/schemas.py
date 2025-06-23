
# schemas.py
# Define los modelos de datos de Pydantic para validación y serialización.

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

# --- Esquemas para Proveedor ---
class ProveedorBase(BaseModel):
    nombre: str
    telefono: Optional[str] = None

class ProveedorCreate(ProveedorBase):
    pass

class Proveedor(ProveedorBase):
    id_proveedor: int

    class Config:
        from_attributes = True

# --- Esquemas para Producto ---
class ProductoBase(BaseModel):
    nombre: str
    precio: float
    stock: int
    categoria_id: Optional[int] = None
    proveedor_id: Optional[int] = None

class ProductoCreate(ProductoBase):
    # Hereda todos los campos de ProductoBase, haciéndolos disponibles para la creación
    pass

class ProductoUpdate(BaseModel):
    # Todos los campos son opcionales para actualizar
    nombre: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    categoria_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    
class Producto(ProductoBase):
    id_producto: int
    proveedor: Optional[Proveedor] = None # Incluir datos del proveedor en la respuesta
    
    class Config:
        from_attributes = True

# --- Esquemas para Categoria ---
class CategoriaBase(BaseModel):
    nombre_categoria: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id_categoria: int
    
    class Config:
        from_attributes = True

# --- Esquemas para Cliente ---
class ClienteBase(BaseModel):
    p_nombre: str
    p_apellido: str
    telefono: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id_cliente: int

    class Config:
        from_attributes = True

# --- Esquemas para Venta ---

# Esquema para un item dentro de la petición de crear venta
class DetalleVentaCreate(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0) # La cantidad debe ser mayor que 0

# Esquema para la petición de crear una venta completa
class VentaCreate(BaseModel):
    cliente_id: int
    empleado_id: Optional[int] = None
    detalles: List[DetalleVentaCreate]

# Esquema para mostrar un detalle de venta en la respuesta
class DetalleVenta(BaseModel):
    id_detalle: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    producto: Producto # Incluye los datos completos del producto vendido

    class Config:
        from_attributes = True

# Esquema completo para la respuesta de una venta
class Venta(BaseModel):
    id_venta: int
    fecha: date
    cliente_id: int
    empleado_id: Optional[int]
    total: Optional[float]
    cliente: Cliente # Incluye los datos del cliente
    detalles: List[DetalleVenta] = []

    class Config:
        from_attributes = True