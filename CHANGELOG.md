# Changelog

Todas as mudanças relevantes deste projeto são documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o projeto adota
[Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não publicado]

### Planejado

- Integração com gateway de pagamento.
- Notificações automáticas de status.
- Rastreamento em tempo real com mapa.
- Integração com o CRM do PI1.
- Testes E2E com Playwright.

## [1.1.0] — 2026-11-06

### Adicionado

- Cardápio real da Combina Açaí (33 itens em 7 categorias) e agrupamento por categoria na interface.
- Mapa de rota com Leaflet/OpenStreetMap, distância e tempo via OSRM.
- Geocodificação de endereços e restaurantes com Nominatim.
- Cache de geocodificação (24 h) e rotas (5 min) e fallback geodésico.
- Migração `0002_geo_coordinates`.
- Testes de coordenadas, rota e categorias do cardápio.
- Documentação de arquitetura, modelo de dados, testes, acessibilidade, segurança, deploy e ADRs.
- Templates de issue/PR, política de segurança, código de conduta e citação.
- Lint com Ruff, typecheck no CI e `requirements-dev.txt`.

### Alterado

- README reescrito com contexto acadêmico, capturas, arquitetura e guias.
- CI com jobs separados, cache e `npm ci`.
- Acessibilidade reforçada: painel de ajustes (texto, alto contraste e movimento), anúncio de rota, resumo textual do mapa e página `/acessibilidade`.
- Rótulos, ARIA, foco visível, erros associados aos campos e `prefers-reduced-motion`.

### Corrigido

- Criação duplicada de enums na migration inicial no PostgreSQL.

## [1.0.0] — 2026-10-26

### Adicionado

- Autenticação JWT e perfis de acesso.
- Cardápio, carrinho e checkout.
- Gestão de produtos e pedidos.
- Painel do entregador e localização.
- Docker Compose, Nginx e deploy em nuvem.
- Testes de API e CI inicial.

## [0.1.0] — 2026-08-31

### Adicionado

- Estrutura inicial do backend FastAPI e do frontend Next.js.
- Modelo de dados e migrations.
- Plano de ação do projeto.
