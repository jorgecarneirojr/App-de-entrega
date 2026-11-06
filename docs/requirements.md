# Requisitos

Especificação resumida dos requisitos do MVP, com rastreabilidade para endpoints e testes.
A fonte de verdade da API é o OpenAPI publicado em `/docs`.

## 1. Atores

| Ator | Descrição |
| --- | --- |
| Cliente | Pessoa que consulta restaurantes e realiza pedidos |
| Dono de restaurante | Responsável pelo catálogo e pelos pedidos do estabelecimento |
| Entregador | Responsável pela retirada e entrega do pedido |
| Administrador | Perfil com acesso administrativo |

## 2. Requisitos funcionais

| ID | Requisito | Ator | Endpoint principal | Teste |
| --- | --- | --- | --- | --- |
| RF01 | Cadastrar, autenticar e consultar o perfil | Todos | `/auth/*` | `test_register_and_login_flow` |
| RF02 | Gerenciar endereços do cliente | Cliente | `/addresses` | `test_address_keeps_explicit_coordinates` |
| RF03 | Listar restaurantes e consultar cardápio | Cliente | `/restaurants`, `/restaurants/{id}/menu` | Smoke/manual |
| RF04 | Montar carrinho e criar pedido com endereço real | Cliente | `/orders` | `test_client_can_create_order_with_real_address` |
| RF05 | Consultar histórico de pedidos | Cliente | `/orders/me` | Manual |
| RF06 | Gerenciar produtos do restaurante | Restaurante | `/products/*` | Manual |
| RF07 | Atualizar status do pedido | Restaurante | `/orders/{id}/status` | `test_owner_assigns_courier_and_courier_updates_delivery` |
| RF08 | Vincular entregador ao pedido | Restaurante | `/orders/{id}/assign-courier` | `test_owner_assigns_courier_and_courier_updates_delivery` |
| RF09 | Atualizar status e localização da entrega | Entregador | `/deliveries/{id}/status`, `/deliveries/{id}/location` | `test_update_location_validates_latitude_and_longitude` |
| RF10 | Calcular rota, distância e tempo | Cliente | `/geo/route` | `test_geo_route_returns_distance_and_geometry` |
| RF11 | Geocodificar endereços | Sistema | `/geo/geocode` | Manual/integração |
| RF12 | População de demonstração idempotente | Sistema | `SEED_DEMO_DATA` | Manual |

## 3. Requisitos não funcionais

| ID | Requisito | Implementação |
| --- | --- | --- |
| RNF01 | API REST documentada | OpenAPI/Swagger |
| RNF02 | Banco relacional com migrations | PostgreSQL + Alembic |
| RNF03 | Back-end em FastAPI e front-end em Next.js | Stack definida em ADR 0001 |
| RNF04 | Deploy em nuvem com Docker | ADR 0004 |
| RNF05 | HTTPS e proxy reverso | Nginx + Let's Encrypt + Cloudflare |
| RNF06 | Backup diário | `infra/backup.sh` + cron |
| RNF07 | Acessibilidade WCAG 2 A/AA | Painel de ajustes, práticas ARIA, página `/acessibilidade` e auditoria axe-core |
| RNF08 | Responsividade | Layout adaptável, verificado em 390 px |
| RNF09 | Qualidade automatizada | Ruff, unittest, typecheck, build, smoke e CI |
| RNF10 | Segurança | JWT, bcrypt, RBAC, CORS e segredos fora do repositório |
| RNF11 | Manutenibilidade | Camadas, tipagem, documentação e ADRs |
| RNF12 | Reprodutibilidade | Docker Compose, migrations e seed |

## 4. Histórias de usuário (amostra)

- **US01** — Como cliente, quero consultar o cardápio para escolher produtos antes de pedir.
- **US02** — Como cliente, quero salvar meus endereços para agilizar o checkout.
- **US03** — Como cliente, quero visualizar a distância e o tempo da entrega para decidir a compra.
- **US04** — Como restaurante, quero atualizar o status do pedido para informar o cliente.
- **US05** — Como restaurante, quero vincular um entregador para organizar a operação.
- **US06** — Como entregador, quero ver minhas entregas ativas e registrar a localização.

## 5. Regras de negócio

- Pedido exige cliente autenticado, restaurante, endereço e ao menos um item.
- Preço unitário é congelado no item do pedido.
- Totais são calculados no back-end.
- Coordenadas devem estar entre -90/90 (latitude) e -180/180 (longitude).
- Cada pedido possui no máximo uma entrega.
- Entregador só atualiza entregas atribuídas a ele.

## 6. Fora de escopo

- Gateway de pagamento real.
- Notificações push.
- Aplicativo móvel nativo.
- Rastreamento em tempo real com streaming.
- Integração com o CRM do PI1 (roadmap).
