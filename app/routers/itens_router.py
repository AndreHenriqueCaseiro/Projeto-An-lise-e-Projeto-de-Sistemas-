# app/routers/itens_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import item_model, usuario_model, movimentacao_model, local_model
from ..schemas import item_schema, movimentacao_schema
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

# Adicionar esta nova função ao final do arquivo itens_router.py
@router.post("/{item_id}/transferir", response_model=dict)
def transfer_item(
    item_id: int,
    transferencia: movimentacao_schema.TransferenciaCreate,
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_user)
):
    # 1. Busca o item que será transferido
    db_item = db.query(item_model.Item).filter(item_model.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    local_origem_id = db_item.local_id

    # 2. Verifica se o local de destino existe (opcional, mas boa prática)
    local_destino = db.query(local_model.Local).filter(local_model.Local.id == transferencia.local_destino_id).first()
    if local_destino is None:
        raise HTTPException(status_code=404, detail="Local de destino não encontrado")

    # 3. Impede a transferência para o mesmo local
    if local_origem_id == transferencia.local_destino_id:
        raise HTTPException(status_code=400, detail="O item já está neste local.")

    # 4. Cria o registro de movimentação (histórico)
    nova_movimentacao = movimentacao_model.Movimentacao(
        item_id=item_id,
        local_origem_id=local_origem_id,
        local_destino_id=transferencia.local_destino_id,
        usuario_id=current_user.id,
        observacao=transferencia.observacao
    )
    db.add(nova_movimentacao)

    # 5. Atualiza a localização do item
    db_item.local_id = transferencia.local_destino_id
    db.add(db_item)

    # 6. Salva ambas as alterações no banco de dados de uma vez (transação)
    db.commit()

    return {"message": f"Item ID {item_id} transferido com sucesso para o local ID {transferencia.local_destino_id}"}

# Adicionaremos um endpoint para DELETAR futuramente se necessário