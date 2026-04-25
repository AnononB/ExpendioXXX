# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

# Esta función es como el "public function" del controlador de Laravel
def crear_nuevo_producto(db: Session, producto: schemas.ProductoCreate):
    db_producto = models.Producto(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        stock=producto.stock
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def obtener_productos(db: Session):
    return db.query(models.Producto).all()