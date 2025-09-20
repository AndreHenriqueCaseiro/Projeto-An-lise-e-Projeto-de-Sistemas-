# app/models/item_model.py

from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Item(Base):
    __tablename__ = "itens"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    local_id = Column(Integer, ForeignKey("locais.id"), nullable=False)
    serial_number = Column(String(100), unique=True, index=True)
    status = Column(String(50), default="disponivel")
    data_aquisicao = Column(Date)
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos: permitem acessar os objetos relacionados diretamente
    # Ex: item.produto poderá acessar os detalhes do produto associado
    produto = relationship("Produto")
    local = relationship("Local")