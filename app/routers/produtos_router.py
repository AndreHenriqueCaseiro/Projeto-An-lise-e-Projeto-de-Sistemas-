# app/routers/produtos_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Importando TODOS os componentes necessários no topo do arquivo
from ..database import get_db, engine # <-- IMPORTAMOS O ENGINE AQUI
from ..models import produto_model
from ..schemas import produto_schema

# A linha abaixo agora funciona, pois o 'engine' já foi importado.
# Esta é uma forma simples de garantir que a tabela seja criada ao iniciar.
# Lembre-se que em produção, o ideal é usar Migrations (Alembic).
produto_model.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)

@router.post("/", response_model=produto_schema.Produto)
def create_produto(produto: produto_schema.ProdutoCreate, db: Session = Depends(get_db)):
    # Verifica se o SKU já existe para evitar duplicatas
    db_produto = db.query(produto_model.Produto).filter(produto_model.Produto.sku == produto.sku).first()
    if db_produto:
        raise HTTPException(status_code=400, detail="SKU já cadastrado")
    
    # Usamos .model_dump() que é o método mais moderno do Pydantic v2
    novo_produto = produto_model.Produto(**produto.model_dump())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@router.get("/", response_model=List[produto_schema.Produto])
def read_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    produtos = db.query(produto_model.Produto).offset(skip).limit(limit).all()
    return produtos
