# Deploy

## 1. Ambiente local (Docker)

```bash
cp .env.deploy.example .env
docker compose up -d --build
```

| Serviço | URL |
| --- | --- |
| Front-end | http://localhost:3000 |
| API | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| Nginx | http://localhost |

O backend executa `alembic upgrade head` na inicialização e, se `SEED_DEMO_DATA=true`, popula a
base de demonstração.

## 2. Ambiente publicado (Oracle Cloud)

Pré-requisitos:

- VM Ubuntu com Docker e Docker Compose.
- Domínio apontando para o IP da VM (ou proxy Cloudflare).
- Portas 80/443 liberadas; 5432 restrita à rede interna.

Passos:

1. Clonar o repositório na VM.
2. Copiar `.env.deploy.example` para `.env` e preencher credenciais fortes.
3. Subir a stack:

```bash
docker compose -f docker-compose.deploy.yml -p pi2 up -d --build
```

4. Configurar o Nginx do host com o arquivo
   [`infra/nginx/p2.carneirojunior.com.br.conf`](../infra/nginx/p2.carneirojunior.com.br.conf).
5. Emitir o certificado:

```bash
sudo certbot --nginx -d p2.carneirojunior.com.br --redirect
```

6. Validar:

```bash
curl -I https://p2.carneirojunior.com.br
curl https://p2.carneirojunior.com.br/api/v1/restaurants
```

## 3. Cloudflare

- Registro DNS do subdomínio com proxy laranja ativado.
- SSL/TLS em modo **Full (strict)**.
- WAF e proteção contra bots habilitados, se disponíveis no plano.
- Cache apenas para assets estáticos; não cachear `/api/`.

## 4. Backup

```bash
POSTGRES_DB=delivery_db \
POSTGRES_USER=delivery \
POSTGRES_CONTAINER_NAME=pi2_postgres \
BACKUP_DIR=/home/ubuntu/backups/pi2 \
sh infra/backup.sh
```

Agendamento recomendado (cron diário):

```cron
0 2 * * * cd /caminho/do/repositorio && POSTGRES_DB=delivery_db POSTGRES_USER=delivery POSTGRES_CONTAINER_NAME=pi2_postgres BACKUP_DIR=/home/ubuntu/backups/pi2 sh infra/backup.sh >> /home/ubuntu/backups/pi2/backup.log 2>&1
```

## 5. Atualização e rollback

```bash
git pull --ff-only
docker compose -f docker-compose.deploy.yml -p pi2 up -d --build
```

Para rollback:

```bash
git checkout <commit-anterior>
docker compose -f docker-compose.deploy.yml -p pi2 up -d --build
```

As migrations devem ser revertidas com `alembic downgrade <revisão>` quando compatível.

## 6. Checklist de go-live

- [ ] `SECRET_KEY` e senhas fortes.
- [ ] `SEED_DEMO_DATA=false` em produção real.
- [ ] HTTPS válido e renovação automática.
- [ ] Backup testado e restaurável.
- [ ] Logs acessíveis e monitorados.
- [ ] CORS restrito ao domínio.
- [ ] Banco sem porta pública.
- [ ] Smoke test pós-deploy.

## 7. Observabilidade

- Logs do Uvicorn e do Nginx.
- `GET /health` para verificação de saúde da API.
- Monitoramento externo recomendado (UptimeRobot, Better Stack ou equivalente).
