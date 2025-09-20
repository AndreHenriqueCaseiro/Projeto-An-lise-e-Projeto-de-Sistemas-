# app/schemas/usuario_schema.py

from pydantic import BaseModel
from datetime import datetime

class UsuarioBase(BaseModel):
    username: str
    role: str

class UsuarioCreate(UsuarioBase):
    password: str # Recebe a senha em texto puro ao criar

class Usuario(UsuarioBase):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes = True