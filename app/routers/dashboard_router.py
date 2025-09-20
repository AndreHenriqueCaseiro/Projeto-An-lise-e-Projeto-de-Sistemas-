# app/routers/dashboard_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..database import get_db
from ..models import usuario_model, produto_model, item_model, local_model, movimentacao_model
from ..schemas import dashboard_schema
from ..security import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/", response_model=dashboard_schema.DashboardData)
def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_user)
):
    # Regra de negócio: Apenas administradores podem ver o dashboard
    if current_user.role != "administrador":
        raise HTTPException(status_code=403, detail="Acesso negado: apenas administradores podem ver o dashboard.")

    # Realiza as consultas para agregar os dados
    total_produtos = db.query(produto_model.Produto).count()
    total_itens = db.query(item_model.Item).count()
    total_locais = db.query(local_model.Local).count()
    total_usuarios = db.query(usuario_model.Usuario).count()

    # Busca os 5 últimos itens adicionados, ordenando pelo ID de forma decrescente
    ultimos_itens = db.query(item_model.Item).order_by(desc(item_model.Item.id)).limit(5).all()

    # Busca as 5 últimas movimentações
    ultimas_movimentacoes = db.query(movimentacao_model.Movimentacao).order_by(desc(movimentacao_model.Movimentacao.id)).limit(5).all()

    # Monta o objeto de resposta
    dashboard_data = {
        "total_produtos": total_produtos,
        "total_itens": total_itens,
        "total_locais": total_locais,
        "total_usuarios": total_usuarios,
        "ultimos_itens_adicionados": ultimos_itens,
        "ultimas_movimentacoes": ultimas_movimentacoes,
    }

    return dashboard_data