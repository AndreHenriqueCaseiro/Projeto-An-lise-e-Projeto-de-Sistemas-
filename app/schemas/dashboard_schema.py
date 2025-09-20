# app/schemas/dashboard_schema.py

from pydantic import BaseModel
from typing import List
from .item_schema import Item
from .movimentacao_schema import Movimentacao

class DashboardData(BaseModel):
    total_produtos: int
    total_itens: int
    total_locais: int
    total_usuarios: int
    ultimos_itens_adicionados: List[Item]
    ultimas_movimentacoes: List[Movimentacao]

    class Config:
        from_attributes = True