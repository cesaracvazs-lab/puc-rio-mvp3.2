from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CalcularRetornoRequest(BaseModel):
    paciente_id: Optional[int] = Field(default=None, ge=1)
    ultima_visita: date
    situacao: str = Field(..., min_length=2, max_length=50)


class CalcularRetornoResponse(BaseModel):
    alerta_id: int = Field(validation_alias="id")
    paciente_id: Optional[int]
    ultima_visita: date
    data_retorno_ideal: date
    situacao: str
    intervalo_dias: int
    dias_restantes: int
    status: str
    ativo: bool

    model_config = ConfigDict(from_attributes=True)


class RegraRetornoResponse(BaseModel):
    id: int
    situacao: str
    intervalo_dias: int
    ativa: bool

    model_config = ConfigDict(from_attributes=True)


class RegraRetornoUpdate(BaseModel):
    intervalo_dias: int = Field(..., ge=1, le=3650)
    ativa: Optional[bool] = None


class AlertaResponse(BaseModel):
    id: int
    paciente_id: Optional[int]
    ultima_visita: date
    data_retorno_ideal: date
    situacao: str
    status: str
    dias_restantes: int
    ativo: bool
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertasAtrasadosResponse(BaseModel):
    total_alertas_ativos: int
    total_atrasados: int
    total_em_dia: int
    total_vence_hoje: int
    alertas: List[AlertaResponse]
