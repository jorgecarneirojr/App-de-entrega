# ADR 0003 — OpenStreetMap, Nominatim e OSRM para mapas e rotas

- **Status:** Aceito
- **Data:** 2026-11-06
- **Contexto:** O checkout precisa exibir mapa, geocodificar endereços e calcular distância/tempo
  sem elevar o custo de operação da microempresa.

## Decisão

Adotar **Leaflet + tiles do OpenStreetMap**, **Nominatim** para geocodificação e **OSRM** para
rotas, com cache e fallback por distância geodésica.

## Justificativa

- Sem chave de API e sem cobrança por requisição.
- Adequado ao MVP e ao orçamento da empresa base.
- Cobertura suficiente para endereços urbanos no Brasil.
- Camada de serviço isolada permite trocar de provedor no futuro.

## Consequências

- Positivas: custo zero, simplicidade de configuração e controle do back-end.
- Negativas: instâncias públicas sem SLA e com políticas de uso; dependência de rede externa.
- Mitigações: cache de 24 h (geocodificação) e 5 min (rotas), fallback local e timeout.
- Alternativas descartadas: Google Maps (custo variável) e Mapbox (token e limite gratuito).

## Evolução

Para escala ou exigência de SLA, substituir por OSRM self-hosted ou provedor comercial.
