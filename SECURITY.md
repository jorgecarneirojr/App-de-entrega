# Política de Segurança

## Versões suportadas

| Versão | Suporte |
| --- | --- |
| 1.x | Sim |
| < 1.0 | Não |

## Como reportar uma vulnerabilidade

Não abra uma issue pública. Utilize o recurso **Security → Report a vulnerability** do GitHub
(Security Advisory) neste repositório. Se o recurso não estiver disponível, entre em contato com
os mantenedores pelo e-mail associado ao commit mais recente.

Inclua, se possível:

- Descrição do problema e impacto.
- Passos para reproduzir.
- Versão/commit afetado.
- Evidências (logs, requisições, capturas) sem dados sensíveis.
- Sugestão de correção, se houver.

## Escopo

Estão no escopo:

- Autenticação e autorização (JWT, RBAC).
- Exposição de dados de usuários, endereços e pedidos.
- Injeção (SQL, XSS, comandos).
- Configuração insegura de containers, Nginx ou banco.
- Exposição de segredos.

Fora do escopo:

- Engenharia social.
- Ataques de negação de serviço em massa.
- Vulnerabilidades em dependências sem impacto demonstrável.
- Ambientes de demonstração com dados fictícios, salvo exposição de segredos reais.

## Controles adotados

- Hash de senhas com bcrypt.
- JWT com expiração e verificação de perfil.
- CORS restrito.
- Segredos fora do repositório.
- Banco sem exposição pública.
- Backup diário.
- Dependências e imagem base atualizáveis.

## Divulgação responsável

Pedimos um prazo razoável para correção antes de qualquer divulgação pública. Reconheceremos a
contribuição quando apropriado.
