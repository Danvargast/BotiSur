
# crud.py
# (MODIFICADO Y CORREGIDO)
# Ahora usa 'utils.py' para el hash.

from sqlalchemy.orm import Session
from datetime import date

# Importaciones locales
import models
import schemas
import utils  # <-- Importa el nuevo archivo de utilidades

# --- CRUD para Usuario ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # Usa la función de hash desde utils.py
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        nombre=user.nombre,
        apellido=user.apellido,
        telefono=user.telefono
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- CRUD para Venta ---
def create_venta(db: Session, venta: schemas.VentaCreate, usuario_id: int):
    for detalle in venta.detalles:
        producto_db = get_producto(db, detalle.producto_id)
        if not producto_db or producto_db.stock < detalle.cantidad:
            raise ValueError("Stock insuficiente o producto no existe.")
            
    db_venta = models.Venta(fecha=date.today(), usuario_id=usuario_id)
    db.add(db_venta)
    db.flush()
    
    total_venta = 0
    for detalle in venta.detalles:
        producto_db = get_producto(db, detalle.producto_id)
        producto_db.stock -= detalle.cantidad
        db_detalle = models.DetalleVenta(
            venta_id=db_venta.id_venta,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
            precio_unitario=producto_db.precio
        )
        db.add(db_detalle)
        total_venta += detalle.cantidad * producto_db.precio
        
    db_venta.total = total_venta
    db.commit()
    db.refresh(db_venta)
    return db_venta

# --- Resto de funciones CRUD sin cambios ---
def get_ventas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Venta).order_by(models.Venta.id_venta.desc()).offset(skip).limit(limit).all()

def get_ventas_by_user(db: Session, usuario_id: int):
    return db.query(models.Venta).filter(models.Venta.usuario_id == usuario_id).order_by(models.Venta.id_venta.desc()).all()

def get_producto(db: Session, producto_id: int):
    return db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Producto).offset(skip).limit(limit).all()

def create_producto(db: Session, producto: schemas.ProductoCreate):
    db_producto = models.Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(db: Session, producto_id: int, producto_update: schemas.ProductoUpdate):
    db_producto = get_producto(db, producto_id)
    if db_producto:
        update_data = producto_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_producto, key, value)
        db.commit()
        db.refresh(db_producto)
    return db_producto
    
def delete_producto(db: Session, producto_id: int):
    db_producto = get_producto(db, producto_id)
    if db_producto:
        db.delete(db_producto)
        db.commit()
    return db_producto
    
def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Categoria).offset(skip).limit(limit).all()

def create_categoria(db: Session, categoria: schemas.CategoriaCreate):
    db_categoria = models.Categoria(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def get_proveedores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Proveedor).offset(skip).limit(limit).all()

def create_proveedor(db: Session, proveedor: schemas.ProveedorCreate):
    db_proveedor = models.Proveedor(**proveedor.model_dump())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor
