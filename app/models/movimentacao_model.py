# app/models/movimentacao_model.py

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("itens.id"), nullable=False)
    local_origem_id = Column(Integer, ForeignKey("locais.id"), nullable=False)
    local_destino_id = Column(Integer, ForeignKey("locais.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    data_movimentacao = Column(DateTime(timezone=True), server_default=func.now())
    observacao = Column(Text)

    # Relacionamentos
    item = relationship("Item")
    usuario = relationship("Usuario")
    local_origem = relationship("Local", foreign_keys=[local_origem_id])
    local_destino = relationship("Local", foreign_keys=[local_destino_id])