# ADR 0005 — Acessibilidade e automação de qualidade no CI

- **Status:** Aceito
- **Data:** 2026-11-06
- **Contexto:** O projeto precisa atender requisitos de acessibilidade e manter qualidade com
  uma equipe pequena e entregas frequentes.

## Decisão

Incorporar acessibilidade desde a implementação e automatizar lint, testes, typecheck, build e
smoke test no GitHub Actions.

## Justificativa

- Acessibilidade é requisito de qualidade e inclusão, não etapa posterior.
- Ruff, TypeScript e testes reduzem regressões de baixo custo.
- O CI garante que o repositório permaneça reproduzível.

## Consequências

- Positivas: detecção precoce de erros, documentação viva e confiança no merge.
- Negativas: tempo de CI maior e necessidade de manter dependências de desenvolvimento.
- A auditoria automatizada com axe-core não substitui testes manuais com leitores de tela.

## Práticas

- HTML semântico, `lang`, rótulos, `aria-live`, foco visível e `prefers-reduced-motion`.
- Checklist manual em [`../accessibility.md`](../accessibility.md).
