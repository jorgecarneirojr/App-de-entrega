# ADR 0004 — Deploy com Docker Compose, Nginx e Cloudflare

- **Status:** Aceito
- **Data:** 2026-11-06
- **Contexto:** A aplicação precisa ser publicada em nuvem com HTTPS, baixo custo e operação
  simples por uma equipe pequena.

## Decisão

Publicar com **Docker Compose** em uma VM Oracle Cloud, **Nginx** como proxy reverso e
**Cloudflare** como CDN/proxy, com certificado **Let's Encrypt**.

## Justificativa

- Docker Compose é suficiente para três serviços e tem custo operacional baixo.
- Nginx termina TLS, serve o front-end e encaminha `/api/` para o back-end.
- Cloudflare adiciona DNS, HTTPS e proteção sem alterar a aplicação.
- Let's Encrypt automatiza a emissão e renovação do certificado.

## Consequências

- Positivas: simplicidade, reprodutibilidade e custo compatível.
- Negativas: sem orquestração avançada, auto-scaling ou alta disponibilidade nativa.
- Alternativas descartadas: Kubernetes (complexidade desproporcional) e PaaS (custo/limites).
