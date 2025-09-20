# app/routers/produtos_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Importando TODOS os componentes necessários no topo do arquivo
from ..database import get_db, engine
from ..models import produto_model, usuario_model # Adicionamos o modelo de usuário
from ..schemas import produto_schema
from ..security import get_current_user # Importamos nossa dependência de segurança

# A linha abaixo agora funciona, pois o 'engine' já foi importado.
produto_model.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)

# --- Endpoints Protegidos ---

@router.post("/", response_model=produto_schema.Produto)
def create_produto(
    produto: produto_schema.ProdutoCreate, 
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_user) # <- Dependência de autenticação
):
    # Verificação de permissão (role)
    if current_user.role != "administrador":
        raise HTTPException(status_code=403, detail="Acesso negado: apenas administradores podem criar produtos.")
    
    db_produto = db.query(produto_model.Produto).filter(produto_model.Produto.sku == produto.sku).first()
    if db_produto:
        raise HTTPException(status_code=400, detail="SKU já cadastrado")
    
    novo_produto = produto_model.Produto(**produto.model_dump())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@router.get("/", response_model=List[produto_schema.Produto])
def read_produtos(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: usuario_model.Usuario = Depends(get_current_user) # <- Apenas requer login
):
    produtos = db.query(produto_model.Produto).offset(skip).limit(limit).all()
    return produtos

@router.get("/{produto_id}", response_model=produto_schema.Produto)
def read_produto_by_id(
    produto_id: int, 
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_user) # <- Apenas requer login
):
    db_produto = db.query(produto_model.Produto).filter(produto_model.Produto.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto

@router.put("/{produto_id}", response_model=produto_schema.Produto)
def update_produto(
    produto_id: int, 
    produto_update: produto_schema.ProdutoUpdate, 
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_user) # <- Dependência de autenticação
):
    # Verificação de permissão (role)
    if current_user.role != "administrador":
        raise HTTPException(status_code=403, detail="Acesso negado: apenas administradores podem editar produtos.")

    db_produto = db.query(produto_model.Produto).filter(produto_model.Produto.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    update_data = produto_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_produto, key, value)

    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@router.delete("/{produto_id}", response_model=dict)
def delete_produto(
    produto_id: int, 
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_user) # <- Dependência de autenticação
):
    # Verificação de permissão (role)
    if current_user.role != "administrador":
        raise HTTPException(status_code=403, detail="Acesso negado: apenas administradores podem deletar produtos.")

    db_produto = db.query(produto_model.Produto).filter(produto_model.Produto.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(db_produto)
    db.commit()
    return {"message": "Produto deletado com sucesso"}