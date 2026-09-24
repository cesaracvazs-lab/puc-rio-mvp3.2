from fastapi import FastAPI

from database import Base, SessionLocal, engine
from endpoint.alerta_endpoint import router as alerta_router
from service.alerta_service import inicializar_regras

Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    inicializar_regras(db)

app = FastAPI(
    title="API de Alertas e Calendário de Retorno",
    version="1.0.0",
    description="API secundária para calcular urgência de retorno e gerenciar alertas de pacientes.",
)


@app.get("/")
def home():
    return {"status": "API de Alertas e Calendário de Retorno funcionando."}


app.include_router(alerta_router)
