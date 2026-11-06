# Segurança e Privacidade

Este documento descreve os controles adotados, as limitações e as recomendações para operação.

## 1. Autenticação e autorização

- Senhas armazenadas com **bcrypt**; nunca em texto puro.
- Tokens **JWT** assinados com HS256 e expiração configurável.
- Perfis: `cliente`, `dono_restaurante`, `entregador`, `admin`.
- Endpoints sensíveis usam dependências de autenticação e verificação de perfil.
- O front-end persiste o token no `localStorage` (decisão de MVP); em evolução, recomenda-se
  cookie `HttpOnly` + `SameSite`.

## 2. Proteção de dados

- O banco PostgreSQL não publica porta no host; o acesso ocorre pela rede interna do Docker.
- CORS restrito ao domínio publicado.
- Segredos ficam em `.env`, ignorado pelo Git; `.env.deploy.example` contém apenas placeholders.
- Dados de demonstração são fictícios.
- Nenhum dado real de cliente é versionado no repositório.
- Backup diário com `pg_dump`, armazenado fora do container.

## 3. APIs externas

- Nominatim e OSRM são chamados pelo back-end, não pelo navegador.
- Apenas endereço/coordenadas são enviados; não há dados pessoais do cliente.
- Cache de geocodificação (24 h) e rotas (5 min) reduz o volume de chamadas.
- Fallback local evita indisponibilidade total quando o OSRM falha.
- As instâncias públicas não oferecem SLA; para produção crítica, recomenda-se provedor com
  contrato ou OSRM self-hosted.

## 4. LGPD

O projeto adota minimização de dados:

- Coleta apenas dados necessários ao pedido: nome, e-mail, endereço e itens.
- Não coleta dados sensíveis.
- O Termo de Consentimento Livre e Esclarecido e o Termo de Autorização da Empresa estão
  disponíveis nos documentos do projeto.
- O titular pode solicitar exclusão dos dados; o modelo permite exclusão de endereços e usuários
  respeitando o histórico de pedidos.
- Recomenda-se, para produção, política de retenção, anonimização e trilha de auditoria.

## 5. Hardening recomendado

- Trocar `SECRET_KEY` e senhas padrão antes do deploy.
- Usar senhas fortes e únicas para o PostgreSQL.
- Manter dependências atualizadas (`pip-audit`, `npm audit`).
- Restringir acesso SSH por chave.
- Monitorar logs e alertas de erro.
- Configurar rate limiting no Nginx/Cloudflare.
- Ativar WAF e proteção contra bots na Cloudflare.
- Revisar permissões de arquivos e backups.

## 6. Limitações

- Não há rate limiting na aplicação.
- Não há autenticação de dois fatores.
- Não há auditoria persistente de ações administrativas.
- O token no `localStorage` é vulnerável a XSS; a mitigação depende da ausência de injeção e de
  sanitização do conteúdo.

## 7. Reportar vulnerabilidades

Consulte [`SECURITY.md`](../SECURITY.md) para o canal de contato e o escopo.
