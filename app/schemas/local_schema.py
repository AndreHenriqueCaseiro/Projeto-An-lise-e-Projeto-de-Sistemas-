# app/schemas/local_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LocalBase(BaseModel):
    nome: str
    descricao: Optional[str] = None

class LocalCreate(LocalBase):
    pass

class LocalUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None

class Local(LocalBase):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes = True