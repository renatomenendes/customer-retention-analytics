# Dicionário de dados — mapeamento provisório

Este documento usa o enunciado do case e **nomes de colunas informados pelos artefatos de auditoria anteriores**, ainda pendentes de verificação de tipos e domínios na planilha-fonte.

| Campo ou grupo | Significado do enunciado / hipótese | Uso permitido antes da validação |
|---|---|---|
| `id_cliente` | Identificador de cliente, **não comprovadamente ID de lead** | Chave de agrupamento e verificação de repetição, nunca feature em si |
| `DATA_FUNIL_SOLAR` | Data de entrada do lead no funil | Recorte temporal, engenharia de mês de entrada |
| `COD_IBGE`, `DSC_CIDADE`, `SGL_UF`, `NM_GRUPO_REGIONAL` | Localização/região | Descrição; cuidado com granularidade e grupos pequenos |
| `FLAG_ORIGEM` | `SOLAR`: recomendação; `LEGADO`: catálogo de ofertas | Descrição/controle de composição; não causal |
| `NM_SUB_INDICADOR_NEGOCIO` | Situação do lead; níveis previamente observados: `RETIDO`, `NAO RETIDO`, `LEAD EM ABERTO` | Possível desfecho, dependente de validação |
| `flag_movel` | Indicador de posse de móvel | Entrada sob confirmação de granularidade |
| `DSC_CLI_MPLAY_M0`, `DSC_CLI_MPLAY_M30` | `MARCADO`: faturas unificadas; `NAO-MARCADO`: elegível à unificação; **vazio: não elegível** (conforme enunciado) | M0: perfil e modelagem retrospectiva; M30: apenas descritiva |
| `ID_PRODUTO_{BL,TV,FONE}_{M0,M30}` | Código por família de produto e instante | Descrever carteira/transições, com atenção a nulos |
| `COD_PLANO_MOVEL_{M0,M30}` | Código de plano móvel | Transições móveis, cuja relação com `flag_movel` precisa ser validada |
| `DSC_PRODUTO_{BL,TV,FONE}_{M0,M30}` | Descrição do produto | Auditoria e possível categorização controlada |
| `DSC_PLANO_MOVEL_{M0,M30}` | Descrição do plano móvel | Auditoria e possível categorização controlada |
| `VALOR_{BL,TV,FONE,MV}_{M0,M30}` | Valor monetário associado ao produto/instante | Variação observada; sem afirmar receita recorrente antes da validação |
| `FLAG_MOV_{BL,TV,FONE,MV}` | Indicador de movimentação por família | Possível desfecho; sem uso como feature de decisão M0 |
| `FLAG_CANC_{BL,TV,FONE,MV}` | Indicador de cancelamento por família | Desfecho de produto; não representa churn total automaticamente |
| `GRUPO_DA_TABELA_DE_PRECOS`, `CLASSIFICACAO` | Agrupamentos / classificação de cidade para preço | Atributos candidatos, dependentes da temporalidade |
| `MEIO_FISICO_BROWNFIELD`, `FLG_BROWNFIELD`, `TP_REDE_HP` | Campos adicionais na planilha e ausentes do enunciado | **Bloquear interpretação e uso preditivo até definição** |

## Temporalidade

**M0** representa o início do processo de retenção; **M30** representa seu momento final, sem prova de intervalo exato de 30 dias. O timestamp de cada um desses estados não consta como campo independente no dicionário conhecido.

## Validações ainda necessárias

- Tipos físicos, faixa válida, domínios reais, semântica de nulos e taxa de preenchimento de cada campo.
- Uso, moeda e periodicidade de `VALOR_*` e tratamento de descontos/créditos.
- Semântica exata de `FLAG_MOV_*`, `FLAG_CANC_*` e codificações de produto/pacote.
- Momento de coleta de origem, elegibilidade e classificação regional, para prevenir leakage.

## Aceite de ofertas e leitura das flags no estudo executado

O DOCX cita clientes que aceitam ofertas, mas **não define nem disponibiliza uma coluna de oferta apresentada/aceita/recusada**. Aceite real é variável não observada.

Nos registros classificados como `RETIDO`, a regra operacional de proxy contratual (alguma flag de movimentação de produto associada a troca de código em M30 sem cancelamento da família) coincide com a incidência de qualquer `FLAG_MOV_*` nos 86.540 registros movimentados. Logo, ela **não é um segundo indicador independente** nem pode ser chamada de aceite. O significado comercial dessa codificação depende do catálogo de ofertas e do log de intervenções.

O DOCX descreve `valor` como **valor monetário pago pelo cliente (receita associada ao lead)**. A periodicidade, o faturamento reconhecido, o efeito de descontos e a composição de pacotes não são documentados, razão pela qual comparamos o valor registrado M0/M30 sem inferir receita incremental.
