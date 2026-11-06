# Backend — FastAPI

API REST do App de Entrega. Documentação completa em [`../docs/api-contract.md`](../docs/api-contract.md)
e Swagger em `/docs`.

## Requisitos

- Python 3.11+
- PostgreSQL 16 (ou Docker Compose)

## Execução local

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Qualidade

```bash
ruff check app tests
python -m unittest discover -s tests -v
```

## Estrutura

```text
app/
├── api/          # Rotas e dependências
├── core/         # Configuração e segurança
├── db/           # Sessão e base declarativa
├── models/       # Entidades SQLAlchemy
├── schemas/      # Contratos Pydantic
└── services/     # Regras de negócio
alembic/          # Migrations
tests/            # Testes de API
```

## Variáveis

Consulte [`../.env.deploy.example`](../.env.deploy.example) e [`../README.md`](../README.md).
