# models.py
# Este archivo define la estructura de tus tablas de la base de datos.
# Esta es la versión corregida y completa, usando la tabla 'usuarios'.

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

# --- Modelo de Usuario (REEMPLAZA A CLIENTE Y EMPLEADO) ---
class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    telefono = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    rol = Column(String, nullable=False, default='cliente')

    ventas = relationship("Venta", back_populates="usuario")

# --- Modelos de la Tienda ---
class Categoria(Base):
    __tablename__ = "categoria"
    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre_categoria = Column(String, nullable=False)
    productos = relationship("Producto", back_populates="categoria")

class Proveedor(Base):
    __tablename__ = "proveedor"
    id_proveedor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String, nullable=True)
    productos = relationship("Producto", back_populates="proveedor")

class Producto(Base):
    __tablename__ = "producto"
    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, index=True)
    precio = Column(Numeric, nullable=False)
    stock = Column(Integer, nullable=False)
    imagen_url = Column(String, nullable=True) # Incluye el campo de la imagen
    categoria_id = Column(Integer, ForeignKey("categoria.id_categoria"))
    proveedor_id = Column(Integer, ForeignKey("proveedor.id_proveedor"))

    categoria = relationship("Categoria", back_populates="productos")
    proveedor = relationship("Proveedor", back_populates="productos")

# --- Modelos de Venta (MODIFICADO para apuntar a User) ---
class Venta(Base):
    __tablename__ = "venta"
    id_venta = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    total = Column(Numeric, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id")) # Apunta a la nueva tabla de usuarios
    
    usuario = relationship("User", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta")

class DetalleVenta(Base):
    __tablename__ = "detalle_venta"
    id_detalle = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("venta.id_venta"), nullable=False)
    producto_id = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric, nullable=False)
    
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto")
