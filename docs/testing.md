# Estratégia de Testes

A qualidade é tratada em quatro frentes: testes automatizados de API, verificação estática,
validação de build e smoke test de interface. O objetivo é cobrir os fluxos críticos de negócio
e detectar regressões antes da publicação.

## 1. Pirâmide adotada

```text
        Smoke test (páginas principais)
      Build de produção + typecheck
    Testes de API (unittest) + lint (ruff)
```

- **Testes de API:** exercitam autenticação, pedidos, entregas, coordenadas e rotas.
- **Lint e typecheck:** reduzem erros de importação, tipagem e estilo.
- **Build:** garante que o front-end compila em modo produção.
- **Smoke test:** verifica disponibilidade das páginas principais.

## 2. Matriz de testes automatizados

| # | Cenário | Tipo | Resultado esperado |
| --- | --- | --- | --- |
| 1 | Cadastro, login e `GET /auth/me` | API | Usuário autenticado e perfil retornado |
| 2 | Criação de pedido com endereço real | API | Pedido e itens persistidos com totais corretos |
| 3 | Atribuição de entregador e atualização da entrega | API | Delivery criada e status atualizado |
| 4 | Pedido com produto inexistente | API | `404` |
| 5 | Validação de latitude/longitude | API | `422` para valores fora dos limites |
| 6 | Persistência de coordenadas explícitas | API | Latitude/longitude retornadas no endereço |
| 7 | Rota com distância e geometria | API | `distance_km`, `duration_min` e `geometry` |
| 8 | Coordenadas inválidas na rota | API | `422` |
| 9 | Cardápio retorna `category_name` | API | Produto agrupado por categoria |

Além dos testes, o front-end passa por `npm run typecheck`, `npm run build` e `npm run smoke`.

## 3. Como executar

```bash
# Backend
cd backend
python -m unittest discover -s tests -v
ruff check app tests

# Frontend
cd frontend
npm run typecheck
npm run build
npm run smoke
```

## 4. Integração contínua

O workflow [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) executa em cada push e pull
request para `main`:

1. **Backend:** instala dependências, roda Ruff e os 9 testes de API.
2. **Frontend:** instala com `npm ci`, roda typecheck, build e smoke test.

O CI usa cache de dependências e cancela execuções antigas do mesmo branch.

## 5. Testes manuais recomendados

| Fluxo | Verificação |
| --- | --- |
| Cadastro/login | Mensagens de erro, persistência da sessão e logout |
| Cardápio | Produtos indisponíveis não aparecem |
| Carrinho | Quantidades, remoção e persistência após recarregar |
| Checkout | Endereço obrigatório e bloqueio sem autenticação |
| Rota | Mapa, marcadores, distância e tempo coerentes |
| Restaurante | CRUD de produtos e atualização de status |
| Entregador | Corrida ativa, status e envio de localização |
| Responsividade | 390 px sem rolagem horizontal |

## 6. Limitações

- Não há testes end-to-end automatizados com navegador.
- A cobertura de código não é medida nem exigida no CI.
- Testes de carga e de segurança automatizados não fazem parte do escopo atual.
- A auditoria de acessibilidade é automatizada (axe-core) e não substitui avaliação manual.

## 7. Evolução

- Adicionar testes E2E com Playwright para checkout e painel do restaurante.
- Medir cobertura com `coverage.py` e definir metas por camada.
- Adicionar testes de contrato da API.
- Incluir análise de dependências e SAST no CI.
