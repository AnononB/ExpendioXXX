from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Aquí le decimos a Python cómo conectarse al MySQL de Docker
# 'db' es el nombre del servicio que pusimos en el docker-compose
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root_password_123@db:3306/expendio_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()