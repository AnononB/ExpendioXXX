from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Producto(Base):
    __tablename__ = "productos_expendio"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    categoria = Column(String(50))
    precio = Column(Float)
    stock = Column(Integer)