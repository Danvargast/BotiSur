
# models.py
# Define los modelos de la base de datos usando SQLAlchemy ORM.

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

# NOTA DE DISEÑO: Se ha simplificado la estructura de ventas.
# En lugar de las tablas de unión `detalle_venta_producto` y `detalle_venta_venta`,
# se ha creado una única tabla `detalle_venta` que se relaciona directamente
# con `venta` y `producto`. Este es un diseño más estándar y eficiente.

class Categoria(Base):
    __tablename__ = "categoria"
    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre_categoria = Column(String, nullable=False)
    
    productos = relationship("Producto", back_populates="categoria")

class Proveedor(Base):
    __tablename__ = "proveedor"
    id_proveedor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String)

    productos = relationship("Producto", back_populates="proveedor")

class Producto(Base):
    __tablename__ = "producto"
    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, index=True)
    precio = Column(Numeric, nullable=False)
    stock = Column(Integer, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria.id_categoria"))
    proveedor_id = Column(Integer, ForeignKey("proveedor.id_proveedor"))

    categoria = relationship("Categoria", back_populates="productos")
    proveedor = relationship("Proveedor", back_populates="productos")

class Cliente(Base):
    __tablename__ = "cliente"
    id_cliente = Column(Integer, primary_key=True, index=True)
    p_nombre = Column(String, nullable=False)
    p_apellido = Column(String, nullable=False)
    telefono = Column(String)

    ventas = relationship("Venta", back_populates="cliente")

class Empleado(Base):
    __tablename__ = "empleado"
    id_empleado = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    cargo = Column(String, nullable=False)

    ventas = relationship("Venta", back_populates="empleado")

class Venta(Base):
    __tablename__ = "venta"
    id_venta = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    total = Column(Numeric, nullable=True) # Campo añadido para el total
    cliente_id = Column(Integer, ForeignKey("cliente.id_cliente"))
    empleado_id = Column(Integer, ForeignKey("empleado.id_empleado"), nullable=True)

    cliente = relationship("Cliente", back_populates="ventas")
    empleado = relationship("Empleado", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta")

class DetalleVenta(Base):
    __tablename__ = "detalle_venta"
    id_detalle = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("venta.id_venta"), nullable=False)
    producto_id = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric, nullable=False)
    
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto") # Relación simple para acceder a los datos del producto