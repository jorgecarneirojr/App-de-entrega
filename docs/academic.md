# Contexto Acadêmico e Metodologia

Este documento sintetiza o enquadramento acadêmico do projeto, complementando o relatório final
entregue à disciplina. O objetivo é tornar explícitos o problema, os objetivos, a metodologia, os
resultados e as limitações para leitores do repositório.

## 1. Identificação

| Item | Descrição |
| --- | --- |
| Instituição | Universidade Virtual do Estado de São Paulo (UNIVESP) |
| Disciplina | PJI240 — Projeto Integrador em Computação II |
| Curso | Eixo da Computação |
| Polo | Lorena/SP |
| Orientador | Prof. Lucas Secarelli Laureano Tostes |
| Empresa base | Açaiteria Combina Açaí — Lorena/SP |
| Tema norteador | Tecnologia aplicada à digitalização e à melhoria de processos em micro e pequenas empresas do setor de alimentação |

## 2. Problema de pesquisa

A empresa base atende pedidos predominantemente por telefone e WhatsApp, sem registro
consolidado, sem cardápio digital próprio e dependente de plataformas agregadoras que cobram
comissões elevadas. A questão central é:

> Como uma plataforma de delivery própria pode melhorar os processos de atendimento e reduzir
> custos de um pequeno restaurante?

## 3. Objetivos

**Geral:** desenvolver e implantar uma plataforma de delivery própria para a empresa base,
digitalizando o fluxo de cardápio, pedido, rota e entrega.

**Específicos:**

- Implementar cardápio digital e gestão de produtos.
- Permitir pedidos com endereço real e histórico.
- Fornecer painel ao restaurante e ao entregador.
- Calcular rota, distância e tempo entre loja e endereço.
- Aplicar boas práticas de acessibilidade, testes, versionamento e implantação em nuvem.

## 4. Metodologia

- **Natureza:** pesquisa aplicada.
- **Abordagem:** qualitativa.
- **Estratégia:** estudo de caso.
- **Método de design:** Design Centrado no Ser Humano (HCD) e Design Thinking, em ciclos de
  escuta, criação e implementação.
- **Coleta:** entrevista semiestruturada com o proprietário e observação direta, realizadas em
  visita presencial em 29 de agosto de 2026.
- **Análise:** análise de conteúdo, com categorização dos relatos em requisitos, casos de uso,
  modelo de dados e protótipos.

### Considerações éticas

A pesquisa adotou minimização de dados e consentimento informado. Foram utilizados o Termo de
Autorização da Empresa e o Termo de Consentimento Livre e Esclarecido, mantidos nos documentos
do projeto. Não foram coletados dados sensíveis, e a base de demonstração contém apenas dados
fictícios.

## 5. Continuidade com o PI1

O PI1 desenvolveu um CRM para gestão interna de clientes, vendas, produtos, pagamentos e
estoque na mesma empresa base. O PI2 complementa o CRM ao digitalizar o canal externo de
pedidos e entregas. A Tabela abaixo sintetiza a complementaridade.

| Dimensão | PI1 — CRM | PI2 — Delivery |
| --- | --- | --- |
| Foco | Gestão interna | Canal externo de pedidos |
| Usuários | Equipe do balcão | Cliente, restaurante e entregador |
| Funções | Clientes, vendas, estoque, pagamentos | Cardápio, carrinho, rota, pedido e entrega |
| Resultado | Organização da operação | Digitalização do pedido e da entrega |

## 6. Resultados

- Aplicação publicada em nuvem com HTTPS: https://p2.carneirojunior.com.br.
- Seis restaurantes e cardápios de demonstração, com pedidos em diferentes estados.
- Quatro perfis de acesso com autenticação JWT.
- Checkout com endereço real e mapa de rota (OpenStreetMap/OSRM), com distância e tempo.
- Oito testes de API, lint com Ruff, typecheck, build e smoke test no CI.
- Auditoria de acessibilidade com axe-core (WCAG 2 A/AA) sem violações nas telas avaliadas.
- Documentação técnica, ADRs, políticas e guias de reprodução no repositório.

## 7. Contribuições

1. **Para a empresa base:** canal digital próprio, com redução de dependência de intermediários
   e centralização do histórico de pedidos.
2. **Para a comunidade acadêmica:** aplicação integrada de engenharia de software, banco de
   dados, APIs, acessibilidade e implantação em nuvem em um caso real.
3. **Para a engenharia:** documentação reprodutível, decisões arquiteturais registradas e
   automação de qualidade.

## 8. Limitações e ameaças à validade

- **Validade de constructo:** os indicadores (testes, auditoria automatizada, build) medem
  qualidade técnica, não adoção real em larga escala.
- **Validade interna:** estudo de caso único, sem grupo de controle; melhorias percebidas podem
  sofrer influência de fatores externos.
- **Validade externa:** os resultados não são generalizáveis automaticamente para outros
  contextos e portes de empresa.
- **Confiabilidade:** o código e o ambiente são versionados, mas a análise qualitativa não foi
  submetida a codificação por múltiplos pesquisadores.
- **Escopo:** não há gateway de pagamento, notificações push, aplicativo nativo nem rastreamento
  em tempo real.

## 9. Reprodutibilidade

- Código público sob licença MIT.
- Ambiente conteinerizado com Docker Compose.
- Migrations versionadas e base de demonstração idempotente.
- Scripts de teste, lint, typecheck, build e smoke test documentados.
- API documentada via OpenAPI/Swagger.
- Dados de demonstração fictícios, sem dados pessoais reais.

## 10. Entregáveis acadêmicos

- Relatório final (documento institucional).
- Plano de ação.
- Relatório parcial.
- Avaliação colaborativa.
- Ficha técnica e vídeo de apresentação: https://www.youtube.com/watch?v=ZHFJPzqw1f0.
- Termo de Autorização da Empresa e Termo de Consentimento Livre e Esclarecido.

## 11. Como citar

Consulte [`CITATION.cff`](../CITATION.cff).
