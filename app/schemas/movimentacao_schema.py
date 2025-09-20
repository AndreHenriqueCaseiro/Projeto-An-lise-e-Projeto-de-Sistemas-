# app/schemas/movimentacao_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .item_schema import Item
from .local_schema import Local
from .usuario_schema import Usuario

# Esquema para o corpo da requisição de transferência
class TransferenciaCreate(BaseModel):
    local_destino_id: int
    observacao: Optional[str] = None

# Esquema para exibir o registro de uma movimentação
class Movimentacao(BaseModel):
    id: int
    data_movimentacao: datetime
    observacao: Optional[str] = None

    # Dados completos para um histórico rico
    item: Item
    local_origem: Local
    local_destino: Local
    usuario: Usuario

    class Config:
        from_attributes = True