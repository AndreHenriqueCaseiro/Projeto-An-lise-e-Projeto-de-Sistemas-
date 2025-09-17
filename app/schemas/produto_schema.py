# app/schemas/produto_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Esquema base com os campos compartilhados
class ProdutoBase(BaseModel):
    sku: str
    nome: str
    descricao: Optional[str] = None

# Esquema para a criação de um produto (recebido via API)
class ProdutoCreate(ProdutoBase):
    pass

# Esquema para a leitura/retorno de um produto (enviado via API)
class Produto(ProdutoBase):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes = True # Permite que o Pydantic leia dados de um modelo ORM


# Esquema para a atualização de um produto (campos opcionais)
class ProdutoUpdate(BaseModel):
    sku: Optional[str] = None
    nome: Optional[str] = None
    descricao: Optional[str] = None