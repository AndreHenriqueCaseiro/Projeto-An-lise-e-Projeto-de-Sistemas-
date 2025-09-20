# app/routers/itens_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import item_model, usuario_model
from ..schemas import item_schema
from ..security import get_current_user

router = APIRouter(
    prefix="/itens",
    tags=["Itens"]
)

@router.post("/", response_model=item_schema.Item)
def create_item(
    item: item_schema.ItemCreate,
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_user)
):
    # Regra: Administradores e Usuários podem criar itens
    novo_item = item_model.Item(**item.model_dump())
    db.add(novo_item)
    db.commit()
    db.refresh(novo_item)
    return novo_item

@router.get("/", response_model=List[item_schema.Item])
def read_itens(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: usuario_model.Usuario = Depends(get_current_user)
):
    # Regra: Administradores e Usuários podem ver os itens
    itens = db.query(item_model.Item).offset(skip).limit(limit).all()
    return itens

@router.get("/{item_id}", response_model=item_schema.Item)
def read_item_by_id(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_user)
):
    db_item = db.query(item_model.Item).filter(item_model.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return db_item

@router.put("/{item_id}", response_model=item_schema.Item)
def update_item(
    item_id: int,
    item_update: item_schema.ItemUpdate,
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_user)
):
    # Regra: Apenas administradores podem editar itens
    if current_user.role != "administrador":
        raise HTTPException(status_code=403, detail="Acesso negado: apenas administradores podem editar itens.")

    db_item = db.query(item_model.Item).filter(item_model.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Adicionaremos um endpoint para DELETAR futuramente se necessário