# app/routers/locais_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import local_model
from ..schemas import local_schema

router = APIRouter(
    prefix="/locais",
    tags=["Locais"]
)

@router.post("/", response_model=local_schema.Local)
def create_local(local: local_schema.LocalCreate, db: Session = Depends(get_db)):
    db_local = db.query(local_model.Local).filter(local_model.Local.nome == local.nome).first()
    if db_local:
        raise HTTPException(status_code=400, detail="Nome de local já cadastrado")

    novo_local = local_model.Local(**local.model_dump())
    db.add(novo_local)
    db.commit()
    db.refresh(novo_local)
    return novo_local

@router.get("/", response_model=List[local_schema.Local])
def read_locais(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    locais = db.query(local_model.Local).offset(skip).limit(limit).all()
    return locais

@router.get("/{local_id}", response_model=local_schema.Local)
def read_local_by_id(local_id: int, db: Session = Depends(get_db)):
    db_local = db.query(local_model.Local).filter(local_model.Local.id == local_id).first()
    if db_local is None:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return db_local

@router.put("/{local_id}", response_model=local_schema.Local)
def update_local(local_id: int, local_update: local_schema.LocalUpdate, db: Session = Depends(get_db)):
    db_local = db.query(local_model.Local).filter(local_model.Local.id == local_id).first()
    if db_local is None:
        raise HTTPException(status_code=404, detail="Local não encontrado")

    update_data = local_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_local, key, value)

    db.add(db_local)
    db.commit()
    db.refresh(db_local)
    return db_local

@router.delete("/{local_id}", response_model=dict)
def delete_local(local_id: int, db: Session = Depends(get_db)):
    db_local = db.query(local_model.Local).filter(local_model.Local.id == local_id).first()
    if db_local is None:
        raise HTTPException(status_code=404, detail="Local não encontrado")

    db.delete(db_local)
    db.commit()
    return {"message": "Local deletado com sucesso"}