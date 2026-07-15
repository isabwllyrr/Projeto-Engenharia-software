# FinTrack — Sistema de Gestão de Gastos Pessoais

**APS — Atividades Práticas Supervisionadas**
DADM00270 — Engenharia de Software para Negócios — UFPB (2026.1)
Entrega: **AV2** — Protótipo de Software Orientado a Dados

**Aluno(s):** Isabelly, Maria Dionila e Maria Carolina

**Professor:** Alandey Severo Leite da Silva

---

## 1. Introdução

Este projeto tem como objetivo desenvolver um protótipo de software orientado a dados, aplicando conceitos de Engenharia de Software e Ciência de Dados na solução de um problema real: a dificuldade de controle financeiro pessoal.

## 2. Objetivo Geral

Desenvolver um protótipo de sistema web/mobile que permita ao usuário registrar receitas e despesas, visualizar seus gastos em um dashboard interativo e receber alertas quando estiver próximo de estourar o orçamento definido.

## 3. Objetivos Específicos

- Identificar e analisar um problema real de controle financeiro
- Levantar requisitos funcionais e não funcionais
- Modelar o sistema (casos de uso e fluxo de navegação)
- Desenvolver um protótipo navegável
- Integrar dados ao sistema (dashboard interativo)
- Validar a solução com usuários (SUS)
- Documentar todo o processo

## 4. Definição do Problema

**Contexto:** grande parte dos jovens e estudantes universitários não tem uma rotina estruturada de controle financeiro, o que dificulta saber quanto foi gasto por categoria e se o orçamento do mês está sendo respeitado.

**Público-alvo:** estudantes universitários e jovens profissionais que querem organizar receitas e despesas pessoais.

**Justificativa:** um sistema simples e orientado a dados reduz o esforço de organizar finanças pessoais e apoia decisões do dia a dia.

## 5. Levantamento de Requisitos

### Requisitos Funcionais

- RF01 — Cadastro e login do usuário
- RF02 — Registrar despesa (valor, categoria, data, descrição)
- RF03 — Registrar receita (valor, origem, data)
- RF04 — Exibir total gasto no mês
- RF05 — Exibir gráfico de gastos por categoria
- RF06 — Exibir evolução de gastos ao longo dos meses
- RF07 — Definir orçamento mensal por categoria
- RF08 — Alertar quando uma categoria ultrapassar 80% do orçamento
- RF09 — Editar ou excluir lançamento

### Requisitos Não Funcionais

- RNF01 — Dashboard deve carregar em até 2 segundos
- RNF02 — Interface responsiva (desktop e mobile)
- RNF03 — Autenticação obrigatória para proteger dados
- RNF04 — Usabilidade validada com teste de usuários (SUS)
- RNF05 — Padrão visual consistente entre telas

## 6. Modelagem do Sistema

*(diagramas de casos de uso e fluxo de navegação — ver seção 13, Pendências)*

**Fluxo principal do protótipo:** Login/Cadastro → Dashboard → Novo lançamento / Relatórios / Metas → Perfil.

## 7. Prototipação (UX/UI)

Protótipo navegável desenvolvido em **HTML/CSS/JS** (mockup de app mobile clicável, sem necessidade de servidor ou conta em ferramenta externa), contendo as telas:

1. Login / Cadastro
2. Dashboard (home)
3. Novo lançamento
4. Relatórios
5. Metas e orçamento
6. Perfil / Configurações

📄 **Arquivo:** [`prototipo_fintrack.html`](https://github.com/isabwllyrr/Projeto_Eng_Software/blob/main/prototipo_fintrack.html)
👉 Para visualizar, baixe o arquivo e abra com duplo clique no navegador — a navegação entre todas as telas funciona por clique, direto na barra inferior do app.

## 8. Integração com Dados (diferencial da disciplina)

### Fonte de dados

Como dados de gastos pessoais individuais não são publicamente disponíveis (questão de privacidade), utilizamos um dataset público real e amplamente reconhecido em ciência de dados — o Bank Marketing Dataset — contendo informações financeiras reais de 4.521 clientes (idade, profissão, saldo em conta, empréstimos, participação em campanha). Ele foi usado aqui como base real para demonstrar o pipeline completo de tratamento, banco de dados e dashboard que o FinTrack aplicaria sobre dados financeiros de usuários.

### Tratamento de dados (ETL)

Aplicado sobre [`dados_tratados.csv`](https://github.com/isabwllyrr/Projeto_Eng_Software/blob/main/dados_tratados.csv), com o processo completo documentado em [`analise_dados.ipynb`](https://github.com/isabwllyrr/Projeto_Eng_Software/blob/main/analise_dados.ipynb):

- Padronização de valores "unknown" para "nao_informado"
- Conversão de colunas binárias (yes/no) para booleano
- Renomeação de colunas técnicas para nomes de negócio em português
- Verificação e remoção de duplicatas
- Adição de chave primária (cliente_id)

### Banco de dados

Os dados tratados foram carregados em um banco SQL relacional (SQLite) — [`fintrack.db`](https://github.com/isabwllyrr/Projeto_Eng_Software/blob/main/fintrack.db) — com schema documentado em [`schema.sql`](https://github.com/isabwllyrr/Projeto_Eng_Software/blob/main/schema.sql). SQLite foi escolhido por ser um banco relacional completo, sem necessidade de servidor, ideal para protótipo acadêmico (o mesmo SQL funciona em PostgreSQL com ajustes mínimos de tipos).

### Dashboard

Dashboard interativo em **Python (Streamlit + Plotly)**, alimentado pelos dados reais tratados:

- Saldo médio em conta por profissão
- Taxa de adesão à campanha por escolaridade
- Distribuição de saldo em conta
- Proporção de clientes com empréstimo pessoal ativo
- Evolução da taxa de adesão por mês de contato
- Filtros interativos por profissão, escolaridade e faixa etária

Código-fonte: [`dashboard.py`](https://github.com/isabwllyrr/Projeto_Eng_Software/blob/main/dashboard.py)
Tema visual: [`.streamlit/config.toml`](https://github.com/isabwllyrr/Projeto_Eng_Software/blob/main/.streamlit/config.toml)

## 9. Implementação (opcional)

Este projeto já entrega uma versão funcional do elemento de dados como aplicação Streamlit, indo além do protótipo estático — cumprindo o item opcional de implementação sugerido pelo professor.

## 10. Testes e Validação

*(questionário SUS e teste com usuários — ver seção 13, Pendências)*

## 11. Estrutura do Repositório

```
├── README.md                    ← este arquivo
├── prototipo_fintrack.html      ← protótipo navegável (telas do app)
├── dashboard.py                 ← dashboard interativo (elemento de dados)
├── requirements.txt             ← dependências Python do dashboard
├── COMO_RODAR.md                ← passo a passo para rodar o dashboard
├── .streamlit/
│   └── config.toml              ← tema visual do dashboard
├── dados_tratados.csv           ← dataset após limpeza e tratamento
├── fintrack.db                  ← banco de dados SQLite (populado)
├── schema.sql                   ← script de criação das tabelas (SQL)
└── analise_dados.ipynb          ← notebook com o tratamento e os gráficos
```

## 12. Como executar

**Protótipo navegável:** baixe `prototipo_fintrack.html` e abra com duplo clique no navegador.

**Dashboard de dados:**
```
pip install -r requirements.txt
streamlit run dashboard.py
```
Abre automaticamente em `http://localhost:8501`. Passo a passo detalhado em [`COMO_RODAR.md`](https://github.com/isabwllyrr/Projeto_Eng_Software/blob/main/COMO_RODAR.md).

**Notebook de tratamento dos dados:** o GitHub renderiza `analise_dados.ipynb` automaticamente — basta abrir o arquivo na interface do GitHub para ver os gráficos, sem precisar rodar nada.

## 13. Metodologia de Desenvolvimento

Recomenda-se organização por Kanban (ex: quadro no Trello ou GitHub Projects), com tarefas divididas entre os integrantes do grupo.

## 15. Conclusão

Este projeto integra conceitos de Engenharia de Software e Ciência de Dados, propondo uma solução tecnológica real para controle financeiro pessoal, com foco em inovação, dados e experiência do usuário.
