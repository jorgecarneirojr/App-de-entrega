# Como Contribuir

Obrigado pelo interesse no projeto. Este documento descreve o fluxo de contribuição, os padrões
de código e os critérios de aceite.

## 1. Pré-requisitos

- Python 3.11+
- Node.js 20+
- Docker e Docker Compose (opcional, mas recomendado)
- Git

## 2. Configuração do ambiente

```bash
git clone https://github.com/jorgecarneirojr/App-de-entrega.git
cd App-de-entrega

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# Frontend
cd ../frontend
npm install
```

## 3. Fluxo de trabalho

1. Atualize a `main`: `git pull --ff-only origin main`.
2. Crie uma branch descritiva: `feat/mapa-rota`, `fix/validacao-endereco`, `docs/adr`.
3. Implemente a mudança com testes e documentação.
4. Execute as verificações locais.
5. Abra um Pull Request usando o template.

## 4. Padrões de commit

Utilize **Conventional Commits**:

```text
feat: adiciona cálculo de rota no checkout
fix: corrige validação de latitude
docs: atualiza contrato da API
test: cobre criação de pedido sem endereço
refactor: extrai serviço de geocodificação
chore: atualiza dependências
```

## 5. Verificações obrigatórias

```bash
# Backend
cd backend
ruff check app tests
python -m unittest discover -s tests -v

# Frontend
cd frontend
npm run typecheck
npm run build
npm run smoke
```

O CI executa as mesmas verificações. Pull requests com falha não são integrados.

## 6. Padrões de código

- Python: PEP 8, tipagem quando possível, funções pequenas e nomes descritivos.
- TypeScript: componentes funcionais, tipos explícitos e sem `any` desnecessário.
- SQL: migrations versionadas e compatíveis com PostgreSQL.
- Documentação: atualizar README/docs quando o comportamento mudar.
- Acessibilidade: rótulos, foco visível, contraste e semântica.

## 7. Critérios de aceite do PR

- [ ] A mudança resolve um problema descrito.
- [ ] Testes passam localmente.
- [ ] Lint e typecheck passam.
- [ ] Documentação atualizada (quando aplicável).
- [ ] Sem segredos, dados pessoais ou arquivos gerados no commit.
- [ ] Mensagem de commit no padrão.

## 8. Segurança

Não abra issues públicas para vulnerabilidades. Consulte [`SECURITY.md`](SECURITY.md).

## 9. Código de conduta

Ao contribuir, você concorda com o [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
