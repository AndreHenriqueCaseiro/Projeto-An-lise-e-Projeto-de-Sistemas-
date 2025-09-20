# app/routers/itens_router.py (Versão Modificada para o Dia 9)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional # <-- ADICIONAMOS Optional

from ..database import get_db
from ..models import item_model, usuario_model, movimentacao_model, local_model
from ..schemas import item_schema, movimentacao_schema
from ..security import get_current_user

router = APIRouter(
    prefix="/itens",
    tags=["Itens"]
)

# ... (as funções create_item, read_item_by_id, update_item, e transfer_item continuam iguais) ...

@router.post("/", response_model=item_schema.Item)
def create_item(
    item: item_schema.ItemCreate,
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_user)
):
    novo_item = item_model.Item(**item.model_dump())
    db.add(novo_item)
    db.commit()
    db.refresh(novo_item)
    return novo_item

# --- FUNÇÃO MODIFICADA ABAIXO ---
@router.get("/", response_model=List[item_schema.Item])
def read_itens(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: usuario_model.Usuario = Depends(get_current_user),
    # --- NOVOS PARÂMETROS DE FILTRO ---
    local_id: Optional[int] = None,
    status: Optional[str] = None,
    serial_number: Optional[str] = None
):
    # Começamos com a query base
    query = db.query(item_model.Item)

    # Aplicamos os filtros dinamicamente, apenas se eles forem fornecidos
    if local_id is not None:
        query = query.filter(item_model.Item.local_id == local_id)
    
    if status is not None:
        query = query.filter(item_model.Item.status.ilike(f"%{status}%"))

    if serial_number is not None:
        query = query.filter(item_model.Item.serial_number.ilike(f"%{serial_number}%"))

    # Aplicamos a paginação e executamos a query final
    itens = query.offset(skip).limit(limit).all()
    return itens
# --- FIM DA FUNÇÃO MODIFICADA ---

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

# ... (função transfer_item continua igual) ...
@router.post("/{item_id}/transferir", response_model=dict)
def transfer_item(
    item_id: int,
    transferencia: movimentacao_schema.TransferenciaCreate,
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_user)
):
    # ... (código da função de transferência) ...
    db_item = db.query(item_model.Item).filter(item_model.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    local_origem_id = db_item.local_id

    local_destino = db.query(local_model.Local).filter(local_model.Local.id == transferencia.local_destino_id).first()
    if local_destino is None:
        raise HTTPException(status_code=404, detail="Local de destino não encontrado")
    
    if local_origem_id == transferencia.local_destino_id:
        raise HTTPException(status_code=400, detail="O item já está neste local.")

    nova_movimentacao = movimentacao_model.Movimentacao(
        item_id=item_id,
        local_origem_id=local_origem_id,
        local_destino_id=transferencia.local_destino_id,
        usuario_id=current_user.id,
        observacao=transferencia.observacao
    )
    db.add(nova_movimentacao)
    
    db_item.local_id = transferencia.local_destino_id
    db.add(db_item)

    db.commit()

    return {"message": f"Item ID {item_id} transferido com sucesso para o local ID {transferencia.local_destino_id}"}