from datetime import date, datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String

from database import Base


class RegraRetorno(Base):
    __tablename__ = "regras_retorno"

    id = Column(Integer, primary_key=True, index=True)
    situacao = Column(String(50), unique=True, nullable=False, index=True)
    intervalo_dias = Column(Integer, nullable=False)
    ativa = Column(Boolean, default=True, nullable=False)


class Alerta(Base):
    __tablename__ = "alertas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, nullable=True, index=True)
    ultima_visita = Column(Date, nullable=False)
    data_retorno_ideal = Column(Date, nullable=False)
    situacao = Column(String(50), nullable=False, index=True)
    intervalo_dias = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, index=True)
    dias_restantes = Column(Integer, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
