from sqlalchemy.orm import Session
from datetime import date
import models
import schemas
import utils

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
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