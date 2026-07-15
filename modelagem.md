# Modelagem do FinTrack Insights

## Casos de uso

```mermaid
flowchart LR
    A[Analista de marketing] --> U1((Acessar painel))
    A --> U2((Filtrar clientes))
    A --> U3((Comparar segmentos))
    A --> U4((Consultar insights))
    A --> U5((Registrar plano de campanha))
    G[Gestor comercial] --> U3
    G --> U4
    G --> U6((Revisar plano))
    U2 --> U3
    U3 --> U5
    U4 --> U5
```

## Fluxo de navegação

```mermaid
flowchart TD
    L[Login simulado] --> V[Visão executiva]
    V --> S[Segmentos]
    V --> I[Insights]
    S --> R[Segmento recomendado]
    R --> C[Nova campanha]
    I --> C
    C --> P[Plano salvo para revisão]
    V --> O[Sobre, fonte e limitações]
```

## Estrutura geral

```mermaid
flowchart LR
    CSV[(dados_tratados.csv)] --> CORE[app_core.py\nvalidação e métricas]
    CORE --> DASH[dashboard.py\nStreamlit + Plotly]
    HTML[prototipo_fintrack.html\nHTML, CSS e JS] --> USER[Analista / gestor]
    DASH --> USER
    TEST[scripts e testes] --> CORE
    DOC[README e documentação] --> USER
```

## Rastreabilidade

| Requisito | Evidência |
|---|---|
| RF01 | Tela de login do protótipo |
| RF02 | Indicadores do protótipo e dashboard |
| RF03 | Barra lateral do dashboard |
| RF04 | Gráficos e tabela de segmentos |
| RF05 | Gráfico mensal |
| RF06 | Tabela operacional |
| RF07 | Tela “Nova campanha” |
| RF08 | Expansor de metodologia e tela “Sobre” |
| RNF03 | Estado vazio no dashboard |
| RNF04 | `scripts/validar_dados.py` e `tests/test_app_core.py` |
| RNF06 | Limitações e cuidados visíveis |

