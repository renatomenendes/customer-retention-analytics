# Dicionário de dados e regras de interpretação

As variáveis são interpretadas de acordo com as definições fornecidas para o estudo. Quando a temporalidade ou a unidade econômica não está especificada, essa restrição é indicada na respectiva análise.

| Campo ou grupo | Definição ou interpretação | Aplicação analítica |
|---|---|---|
| `id_cliente` | Identificador de cliente, **não comprovadamente ID de lead** | Chave de agrupamento e verificação de repetição, nunca feature em si |
| `DATA_FUNIL_SOLAR` | Data de entrada do lead no funil | Recorte temporal, engenharia de mês de entrada |
| `COD_IBGE`, `DSC_CIDADE`, `SGL_UF`, `NM_GRUPO_REGIONAL` | Localização/região | Descrição; cuidado com granularidade e grupos pequenos |
| `FLAG_ORIGEM` | `SOLAR`: recomendação; `LEGADO`: catálogo de ofertas | Descrição/controle de composição; não causal |
| `NM_SUB_INDICADOR_NEGOCIO` | Situação do lead; níveis previamente observados: `RETIDO`, `NAO RETIDO`, `LEAD EM ABERTO` | Possível desfecho, dependente de validação |
| `flag_movel` | Indicador de posse de móvel | Entrada sob confirmação de granularidade |
| `DSC_CLI_MPLAY_M0`, `DSC_CLI_MPLAY_M30` | `MARCADO`: faturas unificadas; `NAO-MARCADO`: elegível à unificação; **vazio: não elegível** | M0: perfil e modelagem retrospectiva; M30: apenas descritiva |
| `ID_PRODUTO_{BL,TV,FONE}_{M0,M30}` | Código por família de produto e instante | Descrever carteira/transições, com atenção a nulos |
| `COD_PLANO_MOVEL_{M0,M30}` | Código de plano móvel | Transições móveis, cuja relação com `flag_movel` precisa ser validada |
| `DSC_PRODUTO_{BL,TV,FONE}_{M0,M30}` | Descrição do produto | Auditoria e possível categorização controlada |
| `DSC_PLANO_MOVEL_{M0,M30}` | Descrição do plano móvel | Auditoria e possível categorização controlada |
| `VALOR_{BL,TV,FONE,MV}_{M0,M30}` | Valor monetário associado ao produto/instante | Variação observada; sem afirmar receita recorrente antes da validação |
| `FLAG_MOV_{BL,TV,FONE,MV}` | Indicador de movimentação por família | Possível desfecho; sem uso como feature de decisão M0 |
| `FLAG_CANC_{BL,TV,FONE,MV}` | Indicador de cancelamento por família | Desfecho de produto; não representa churn total automaticamente |
| `GRUPO_DA_TABELA_DE_PRECOS`, `CLASSIFICACAO` | Agrupamentos / classificação de cidade para preço | Atributos candidatos, dependentes da temporalidade |
| `MEIO_FISICO_BROWNFIELD`, `FLG_BROWNFIELD`, `TP_REDE_HP` | Campos sem definição de negócio disponível | Fora das variáveis modeladas |

## Temporalidade

**M0** representa o início do processo de retenção; **M30** representa seu momento final, sem prova de intervalo exato de 30 dias. O timestamp de cada um desses estados não consta como campo independente no dicionário conhecido.

## Limites de interpretação

- Tipos físicos, faixa válida, domínios reais, semântica de nulos e taxa de preenchimento de cada campo.
- Uso, moeda e periodicidade de `VALOR_*` e tratamento de descontos/créditos.
- Semântica exata de `FLAG_MOV_*`, `FLAG_CANC_*` e codificações de produto/pacote.
- Momento de coleta de origem, elegibilidade e classificação regional, para prevenir leakage.

## Aceite de ofertas e leitura das flags

Não há variável observada de oferta apresentada, aceita ou recusada. A taxa verdadeira de aceite não é identificável neste conjunto.

Nos registros classificados como `RETIDO`, a regra operacional de proxy contratual (alguma flag de movimentação de produto associada a troca de código em M30 sem cancelamento da família) coincide com a incidência de qualquer `FLAG_MOV_*` nos 86.540 registros movimentados. Logo, ela **não é um segundo indicador independente** nem pode ser chamada de aceite. O significado comercial dessa codificação depende do catálogo de ofertas e do log de intervenções.

Os campos `VALOR_*` representam valores pagos associados ao registro. Como periodicidade, faturamento reconhecido, descontos e composição dos pacotes não são discriminados, a comparação M0/M30 caracteriza diferenças registradas, sem identificar receita incremental.
