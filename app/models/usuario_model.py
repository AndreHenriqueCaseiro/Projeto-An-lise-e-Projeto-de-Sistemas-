# app/models/usuario_model.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False) # Ex: "administrador" ou "usuario"
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())