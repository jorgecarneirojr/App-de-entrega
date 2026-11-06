# ADR 0002 — PostgreSQL com migrations Alembic

- **Status:** Aceito
- **Data:** 2026-08-29
- **Contexto:** O domínio envolve usuários, endereços, restaurantes, produtos, pedidos, pagamentos
  e entregas, com forte integridade referencial.

## Decisão

Usar **PostgreSQL 16** e versionar o esquema com **Alembic**.

## Justificativa

- Integridade referencial, transações e tipos robustos.
- Suporte a enums nativos, `numeric` para valores monetários e timestamps com fuso.
- Migrations versionadas permitem evolução segura do esquema.
- Docker facilita a paridade entre desenvolvimento e produção.

## Consequências

- Positivas: consistência, integridade e rastreabilidade das mudanças.
- Negativas: enums exigem cuidado em migrations; testes usam SQLite e podem divergir do
  PostgreSQL em detalhes de DDL.
- Alternativas descartadas: SQLite (limitações de concorrência e tipos) e MySQL (menor aderência
  aos recursos utilizados).

## Observação

A migration inicial foi ajustada para evitar criação duplicada de enums no PostgreSQL, um problema
que não aparece em SQLite.
