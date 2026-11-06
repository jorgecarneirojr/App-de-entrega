# ADR 0001 — FastAPI no back-end e Next.js no front-end

- **Status:** Aceito
- **Data:** 2026-08-29
- **Contexto:** O projeto exige uma API REST documentada, autenticação, validação e uma interface
  web responsiva, com prazo acadêmico curto e equipe pequena.

## Decisão

Adotar **FastAPI + SQLAlchemy** no back-end e **Next.js 14 + TypeScript** no front-end.

## Justificativa

- FastAPI gera OpenAPI automaticamente e integra validação com Pydantic.
- SQLAlchemy e Alembic oferecem ORM maduro e migrations versionadas.
- Next.js fornece roteamento, build otimizado, SSR quando necessário e ecossistema React.
- TypeScript reduz erros de integração entre front-end e API.

## Consequências

- Positivas: produtividade, documentação automática, tipagem e ecossistema.
- Negativas: duas stacks e dois processos de build; exige CI separado.
- Alternativas descartadas: Django (mais acoplado ao ORM e admin), Flask (menos validação nativa)
  e Rails (fora do domínio da equipe).
