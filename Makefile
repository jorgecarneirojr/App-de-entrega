.PHONY: help up down logs build test lint typecheck smoke backup deploy check

help:
	@echo "Comandos disponíveis:"
	@echo "  make up          Sobe a stack local com Docker Compose"
	@echo "  make down        Derruba a stack local"
	@echo "  make logs        Exibe logs da stack local"
	@echo "  make build       Rebuild da stack local"
	@echo "  make test        Executa os testes de API"
	@echo "  make lint        Executa o lint do backend (Ruff)"
	@echo "  make typecheck   Executa o typecheck do frontend"
	@echo "  make smoke       Executa o smoke test do frontend"
	@echo "  make check       Executa lint + testes + typecheck"
	@echo "  make backup      Executa o backup do banco publicado"
	@echo "  make deploy      Sobe a stack de produção (Oracle Cloud)"

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

build:
	docker compose build

test:
	cd backend && python -m unittest discover -s tests -v

lint:
	cd backend && ruff check app tests

typecheck:
	cd frontend && npm run typecheck

smoke:
	cd frontend && npm run smoke

check: lint test typecheck

backup:
	POSTGRES_DB=$${POSTGRES_DB:-delivery_db} POSTGRES_USER=$${POSTGRES_USER:-delivery} POSTGRES_CONTAINER_NAME=$${POSTGRES_CONTAINER_NAME:-pi2_postgres} BACKUP_DIR=$${BACKUP_DIR:-./backups} sh infra/backup.sh

deploy:
	docker compose -f docker-compose.deploy.yml -p pi2 up -d --build
