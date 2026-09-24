from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import Alerta, RegraRetorno


def buscar_regra_por_situacao(db: Session, situacao: str) -> Optional[RegraRetorno]:
    return (
        db.query(RegraRetorno)
        .filter(func.lower(RegraRetorno.situacao) == situacao.lower())
        .first()
    )


def buscar_regra_por_id(db: Session, regra_id: int) -> Optional[RegraRetorno]:
    return db.query(RegraRetorno).filter(RegraRetorno.id == regra_id).first()


def salvar_regra(db: Session, regra: RegraRetorno) -> RegraRetorno:
    db.add(regra)
    db.commit()
    db.refresh(regra)
    return regra


def salvar_alerta(db: Session, alerta: Alerta) -> Alerta:
    db.add(alerta)
    db.commit()
    db.refresh(alerta)
    return alerta


def listar_alertas_ativos(db: Session) -> list[Alerta]:
    return db.query(Alerta).filter(Alerta.ativo.is_(True)).order_by(Alerta.data_retorno_ideal.asc()).all()


def buscar_alerta_por_id(db: Session, alerta_id: int) -> Optional[Alerta]:
    return db.query(Alerta).filter(Alerta.id == alerta_id).first()
