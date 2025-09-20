# app/schemas/item_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from .produto_schema import Produto # Importamos o esquema do Produto
from .local_schema import Local   # Importamos o esquema do Local

class ItemBase(BaseModel):
    serial_number: Optional[str] = None
    status: str = "disponivel"
    data_aquisicao: Optional[date] = None

class ItemCreate(ItemBase):
    produto_id: int
    local_id: int

class ItemUpdate(BaseModel):
    local_id: Optional[int] = None
    serial_number: Optional[str] = None
    status: Optional[str] = None
    data_aquisicao: Optional[date] = None

# Esquema para o retorno de dados (leitura)
class Item(ItemBase):
    id: int
    produto_id: int
    local_id: int
    data_atualizacao: Optional[datetime] = None

    # Estes campos carregarão os objetos completos do produto e do local
    produto: Produto 
    local: Local

    class Config:
        from_attributes = True