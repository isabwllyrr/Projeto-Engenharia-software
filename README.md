# FinTrack Insights — Inteligência para Campanhas Bancárias

**APS — Engenharia de Software para Negócios — UFPB (2026.1)**

**Entrega:** AV2 — Protótipo de Software Orientado a Dados

**Equipe:** Isabelly Rodrigues, Maria Dionila e Maria Carolina

**Professor:** Alandey Severo Leite da Silva

## Resumo

O FinTrack Insights é um protótipo de apoio à decisão para equipes de marketing bancário. A solução integra um protótipo navegável e um dashboard interativo para analisar o desempenho histórico de campanhas de depósito a prazo, comparar segmentos e documentar critérios de priorização. O projeto utiliza uma amostra pública tratada do Bank Marketing Dataset, com 4.521 clientes e 18 campos. Na amostra, 521 clientes aderiram ao produto, correspondendo a uma taxa geral de 11,52%. A proposta não automatiza decisões individuais: apresenta evidências agregadas e limitações para apoiar análise humana responsável.

## Problema e público-alvo

Campanhas de marketing direto podem consumir tempo e capacidade operacional quando são planejadas sem evidências sobre volume, perfil e histórico de resposta. O problema abordado é a dificuldade de transformar registros de campanhas anteriores em informações compreensíveis para priorizar segmentos.

O público-alvo são analistas de marketing, gestores comerciais e profissionais responsáveis pelo planejamento e acompanhamento de campanhas bancárias.

## Objetivos

### Objetivo geral

Desenvolver um protótipo orientado a dados que ajude equipes bancárias a explorar o histórico de campanhas, comparar segmentos e justificar decisões de priorização.

### Objetivos específicos

- apresentar indicadores de clientes, adesões, taxa de adesão e saldo médio;
- permitir filtros por profissão, escolaridade, tipo de contato e idade;
- comparar taxa e volume para evitar decisões baseadas apenas em percentuais;
- registrar um plano de campanha com segmento e justificativa;
- explicitar fonte, definições, limitações e cuidados de uso;
- validar a experiência do protótipo com usuários por meio do SUS.

## Fonte de dados

O projeto usa o **Bank Marketing Dataset**, relacionado a campanhas telefônicas de uma instituição bancária portuguesa. O arquivo tratado deste repositório corresponde à amostra `bank.csv`, com 4.521 registros e 17 variáveis originais, acrescida de `cliente_id`.

- Fonte oficial: [UCI Machine Learning Repository — Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank)
- Autores: S. Moro, P. Rita e P. Cortez
- DOI: [10.24432/C5K306](https://doi.org/10.24432/C5K306)
- Licença da fonte: CC BY 4.0
- Unidade de análise: cliente contatado em campanha
- Variável de resultado: adesão a depósito a prazo

O [dicionário de dados](docs/dicionario_dados.md) registra o significado das colunas e as transformações aplicadas.

## Principais achados da amostra

- 4.521 clientes e 521 adesões;
- taxa geral de adesão de **11,52%**;
- clientes com sucesso em campanha anterior apresentam taxa de **64,34%** (`n=129`);
- aposentados apresentam taxa de **23,48%** (`n=230`);
- estudantes apresentam taxa de **22,62%** (`n=84`);
- contatos sem tipo informado apresentam taxa inferior aos contatos por celular ou telefone.

Os resultados são descritivos. Grupos pequenos podem apresentar percentuais instáveis e não devem ser interpretados como causalidade ou previsão individual.

## Requisitos

### Funcionais

- **RF01:** permitir acesso simulado ao protótipo;
- **RF02:** exibir indicadores gerais da campanha;
- **RF03:** filtrar clientes por características disponíveis;
- **RF04:** comparar segmentos por taxa de adesão e volume;
- **RF05:** apresentar evolução por mês de contato;
- **RF06:** consultar tabela operacional de segmentos;
- **RF07:** registrar um plano simulado de campanha;
- **RF08:** informar fonte, definições e limitações dos dados.

### Não funcionais

- **RNF01:** interface responsiva e legível em desktop e dispositivos móveis;
- **RNF02:** carregamento local da base com cache do Streamlit;
- **RNF03:** mensagens claras para filtros sem resultados;
- **RNF04:** métricas reconciliáveis com a base tratada;
- **RNF05:** contraste e hierarquia visual consistentes;
- **RNF06:** uso agregado e responsável, sem decisão automatizada sobre indivíduos;
- **RNF07:** usabilidade avaliada por teste com usuários e questionário SUS antes da entrega final.

## Modelagem

A modelagem contempla casos de uso, fluxo de navegação, componentes e rastreabilidade entre requisitos e telas. Consulte [docs/modelagem.md](docs/modelagem.md).

## Entregas da AV2

1. **Protótipo navegável:** [`prototipo_fintrack.html`](prototipo_fintrack.html)
2. **Elemento de dados:** [`dashboard.py`](dashboard.py)
3. **Apresentação:** [`docs/FinTrack_Insights_AV2.pptx`](docs/FinTrack_Insights_AV2.pptx)
4. **Modelagem:** [`docs/modelagem.md`](docs/modelagem.md)
5. **Plano de validação SUS:** [`docs/validacao_sus.md`](docs/validacao_sus.md)

## Como executar

Consulte [COMO_RODAR.md](COMO_RODAR.md). Resumo:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run dashboard.py
```

O protótipo não precisa de servidor: abra `prototipo_fintrack.html` no navegador.

## Estrutura

```text
.
├── .streamlit/config.toml
├── app_core.py
├── dashboard.py
├── dados_tratados.csv
├── prototipo_fintrack.html
├── requirements.txt
├── COMO_RODAR.md
├── docs/
│   ├── FinTrack_Insights_AV2.pptx
│   ├── dicionario_dados.md
│   ├── modelagem.md
│   └── validacao_sus.md
├── scripts/validar_dados.py
└── tests/test_app_core.py
```

## Metodologia

O trabalho foi organizado em cinco etapas: definição do problema, análise dos requisitos, validação da qualidade da base, prototipação e construção do dashboard. A inspeção dos dados verifica colunas obrigatórias, unicidade de `cliente_id`, domínio da variável-alvo, valores nulos e duplicidades. O desenvolvimento pode ser acompanhado por Kanban e validado em ciclos curtos com usuários do público-alvo.

## Testes e validação

A base possui um script de validação reproduzível e testes das métricas. A validação de usabilidade depende de participantes reais e **não foi simulada**. O protocolo, as tarefas, o questionário SUS e a tabela para registrar resultados estão prontos em [docs/validacao_sus.md](docs/validacao_sus.md). Após a aplicação, o grupo deve incluir quantidade de participantes, escore SUS, problemas observados e mudanças realizadas.

## Limitações

- a base é histórica e corresponde a uma amostra de 10%;
- não há custo de campanha, receita gerada ou datas completas;
- taxas altas em segmentos pequenos têm maior incerteza;
- duração do contato é conhecida apenas após a ligação e não deve ser usada para segmentação prévia;
- os resultados não demonstram relação causal;
- o protótipo simula fluxos e não possui autenticação ou persistência reais.

## Referências

MORO, S.; RITA, P.; CORTEZ, P. **Bank Marketing**. UCI Machine Learning Repository, 2014. DOI: 10.24432/C5K306.

BROOKE, J. SUS: A “quick and dirty” usability scale. In: JORDAN, P. W. et al. *Usability Evaluation in Industry*. London: Taylor & Francis, 1996.
