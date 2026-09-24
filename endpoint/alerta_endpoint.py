from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from dto.alerta_dto import (
    AlertaResponse,
    AlertasAtrasadosResponse,
    CalcularRetornoRequest,
    CalcularRetornoResponse,
    RegraRetornoResponse,
    RegraRetornoUpdate,
)
from service import alerta_service

router = APIRouter(prefix="/alertas", tags=["Alertas e calendário de retorno"])


@router.post(
    "/calcular-retorno",
    response_model=CalcularRetornoResponse,
    status_code=status.HTTP_201_CREATED,
)
def calcular_retorno(dados: CalcularRetornoRequest, db: Session = Depends(get_db)):
    return alerta_service.calcular_retorno(db, dados)


@router.get("/atrasados", response_model=AlertasAtrasadosResponse)
def listar_atrasados(db: Session = Depends(get_db)):
    return alerta_service.listar_atrasados(db)


@router.put("/regras/{regra_id}", response_model=RegraRetornoResponse)
def atualizar_regra(
    regra_id: int,
    dados: RegraRetornoUpdate,
    db: Session = Depends(get_db),
):
    return alerta_service.atualizar_regra(db, regra_id, dados)


@router.delete("/{alerta_id}")
def cancelar_alerta(alerta_id: int, db: Session = Depends(get_db)):
    alerta_service.cancelar_alerta(db, alerta_id)
    return {"message": "Alerta cancelado com sucesso."}
