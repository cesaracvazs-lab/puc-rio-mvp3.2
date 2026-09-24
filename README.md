# API de Alertas e Calendário de Retorno

API secundária do MVP de Controle de Pacientes. Ela calcula a urgência da próxima consulta com base na data de `ultima_visita` e na situação do paciente, mantendo regras de intervalo e alertas ativos em SQLite.

## Responsabilidade

A API principal de pacientes pode enviar `paciente_id`, `ultima_visita` e `situacao` para esta API. A API secundária então:

- calcula a data ideal do retorno;
- classifica o alerta como `em_dia`, `vence_hoje` ou `atrasado`;
- mantém métricas de alertas ativos;
- permite alterar regras de intervalo;
- permite cancelar alertas.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## Estrutura

```text
alerta_retorno/
├── dao/
├── dto/
├── endpoint/
├── service/
├── database.py
├── models.py
├── main.py
├── Dockerfile
└── requirements.txt
```

## Execução local

```bash
cd alerta_retorno
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

Documentação Swagger: http://127.0.0.1:8001/docs

ReDoc: http://127.0.0.1:8001/redoc

## Rotas

### POST `/alertas/calcular-retorno`

Calcula e salva um alerta de retorno.

```json
{
  "paciente_id": 1,
  "ultima_visita": "2026-09-01",
  "situacao": "Em Tratamento"
}
```

A regra inicial de `Em Tratamento` usa intervalo de 15 dias. O resultado informa a data ideal, dias restantes e status.

### GET `/alertas/atrasados`

Retorna métricas dos alertas ativos e a lista detalhada, incluindo totais atrasados, em dia e com vencimento hoje.

### PUT `/alertas/regras/{id}`

Atualiza o intervalo de uma regra existente.

```json
{
  "intervalo_dias": 30,
  "ativa": true
}
```

Regras criadas inicialmente: `Ativo`, `Em Tratamento`, `Alta` e `Acompanhamento`.

### DELETE `/alertas/{id}`

Cancela um alerta ativo pelo identificador retornado em `POST /alertas/calcular-retorno`.

## Banco de dados

A aplicação cria o arquivo `alertas.db` automaticamente na raiz do projeto.

## Docker

```bash
docker build -t api-alerta-retorno .
docker run --rm --name alerta-retorno \
  --network mvp-rede \
  -p 8001:8001 \
  api-alerta-retorno
```

Acesse http://127.0.0.1:8001/docs.

Se a rede ainda não existir, crie-a antes dos containers:

```bash
docker network create mvp-rede
```
