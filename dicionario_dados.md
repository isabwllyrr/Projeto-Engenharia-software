# Dicionário da base tratada

| Campo | Tipo | Descrição |
|---|---|---|
| cliente_id | inteiro | Identificador sequencial criado no tratamento |
| idade | inteiro | Idade do cliente |
| profissao | texto | Ocupação declarada |
| estado_civil | texto | Estado civil |
| escolaridade | texto | Nível de escolaridade |
| possui_inadimplencia | 0/1 | Existência de inadimplência de crédito |
| saldo_conta | inteiro | Saldo médio anual em euros |
| possui_financiamento_imovel | 0/1 | Financiamento imobiliário ativo |
| possui_emprestimo_pessoal | 0/1 | Empréstimo pessoal ativo |
| tipo_contato | texto | Canal do contato |
| dia_contato | inteiro | Dia do mês do último contato |
| mes_contato | texto | Mês abreviado do último contato |
| duracao_contato_seg | inteiro | Duração da ligação em segundos |
| qtd_contatos_campanha | inteiro | Contatos realizados na campanha atual |
| dias_desde_ultimo_contato | inteiro | Dias desde contato anterior; -1 indica ausência |
| contatos_campanha_anterior | inteiro | Quantidade de contatos anteriores |
| resultado_campanha_anterior | texto | Resultado da campanha anterior |
| aderiu_produto | 0/1 | Adesão ao depósito a prazo |

## Tratamentos presentes

- tradução dos nomes das colunas para português;
- criação de `cliente_id`;
- conversão de respostas binárias para 0 e 1;
- substituição de `unknown` por `nao_informado`;
- verificação de valores nulos, duplicidades e domínio do desfecho.

> A duração do contato é conhecida apenas ao término da ligação. Ela pode ser analisada descritivamente, mas não deve ser usada como variável disponível antes do contato.

