from datetime import date, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from dao import alerta_dao
from dto.alerta_dto import CalcularRetornoRequest, RegraRetornoUpdate
from models import Alerta, RegraRetorno

REGRAS_INICIAIS = {
    "Ativo": 90,
    "Em Tratamento": 15,
    "Alta": 180,
    "Acompanhamento": 30,
}


def inicializar_regras(db: Session) -> None:
    for situacao, intervalo_dias in REGRAS_INICIAIS.items():
        if not alerta_dao.buscar_regra_por_situacao(db, situacao):
            alerta_dao.salvar_regra(
                db,
                RegraRetorno(
                    situacao=situacao,
                    intervalo_dias=intervalo_dias,
                    ativa=True,
                ),
            )


def obter_regra(db: Session, situacao: str) -> RegraRetorno:
    regra = alerta_dao.buscar_regra_por_situacao(db, situacao)
    if not regra or not regra.ativa:
        raise HTTPException(
            status_code=404,
            detail=f"Não existe regra de retorno ativa para a situação '{situacao}'.",
        )
    return regra


def determinar_status(dias_restantes: int) -> str:
    if dias_restantes < 0:
        return "atrasado"
    if dias_restantes == 0:
        return "vence_hoje"
    return "em_dia"


def calcular_retorno(db: Session, dados: CalcularRetornoRequest) -> Alerta:
    regra = obter_regra(db, dados.situacao)
    data_retorno_ideal = dados.ultima_visita + timedelta(days=regra.intervalo_dias)
    dias_restantes = (data_retorno_ideal - date.today()).days

    alerta = Alerta(
        paciente_id=dados.paciente_id,
        ultima_visita=dados.ultima_visita,
        data_retorno_ideal=data_retorno_ideal,
        situacao=regra.situacao,
        intervalo_dias=regra.intervalo_dias,
        status=determinar_status(dias_restantes),
        dias_restantes=dias_restantes,
        ativo=True,
    )
    return alerta_dao.salvar_alerta(db, alerta)


def atualizar_regra(db: Session, regra_id: int, dados: RegraRetornoUpdate) -> RegraRetorno:
    regra = alerta_dao.buscar_regra_por_id(db, regra_id)
    if not regra:
        raise HTTPException(status_code=404, detail="Regra de retorno não encontrada.")

    regra.intervalo_dias = dados.intervalo_dias
    if dados.ativa is not None:
        regra.ativa = dados.ativa
    return alerta_dao.salvar_regra(db, regra)


def listar_atrasados(db: Session) -> dict:
    alertas = alerta_dao.listar_alertas_ativos(db)
    hoje = date.today()

    for alerta in alertas:
        alerta.dias_restantes = (alerta.data_retorno_ideal - hoje).days
        alerta.status = determinar_status(alerta.dias_restantes)

    db.commit()
    atrasados = [alerta for alerta in alertas if alerta.status == "atrasado"]
    em_dia = [alerta for alerta in alertas if alerta.status == "em_dia"]
    vence_hoje = [alerta for alerta in alertas if alerta.status == "vence_hoje"]

    return {
        "total_alertas_ativos": len(alertas),
        "total_atrasados": len(atrasados),
        "total_em_dia": len(em_dia),
        "total_vence_hoje": len(vence_hoje),
        "alertas": alertas,
    }


def cancelar_alerta(db: Session, alerta_id: int) -> None:
    alerta = alerta_dao.buscar_alerta_por_id(db, alerta_id)
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta não encontrado.")

    if not alerta.ativo:
        raise HTTPException(status_code=409, detail="O alerta já está inativo.")

    alerta.ativo = False
    db.commit()
