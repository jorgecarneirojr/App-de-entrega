# Frontend — Next.js

Interface web do App de Entrega, construída com Next.js 14, TypeScript, Tailwind CSS, React Query
e Zustand.

## Execução local

```bash
cp .env.example .env.local
npm install
npm run dev
```

Aplicação: http://localhost:3000

## Scripts

```bash
npm run dev        # Desenvolvimento
npm run build      # Build de produção
npm run start      # Produção
npm run typecheck  # TypeScript
npm run smoke      # Smoke test
```

## Estrutura

```text
app/          # Rotas (App Router)
components/   # Componentes e mapa
lib/          # Cliente HTTP e tipos
store/        # Auth e carrinho
```

## Acessibilidade

Práticas e auditoria em [`../docs/accessibility.md`](../docs/accessibility.md).
