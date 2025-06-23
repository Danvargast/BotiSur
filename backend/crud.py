
# crud.py
# Contiene las funciones para interactuar con la base de datos (Operaciones CRUD).

from sqlalchemy.orm import Session
from datetime import date
import models
import schemas

# --- CRUD para Venta ---

def create_venta(db: Session, venta: schemas.VentaCreate):
    """
    Procesa una nueva venta, valida el stock y crea los registros en la BD.
    Esta operación es atómica: o se completa entera o no se hace nada.
    """
    # 1. Validar stock de todos los productos antes de cualquier operación
    for detalle in venta.detalles:
        producto_db = get_producto(db, detalle.producto_id)
        if not producto_db:
            raise ValueError(f"Producto con ID {detalle.producto_id} no existe.")
        if producto_db.stock < detalle.cantidad:
            raise ValueError(f"Stock insuficiente para '{producto_db.nombre}'. "
                             f"Disponible: {producto_db.stock}, Solicitado: {detalle.cantidad}.")

    # 2. Crear el registro principal de la venta
    db_venta = models.Venta(
        fecha=date.today(),
        cliente_id=venta.cliente_id,
        empleado_id=venta.empleado_id
    )
    db.add(db_venta)
    db.flush() # Asigna un ID a db_venta sin hacer commit todavía

    # 3. Crear detalles y actualizar stock
    total_venta = 0
    for detalle in venta.detalles:
        producto_db = get_producto(db, detalle.producto_id) # Volver a obtener para bloquear la fila
        
        # Descontar stock
        producto_db.stock -= detalle.cantidad
        
        # Crear el registro del detalle de la venta
        db_detalle = models.DetalleVenta(
            venta_id=db_venta.id_venta,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
            precio_unitario=producto_db.precio # Precio al momento de la venta
        )
        db.add(db_detalle)
        total_venta += detalle.cantidad * producto_db.precio

    # Opcional: guardar el total en la venta
    db_venta.total = total_venta
    
    # 4. Confirmar todos los cambios en la base de datos
    db.commit()
    db.refresh(db_venta) # Refrescar para obtener los detalles cargados
    
    return db_venta

def get_ventas(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene un historial de ventas."""
    return db.query(models.Venta).order_by(models.Venta.id_venta.desc()).offset(skip).limit(limit).all()

# --- CRUD para Producto ---

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

# --- CRUD para Categoria ---

def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Categoria).offset(skip).limit(limit).all()

def create_categoria(db: Session, categoria: schemas.CategoriaCreate):
    db_categoria = models.Categoria(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

# --- CRUD para Proveedor ---

def get_proveedores(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene todos los proveedores."""
    return db.query(models.Proveedor).offset(skip).limit(limit).all()

def create_proveedor(db: Session, proveedor: schemas.ProveedorCreate):
    """Crea un nuevo proveedor."""
    db_proveedor = models.Proveedor(**proveedor.model_dump())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

# --- CRUD para Cliente ---

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente