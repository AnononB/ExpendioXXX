from fastapi import FastAPI, Depends
from fastapi import HTTPException # Asegúrate de que esta esté en tus imports
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import engine, get_db
from . import models, schemas

# Crea automáticamente las tablas en MySQL al iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema del Expendio")

# RUTA POST: Envía datos para ser procesados (como dice tu PDF [cite: 110])
# Aparecerá como un botón VERDE en /docs
@app.post("/registrar/")
def registrar_producto(item: schemas.ProductoExpendio, db: Session = Depends(get_db)):
    nuevo = models.Producto(
        nombre=item.nombre, 
        categoria=item.categoria, 
        precio=item.precio, 
        stock=item.stock
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"mensaje": "Producto anotado en el inventario", "datos": nuevo}

# RUTA GET: Pide una representación del recurso (como dice tu PDF )
# Aparecerá como un botón AZUL en /docs
@app.get("/inventario/")
def ver_inventario(db: Session = Depends(get_db)):
    return db.query(models.Producto).all()


# MÉTODO PUT: Para actualizar datos (Precio o Stock)
@app.put("/actualizar/{producto_id}")
def actualizar_producto(producto_id: int, item: schemas.ProductoExpendio, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Ese producto no existe en el expendio")
    
    producto.nombre = item.nombre
    producto.categoria = item.categoria
    producto.precio = item.precio
    producto.stock = item.stock
    
    db.commit()
    return {"mensaje": "Producto actualizado", "datos": producto}

# MÉTODO DELETE: Para eliminar un producto del inventario
@app.delete("/borrar/{producto_id}")
def borrar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="No se encontró el producto para borrar")
    
    db.delete(producto)
    db.commit()
    return {"mensaje": f"Producto {producto_id} eliminado del inventario"}

# RUTA DE FILTRO: Buscar productos por categoría
@app.get("/inventario/categoria/{categoria}")
def buscar_por_categoria(categoria: str, db: Session = Depends(get_db)):
    # Buscamos en la base de datos todos los productos que coincidan con la categoría
    resultados = db.query(models.Producto).filter(func.lower(models.Producto.categoria) == categoria.lower()).all()
    
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No hay productos en la categoría: {categoria}")
    
    return resultados