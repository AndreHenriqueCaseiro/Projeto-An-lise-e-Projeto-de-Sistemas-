# app/models/produto_model.py

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from ..database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())