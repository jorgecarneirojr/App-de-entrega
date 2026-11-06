# Contrato da API (v1)

- **Base URL local:** `http://localhost:8000`
- **Base URL publicada:** `https://p2.carneirojunior.com.br`
- **Prefixo:** `/api/v1`
- **Autenticação:** `Authorization: Bearer <token>`
- **Documentação interativa:** `/docs`
- **OpenAPI:** `/openapi.json`

## 1. Autenticação

### `POST /auth/register`

```json
{
  "name": "Cliente Demo",
  "email": "cliente@exemplo.com",
  "password": "123456",
  "role": "cliente"
}
```

### `POST /auth/login`

```json
{
  "email": "client@demo.com",
  "password": "123456"
}
```

Resposta:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

### `GET /auth/me`

Retorna o usuário autenticado.

## 2. Endereços

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/addresses` | Lista endereços do usuário |
| POST | `/addresses` | Cria endereço (geocodifica se faltarem coordenadas) |
| PUT | `/addresses/{id}` | Atualiza endereço |
| DELETE | `/addresses/{id}` | Remove endereço |

Campos: `street`, `number`, `district`, `city`, `state`, `zip_code`, `complement`,
`reference`, `latitude`, `longitude`.

## 3. Restaurantes e produtos

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/restaurants` | Lista restaurantes ativos |
| GET | `/restaurants/mine` | Restaurantes do dono autenticado |
| POST | `/restaurants` | Cria restaurante (geocodifica o endereço) |
| GET | `/restaurants/{id}` | Detalhe |
| GET | `/restaurants/{id}/menu` | Cardápio agrupado |
| GET | `/products/restaurant/{id}` | Produtos do restaurante |
| POST | `/products` | Cria produto |
| PUT | `/products/{id}` | Atualiza produto |
| DELETE | `/products/{id}` | Remove produto |

## 4. Pedidos

| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/orders` | Cria pedido com endereço real |
| GET | `/orders/me` | Pedidos do usuário conforme perfil |
| PATCH | `/orders/{id}/status` | Atualiza status (restaurante) |
| PATCH | `/orders/{id}/assign-courier` | Vincula entregador |

Exemplo de criação:

```json
{
  "restaurant_id": 1,
  "delivery_address_id": 1,
  "items": [
    { "product_id": 1, "quantity": 2 }
  ],
  "notes": "Sem cebola"
}
```

Erros: `404` para produto inexistente; `401` sem autenticação; `403` sem permissão.

## 5. Entregas

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/deliveries/me/active` | Entregas ativas do entregador |
| PATCH | `/deliveries/{id}/status` | Atualiza status |
| POST | `/deliveries/{id}/location` | Registra latitude/longitude |

Validação de coordenadas: latitude `-90..90`, longitude `-180..180`.

## 6. Geolocalização

### `GET /geo/geocode?q={endereco}`

```json
{
  "latitude": -22.7305,
  "longitude": -45.1235,
  "display_name": "Lorena, São Paulo, Brasil"
}
```

### `GET /geo/route?from_lat=&from_lon=&to_lat=&to_lon=`

```json
{
  "distance_km": 1.58,
  "duration_min": 3,
  "geometry": [[-22.7305, -45.1235], [-22.7262, -45.1138]],
  "source": "osrm"
}
```

`source` indica `osrm` (rota real) ou `estimado` (fallback geodésico).

## 7. Códigos de status

| Código | Significado |
| --- | --- |
| 200 | Sucesso |
| 201 | Criado (quando aplicável) |
| 401 | Token ausente/inválido |
| 403 | Perfil sem permissão |
| 404 | Recurso não encontrado |
| 422 | Validação de entrada |
| 500 | Erro interno |

## 8. Boas práticas de consumo

- Enviar `Content-Type: application/json` em POST/PUT/PATCH.
- Renovar o token antes da expiração.
- Tratar `detail` das respostas de erro.
- Não cachear respostas autenticadas no CDN.
