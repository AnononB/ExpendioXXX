from pydantic import BaseModel

class ProductoExpendio(BaseModel):
    nombre: str
    categoria: str
    precio: float
    stock: int