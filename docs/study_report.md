# Estudo de retenção e movimentação de produtos — resultados observacionais

**Período:** junho a dezembro de 2025. **Unidade:** registro da planilha (episódio do funil apenas candidato). **Status:** estudo exploratório executado, conclusões com hipóteses explícitas. **Classificação:** uso restrito no repositório privado.

## Resumo executivo

Foram examinados **303.652 registros** no período, com **249.309 classificados como retidos**, **48.091 como não retidos** e **6.252 sem desfecho concluído**. No grupo retido, **86.540 registros** apresentaram ao menos uma flag de movimentação (**34,7%**). A medida se refere a registros do funil, não a permanência do assinante, aceite de ofertas ou retenção futura.

Três achados delimitam a decisão: (i) a aparente maior movimentação em carteiras multiproduto é parcialmente dependente do número de oportunidades; (ii) a variação dos campos de valor em retidos com movimentação é frequentemente negativa; (iii) um classificador do evento composto mostrou discriminação moderada fora do treino, mas não avalia efeito de intervenção.

## 1. Escopo, pergunta, estimandos e elegibilidade

A pergunta central não é simplesmente prever *churn*. É caracterizar, **dentro dos registros classificados como retidos**, aqueles com alteração contratual e examinar separadamente a evolução de valor observado. Distinguimos:

- **R** = status `RETIDO` nos leads com desfecho conhecido; `LEAD EM ABERTO` não compõe a classe negativa.
- **M** = ao menos uma `FLAG_MOV_BL/TV/FONE/MV` acionada, observada após atendimento.
- **Perfil central** = distribuição das características de M0 entre `R=1,M=1` comparada a `R=1,M=0`; calcular `P(M=1|R=1,X)` exige deixar claro o condicionamento no desfecho.
- **Predição secundária** = `P(R=1,M=1|X)` entre encerrados, com atributos presumidos em M0. Esse não é o mesmo alvo do perfil central.
- **ΔV** = `Σ VALOR_*_M30 − Σ VALOR_*_M0`, com unidades e periodicidade ainda **não confirmadas**. Não é lucro, receita faturada, margem, economia gerada ou causalidade da oferta.

O arquivo contém **303.654** linhas, mas duas precedem junho de 2025; logo, são usados **303.652** registros. Há **14.069 IDs de cliente repetidos**, dos quais **1.706 com status distintos**. Não se deve deduplicar nem atribuir a cada linha uma pessoa distinta até que exista chave oficial de episódio. A frequência dos leads por mês não demonstra desenho probabilístico da amostra.

## 2. Evolução no tempo

| Entrada | Registros | Retidos | Não retidos | Abertos | Retidos / encerrados | Com movimento / retidos |
|---|---:|---:|---:|---:|---:|---:|
| 2025-06 | 43.218 | 36.175 | 6.330 | 713 | 85,1% | 30,6% |
| 2025-07 | 43.244 | 36.023 | 6.501 | 720 | 84,7% | 39,6% |
| 2025-08 | 43.418 | 36.176 | 6.623 | 619 | 84,5% | 36,2% |
| 2025-09 | 43.470 | 35.929 | 6.989 | 552 | 83,7% | 34,6% |
| 2025-10 | 43.509 | 35.559 | 7.028 | 922 | 83,5% | 36,0% |
| 2025-11 | 43.337 | 34.912 | 7.177 | 1.248 | 82,9% | 33,8% |
| 2025-12 | 43.456 | 34.535 | 7.443 | 1.478 | 82,3% | 32,1% |

![Status ao longo do período](../reports/figures/status_retention_monthly.svg)

A participação do status de retenção entre atendimentos **encerrados** declina na amostra, mas não é inferível como deterioração do processo: composição por origem, critérios de encerramento, extração e maturidade podem variar. A movimentação entre retidos apresenta um pico em julho, o que recomenda checar política e mix do período, em vez de interpretá-lo como efeito sazonal comprovado.

## 3. Perfis de carteira e viés de oportunidade

| Famílias M0 | Retidos (registros) | Retidos com alguma movimentação | Taxa por registro retido | Flags por oportunidade M0 |
|---|---:|---:|---:|---:|
| 1 | 90.470 | 25.011 | 27,6% | 27,6% |
| 2 | 91.072 | 33.605 | 36,9% | 23,6% |
| 3 | 65.304 | 26.302 | 40,3% | 21,4% |
| 4 | 2.333 | 1.622 | 69,5% | 36,4% |

![Movimentação por exposição inicial](../reports/figures/portfolio_opportunities.svg)

A taxa de qualquer movimentação responde à pergunta de **qual percentual de registros tiveram ao menos uma mudança**. A taxa por oportunidade responde à pergunta distinta de **quantas flags ocorreram por família existente em M0**. Não se pode somar ambas nem tratar oportunidades como ensaios independentes. A curva não é monotônica após normalização: 4 famílias permanecem um grupo diferenciado, mas com tamanho muito menor, possível efeito de composição e regras próprias de produto móvel.

### Famílias disponíveis em M0

| Família | Oportunidades observadas entre retidos | Flags acionadas | Flags / oportunidades |
|---|---:|---:|---:|
| BL | 239.562 | 74.255 | 31,0% |
| TV | 138.754 | 24.595 | 17,7% |
| FONE | 88.578 | 10.007 | 11,3% |
| MV | 10.964 | 4.387 | 40,0% |

![Taxa por família disponível](../reports/figures/movements_by_family.svg)

As famílias apresentam heterogeneidade substantiva. Móvel possui a maior incidência condicionada à presença inicial, mas também possui o menor denominador. Seria incorreto recomendar inclusão de móvel para elevar movimentação: a associação pode resultar de oferta, elegibilidade, seleção e natureza da alteração.

### Combinações iniciais mais frequentes

| Mix M0 | Retidos | Movimentação / retidos |
|---|---:|---:|
| BL | 82.490 | 28,9% |
| BL+TV | 63.301 | 36,3% |
| BL+TV+FONE | 61.897 | 39,0% |
| BL+FONE | 21.380 | 35,0% |
| TV | 7.120 | 15,7% |
| BL+MV | 4.802 | 55,5% |
| BL+TV+MV | 2.511 | 64,8% |
| BL+TV+FONE+MV | 2.333 | 69,5% |
| TV+FONE | 1.169 | 21,1% |

Os grupos exibidos exigem pelo menos **1.000 registros retidos**; grupos menores foram suprimidos desta síntese. Não há ranking de desempenho causal entre mixes. Um refinamento futuro deve estimar comparações estratificadas por origem, mês e famílias elegíveis, preferencialmente com incerteza por cluster de cliente.

## 4. Origem e desfechos ainda abertos

| Origem | Registros | Abertos | Abertos / total | Retidos / encerrados | Movimentação / retidos |
|---|---:|---:|---:|---:|---:|
| LEGADO | 68.380 | 6.162 | 9,0% | 82,3% | 32,0% |
| SOLAR | 235.272 | 90 | 0,0% | 84,2% | 35,4% |

A concentração de leads em aberto em `LEGADO` é uma ameaça à comparabilidade dos canais. Condicionar a análise apenas aos atendimentos encerrados seleciona grupos com maturidade diferente. **Não existe base para concluir que o mecanismo `SOLAR` causa maior retenção ou preservação de receita.** A estratégia adequada é reconciliar critérios de encerramento e estágio do funil antes de estimar vantagens comparativas.

## 5. Movimentação e preservação de valor: limites econômicos

| Grupo (registros) | N | Mediana ΔV | Média ΔV | ΔV negativo | ΔV positivo | Variação da soma M0→M30 |
|---|---:|---:|---:|---:|---:|---:|
| Retidos com movimentação | 86.540 | -25.46 | -37.72 | 78,7% | 14,9% | -20,1% |
| Retidos sem movimentação | 162.769 | 0.00 | -21.49 | 19,5% | 9,9% | -12,4% |
| Não retidos | 48.091 | -103.64 | -96.65 | 70,5% | 4,3% | -68,9% |

![Mediana dos valores](../reports/figures/value_deltas.svg)

No grupo com status retido e movimento, **78,7%** têm ΔV negativo e apenas **14,9%** ΔV positivo. A mediana é **−25,46** e a variação relativa da soma, **−20,1%**. Esses números não medem impacto de oferta ou receita realizada. Sem competência financeira, regras de bundle, desconto, crédito, preço versus cobrança e custo, nenhuma análise de LTV, margem ou lucro foi validada. O campo monetário de Fone é quase sempre zero apesar da presença contratual, aumentando o risco de erro econômico se interpretado como faturamento real.

Recomendação metodológica imediata: conciliar valor por **produto, tipo de transição de código, flag de cancelamento, origem e mês**, com identificação contratual do campo; só então monetizar preservação efetiva ou construir um modelo orientado a margem.

## 6. Modelo experimental: avaliação cronológica, não validação comercial

**Tarefa modelada:** evento composto `RETIDO ∧ qualquer FLAG_MOV`, entre registros de status encerrado. **Não foi modelada isoladamente a variável M entre os retidos.** Preditores disponíveis ou presumidos em M0; origem, UF, classificação, quantidade e mix de famílias e valores M0. A disponibilidade temporal de todos os preditores ainda requer confirmação.

| Divisão | Período | Registros |
|---|---|---:|
| train | junho–setembro de 2025 | 165.424 |
| validation | outubro de 2025 | 41.343 |
| test | novembro–dezembro de 2025 | 84.067 |

Os clientes presentes em períodos posteriores foram excluídos do treino (5.322 registros) e, quando pertinente, da validação (1.244), evitando compartilhamento direto de IDs entre essas partições. Há ainda observações repetidas **dentro** de cada partição.

| Modelo | Validação: AUC | Validação: AP | Validação: Brier |
|---|---:|---:|---:|
| Constante | 0.500 | 0.300 | 0.2102 |
| Logística | 0.665 | 0.469 | 0.1939 |
| Árvore curta | 0.668 | 0.445 | 0.1939 |

**A árvore foi selecionada pelo menor Brier em outubro, mas a diferença para a logística foi somente 0,000082**. Sem intervalo de incerteza e sem teste da logística em novembro–dezembro, não há base para declarar superioridade geral da árvore.

| Modelo no holdout | AUC-ROC | AP | Brier | Log-loss | Lift top 10% |
|---|---:|---:|---:|---:|---:|
| Constante | 0.500 | 0.272 | 0.1988 | 0.5871 | 1.00× |
| Árvore selecionada | 0.662 | 0.405 | 0.1849 | 0.5525 | 1.84× |

O holdout tem 84.067 registros encerrados e prevalência do evento composto de 27,24%. A precisão no decil superior da árvore foi 50,04%, comparada à prevalência da base de 27,24%. Isso é ranking de um **evento operacional observado**, não benefício de ofertar a clientes pontuados. O Brier não é prova isolada de calibração: faltam curvas de confiabilidade, ECE com intervalos, replicações temporais e acompanhamento prospectivo.

## 7. Benchmark científico: posicionamento apropriado

- **Verbeke et al. (2012)**: otimização de retenção requer custo e valor econômico de campanhas. Usar AUC como indicador único é insuficiente. DOI: [10.1016/j.ejor.2011.09.031](https://doi.org/10.1016/j.ejor.2011.09.031).
- **Verhelst et al. (2025)**: uplift em telecom diferencia probabilidade de churn de *mudança provocada pela ação*. Nosso dataset não registra tratamento/controle e aceite em termos que permitam identificar tal estimando. DOI: [10.1007/978-3-031-74640-6_21](https://doi.org/10.1007/978-3-031-74640-6_21).
- **Scikit-learn, calibração**: perdas próprias como Brier combinam resolução e calibração; é obrigatório avaliar confiabilidade de probabilidades antes de uso comercial. [Documentação](https://scikit-learn.org/stable/modules/calibration.html).

A literatura fornece critérios metodológicos, **não metas de AUC diretamente comparáveis** ao case. Curvas de sobrevivência (Kaplan–Meier/Cox) ficam fora do escopo empiricamente identificado até existir duração e censura observáveis por lead.

## 8. Recomendações priorizadas como hipóteses a testar

| Prioridade | Perfil-alvo | Evidência | Ação e desenho de teste | Métrica principal | Pré-condição |
|---|---|---|---|---|---|
| 1 | Carteiras BL e multiproduto com movimentação | Denominador por família altera leitura de propensão | Experimentar políticas de oferta estratificadas por mix e elegibilidade; randomização no atendimento | Retenção real e valor líquido validado por conta | Chave do atendimento, produtos elegíveis e custos |
| 2 | Atendimentos com redução de valores apesar de `RETIDO` | 78,7% do grupo retido/movimentado têm ΔV negativo | Auditar downgrade, cancelamento parcial, crédito e desconto; intervir após validação dos tipos | Receita líquida e margem após ciclo definido | Dicionário financeiro/contábil |
| 3 | Leads abertos do canal LEGADO | Taxa de pendência desproporcional entre canais | Diagnosticar SLA, data de resolução e cadência de atualização; comparar apenas coortes maduras | Fração encerrada por idade do lead | Timestamp de encerramento |
| 4 | Registros com score alto do evento composto | Lift 1,84× no decil superior de teste temporal | Modo sombra e auditoria de estabilidade; depois A/B de oferta com controle | Ganho incremental líquido por contato | Tratamento definido, holdout e custos |

Nenhuma dessas ações tem impacto causal ou financeiro demonstrado na amostra. As recomendações são desenhos de aprendizado e decisão, não promessas comerciais.

## 9. Validade, sensibilidade e pendências impeditivas

- **Unidade da análise:** episódios ainda não têm chave oficial; intervalos binomiais ingênuos subestimam dependência de IDs repetidos.
- **População e seleção:** amostra sem plano de extração/pesos; volume mensal regular e canal dependente de encerramento.
- **Tempo:** apenas sete meses e M30 sem timestamp individual de desfecho; não identificar sobrevivência, churn sustentado ou censura.
- **Movimentação:** flags indicam transição/código, não oferta aceita; crescimento de volume/compra recorrente não observável.
- **Economia:** unidades monetárias ainda não validadas, possível bundling e valores de Fone nulos/zero na maior parte dos registros.
- **Modelagem:** partição cronológica, mas sem teste comparativo completo, estabilidade, incerteza por cliente, controle de múltiplos testes, calibração ou uplift causal.
- **Privacidade:** somente agregados com grandes denominadores são materializados neste relatório; nenhum registro, hash de dados, endereço ou identificador foi divulgado.

**Condição de encerramento científico:** a investigação descritiva e o experimento estão executados e documentados. A validação de política de retenção e de preservação de receita **não está empiricamente identificada**; requer decisões de negócio e/ou novas fontes. Declarar essas limitações faz parte da conclusão correta do estudo, não é omissão de um resultado possível.

## 10. Procedência e reprodução

Indicadores gerados pela leitura integral local da planilha autorizada. Os arquivos-fonte privados foram analisados em ambiente local. Os agregados publicados em [`reports/aggregate_study_2025.json`](../reports/aggregate_study_2025.json) resultam de **`audit_summary.json`**, **`profiles_summary.json`**, **`opportunity_diagnostics.json`** e **`model_validation.json`**, preservados apenas localmente. O notebook [05](../notebooks/05_study_synthesis.ipynb) demonstra os cálculos da síntese pública do repositório privado, enquanto notebooks 01–04 permitem recomputar as etapas originais mediante acesso à planilha privada.