# Estudo de clientes retidos com movimentação — caracterização analítica e decisões

**Período:** junho a dezembro de 2025. **População:** atendimentos com status `RETIDO`. **Unidade:** registro do funil, não necessariamente cliente único. Os resultados são relativos à amostra demonstrativa.

## Resumo executivo

A análise caracteriza **movimentações entre registros retidos**, com base no status do funil, nas flags de movimentação, nas transições de produto/plano e nos valores M0/M30. O estimando central é `P(MOV=1 | RETIDO=1, X_M0)`. O conjunto não registra decisões de aceite de oferta.

**População central:** 249.309 registros `RETIDO`; 86.540 com alguma movimentação (34,7%); 86.540 com proxy restritiva de alteração contratual não cancelada (34,7%). Do total de retidos com movimentação, 15,2% também têm alguma flag de cancelamento de produto: **movimentação é heterogênea**, não sinônimo de oferta aceita.

## 1. Pergunta, construtos e validade

- **R**: `RETIDO`, desfecho operacional do funil. **M**: pelo menos uma `FLAG_MOV_* = 1`. **X_M0**: carteira, atributos geográficos e comerciais disponíveis ou presumidos no início. **A**: aceite real de oferta, **variável latente não observada**.
- **Estimando central:** `P(M=1 | R=1, X_M0)`. Esta condição gera seleção pelo desfecho e serve para **caracterização retrospectiva**, não para pontuar todos os leads antes da retenção.
- **Estimando secundário:** `P(R=1, M=1 | X_M0)` entre atendimentos concluídos. Continua no notebook 03 com escopo próprio.
- **Valor:** M30−M0 de campos `VALOR_*`; são valores pagos associados ao registro. Sem competência e preço líquido conciliado, não equivalem a ganho incremental da campanha.
- **Aceite de oferta:** não observado. A proxy ampla pode superestimar aceite e a restritiva pode simultaneamente admitir falsos positivos e excluir aceites sem troca de código. Não há limite estatisticamente identificado para `P(A=1)` a partir dos campos presentes.

## 2. Caracterização dos perfis — todos os denominadores são retidos

### 2.1 Mix inicial

| Composição da carteira em M0 | Retidos | Com alguma movimentação |
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
| FONE | 858 | 8,2% |
| BL+FONE+MV | 848 | 59,8% |

Esta tabela só mostra grupos com pelo menos 500 registros. Uma carteira com mais famílias oferece mais oportunidades de movimento. Dividir o total de flags por famílias presentes em M0 ajuda a expor esse problema, mas não produz efeito ajustado nem causal. As comparações por família e exposição estão no notebook 05.

### 2.2 Origem e composição

| Canal | Registros `RETIDO` | Com movimentação |
|---|---:|---:|
| LEGADO | 51.214 | 32,0% |
| SOLAR | 198.095 | 35,4% |

| Famílias M0 + origem | Retidos | Movimentação |
|---|---:|---:|
| 1|LEGADO | 19.591 | 23,8% |
| 1|SOLAR | 70.879 | 28,7% |
| 2|LEGADO | 17.969 | 34,3% |
| 2|SOLAR | 73.103 | 37,5% |
| 3|LEGADO | 13.244 | 40,1% |
| 3|SOLAR | 52.060 | 40,3% |
| 4|SOLAR | 1.988 | 69,1% |

Há 6.162 leads abertos em LEGADO e 90 em SOLAR, segundo os agregados auditados. A diferença de casos pendentes torna inadequada uma comparação causal entre canais.

### 2.3 Região, MPlay, classificação e posse móvel

Essas dimensões estão representadas no modelo conjunto e foram examinadas em segmentos de pelo menos 500 registros, com seus denominadores explícitos.

**MPlay (M0):** campo vazio significa **não elegível** à unificação de faturas no dicionário fornecido; não é valor desconhecido. A categoria representa **93,1%** dos registros retidos, enquanto **34,4%** é a taxa de movimentação dentro dela. Os percentuais da tabela seguinte são todos taxas condicionadas ao respectivo grupo.

| Categoria | Retidos | Movimentação |
|---|---:|---:|
| NÃO ELEGÍVEL (vazio no campo original) | 232.017 | 34,4% |
| MARCADO | 10.587 | 54,0% |
| NAO-MARCADO | 6.705 | 15,2% |

**Classificação comercial:**

| Categoria | Retidos | Movimentação |
|---|---:|---:|
| G1 | 144.563 | 34,6% |
| G2 | 45.764 | 34,6% |
| MD2 | 24.914 | 36,4% |
| MD1 | 7.000 | 36,4% |
| G7 | 5.974 | 34,1% |
| G4 | 5.929 | 34,3% |
| G5 | 4.193 | 34,5% |

**Posse móvel:**

| Categoria | Retidos | Movimentação |
|---|---:|---:|
| 1 | 136.438 | 37,8% |
| 0 | 112.871 | 31,0% |

**UFs com mais registros:**

| UF | Retidos | Movimentação |
|---|---:|---:|
| SP | 108.570 | 36,6% |
| RJ | 35.753 | 33,4% |
| RS | 16.132 | 28,5% |
| MG | 14.959 | 37,8% |
| PR | 10.356 | 32,8% |
| SC | 10.024 | 33,1% |
| DF | 7.823 | 34,9% |
| GO | 5.860 | 33,5% |
| BA | 5.692 | 33,9% |
| AM | 4.489 | 37,1% |
| ES | 4.087 | 30,1% |
| PA | 3.347 | 35,8% |

A regressão penalizada permite examinar associação conjunta, mas não resolve seleção do funil, confundimento por ofertas não medidas ou a natureza comercial dessas categorias. O estudo não declara que estes grupos constituem *personas* estáveis ou são efeitos causais.

### 2.4 Sensibilidade à repetição do mesmo cliente

Há uma média de 34,7% de movimentação entre **todos os registros retidos** versus 34,8% quando se mantém somente o primeiro registro `RETIDO` conhecido de cada ID (235.462 IDs). Essa sensibilidade não equivale à identificação do primeiro lead do cliente: registros com `NAO RETIDO` podem preceder o primeiro `RETIDO`.

### 2.5 Evolução mensal

| Mês | Registros `RETIDO` | Com movimentação |
|---|---:|---:|
| 2025-06 | 36.175 | 30,6% |
| 2025-07 | 36.023 | 39,6% |
| 2025-08 | 36.176 | 36,2% |
| 2025-09 | 35.929 | 34,6% |
| 2025-10 | 35.559 | 36,0% |
| 2025-11 | 34.912 | 33,8% |
| 2025-12 | 34.535 | 32,1% |

Alterações entre meses podem refletir mix, política de atendimento, maturidade ou composição amostral. Não há série longitudinal de faturamento de cada cliente.

## 3. Movimentação, cancelamento e variação monetária por família

As transições usam os códigos de produto/plano de M0 e M30. **Troca de código** não é necessariamente inclusão de produto, **cancelamento de produto** não é churn total, e **mudança de valor sem troca de código** não deve ser ignorada.

| Família | Transição | Registros retidos | FLAG_MOV na transição | FLAG_CANC | Média Δ valor quando presente |
|---|---|---:|---:|---:|---:|
| BL | unchanged | 142.829 | 0,0% | 0,0% | 0,98 |
| BL | replacement | 74.255 | 100,0% | 0,0% | -22,08 |
| BL | absent | 9.747 | 0,0% | 0,0% | 0,00 |
| BL | removal | 22.478 | 0,0% | 100,0% | -101,32 |
| TV | removal | 19.381 | 0,0% | 100,0% | -118,33 |
| TV | replacement | 24.595 | 100,0% | 0,0% | -30,76 |
| TV | absent | 110.555 | 0,0% | 0,0% | -0,37 |
| TV | unchanged | 94.778 | 0,0% | 0,0% | 1,46 |
| FONE | absent | 160.731 | 0,0% | 0,0% | 0,00 |
| FONE | unchanged | 61.512 | 0,0% | 0,0% | 0,00 |
| FONE | removal | 17.059 | 0,0% | 100,0% | 0,00 |
| FONE | replacement | 10.007 | 100,0% | 0,0% | 0,00 |
| MV | absent | 238.345 | 0,0% | 0,0% | 0,00 |
| MV | unchanged | 6.577 | 0,0% | 0,0% | -1,64 |
| MV | replacement | 4.387 | 100,0% | 0,0% | -4,81 |

*Grupos abaixo de 500 foram omitidos nesta tabela de divulgação agregada. Médias monetárias são por registro com valor comparável em ambos os estados, sem correção por pacotes, desconto ou competência.*

Nos retidos que movimentaram: mediana M30−M0 de **-25,46**, redução em **78,7%** e variação agregada da soma de **-20,1%**. Sem transação de oferta, custo e competência financeira, não calcular **preservação de receita incremental** ou margem.

## 4. Aceite de ofertas: evidência disponível

**Aceite observado:** indisponível. **Sinais observados:** movimento amplo e transição restritiva compatível com uma alteração de plano/produto. A última exige mudança de código/plano, presença do produto ao final, flag de movimento e inexistência de cancelamento naquela família.

| Sinal | N entre retidos | Fração dos retidos | O que indica |
|---|---:|---:|---|
| Alguma flag `FLAG_MOV_*` | 86.540 | 34,7% | Alteração operacional; pode ou não estar ligada a oferta |
| Proxy de alteração contratual não cancelada | 86.540 | 34,7% | Mudança compatível com possível oferta; não confirma apresentação nem aceite |

Para estabelecer a escala do **risco de extrapolação**, a tabela abaixo varia *hipoteticamente* a fração de movimentos ligados a aceites; **não é modelo estimado a partir da planilha**:

| Hipótese de aceites dentre movimentos | Quantidade hipotética |
|---|---:|
| 25% (suposição) | 21.635 (simulação) |
| 50% (suposição) | 43.270 (simulação) |
| 75% (suposição) | 64.905 (simulação) |

**Teste de informação incremental da proxy:** na amostra analisada, os **86.540** registros positivos na proxy restritiva são exatamente os **86.540** com alguma flag de movimentação. Portanto a proxy restritiva **não discrimina** um subconjunto adicional e não aumenta a evidência acerca de aceite. É um diagnóstico do modo como as flags codificam a troca contratual; não valida a oferta apresentada ou aceita.

A proporção real pode ficar fora dessas hipóteses: mudanças sem flags e ofertas que alteram só desconto são possíveis. O intervalo 25–75% **não é intervalo de confiança, faixa identificada nem estimativa**. A medição exigirá campos de oferta exposta, oferta aceite/recusada, data, canal, elegibilidade e preço antes/depois.

## 5. Modelagem condicional — comparação comum e estabilidade

### 5.1 Desenho

Treino junho–setembro, validação outubro, teste novembro–dezembro. Observações com o mesmo ID de cliente não atravessam períodos de treino/validação/teste; os descartes foram 4.918 registros do treino e 1.131 da validação. Repetições **dentro** dos períodos permanecem. O estado `RETIDO` é usado para delimitar a amostra, logo os modelos são retrospectivos, não motores acionáveis em M0 para toda a população.

Alvo operacional: `MOV` em `R=1`. Atributos: canal, UF, MPlay, classificação, posse móvel, mix e tamanho da carteira inicial e três valores M0. A semântica temporal de todas as classificações ainda requer validação. A mesma divisão foi aplicada à taxa de treino (baseline), regressão penalizada, árvore rasa e boosting tabular.

| Modelo | AUC-ROC | AP | Brier | Log-loss | Lift no top 10% |
|---|---:|---:|---:|---:|---:|
| prior | 0,500 | 0,330 | 0,2216 | 0,6352 | 1,00× |
| logistic | 0,627 | 0,458 | 0,2104 | 0,6099 | 1,68× |
| small tree | 0,629 | 0,444 | 0,2097 | 0,6083 | 1,67× |
| hist boosting | 0,650 | 0,487 | 0,2065 | 0,6010 | 1,81× |

**Modelo com menor Brier na validação:** hist_boosting. Nenhuma métrica foi calculada em outro conjunto de teste para favorecê-lo. A seleção por validação não prova melhoria comercial; se os modelos tiverem desempenho próximo, simplificação e estabilidade devem prevalecer.

### 5.2 Evolução dentro do holdout

| Mês do teste | N | Prevalência de MOV | AUC do escolhido | Brier do escolhido |
|---|---:|---:|---:|---:|
| 2025-11 | 34.912 | 33,8% | 0,647 | 0,2094 |
| 2025-12 | 34.535 | 32,1% | 0,652 | 0,2036 |

**Por origem no teste:**

| Origem | N | Prevalência | AUC | Brier |
|---|---:|---:|---:|---:|
| LEGADO | 17.014 | 32,9% | 0,659 | 0,2046 |
| SOLAR | 52.433 | 33,0% | 0,651 | 0,2071 |

### 5.3 Calibração descritiva do melhor por validação

| Faixa prevista | N | P média prevista | Movimento observado |
|---|---:|---:|---:|
| 0.1-0.2 | 6.976 | 16,7% | 14,2% |
| 0.2-0.3 | 12.659 | 25,6% | 24,1% |
| 0.3-0.4 | 33.196 | 34,5% | 31,8% |
| 0.4-0.5 | 11.628 | 44,6% | 44,9% |
| 0.5-0.6 | 3.601 | 53,8% | 57,3% |
| 0.6-0.7 | 1.268 | 64,5% | 74,9% |

As faixas têm largura de 0,1 e são publicadas quando contêm ao menos 100 observações; a ECE informada no arquivo de métricas é **parcial** quando há faixas omitidas. Brier e diagrama de calibração não validam a decisão de oferta, apenas o ajuste da previsão do evento analisado.

### 5.4 Interpretação e incerteza

O modelo com todas as variáveis iniciais proporciona avaliação multivariada da discriminação, mas seus coeficientes/variáveis não identificam o efeito de intervenção nem inferem o evento **A = aceite**. Intervalos de confiança por cluster de cliente, curvas de decisão e avaliação em novos períodos após dezembro ainda não estão identificados: não os substituímos por p-values ingênuos. A consistência por mês e canal é apresentada com prevalência e denominadores.

### 5.5. Cancelamentos de produtos, desfechos em aberto e robustez

A [análise de eventos contratuais](deep_exploration_findings.md) apresenta os quatro cruzamentos **movimentação × cancelamento**, distribuições monetárias P10–mediana–P90, transições por família, coortes abertas por origem e diferença padronizada entre canais com bootstrap por cliente.

O achado central é a presença de **32.318** retidos sem `FLAG_MOV_*` e com cancelamento de produto (mediana ΔV **−104,90**); entre os 86.540 retidos com movimento, **13.161** também tiveram cancelamento (mediana **−88,96**). A comparação SOLAR–LEGADO entre retidos passou de **+3,41 p.p.** brutos para **+2,93 p.p.** padronizados por coorte mensal × número de famílias em M0; intervalo bootstrap agrupado por cliente **[+2,53; +3,41] p.p.**. São associações condicionadas ao status RETIDO, sem interpretação causal.

Os cenários extremos para atendimentos em aberto mostram a sensibilidade das taxas de retenção ao encerramento dos casos. Eles não constituem curvas de sobrevivência. A análise parametrizada de contribuição e custo apresenta limiares hipotéticos de equilíbrio, sem estimar lucro ou efeito incremental observado.

## 6. Desbalanceamento por família e sensibilidade à ponderação

A análise global não basta para concluir que os modelos representam igualmente bem BL (Banda Larga, internet fixa), TV, Fone e Móvel. A avaliação por produto usa quatro alvos binários, cada um condicionado à presença do respectivo produto em M0. No teste cronológico, a classe positiva variou de 12,1% (Fone) a 40,7% (Móvel). Nos pipelines testados, a ponderação balanceada, sem recalibração posterior, piorou o Brier nas quatro famílias e nem sempre melhorou o ranking. Em Fone elevou a AUC (0,551 para 0,574), mas o Brier subiu de 0,1061 para 0,2219; em Móvel, a vantagem marginal de validação do ponderado não se manteve no teste. Os valores, AP relativa à prevalência e comparação dos modelos estão no [estudo de desbalanceamento](family_imbalance_analysis.md) e no [notebook 08](../notebooks/08_family_imbalance.ipynb). Nenhum resultado valida aceite de oferta ou recomendação causal.


## 7. Recomendações para avaliação comercial

| Perfil ou problema | Evidência | Ação/protocolo | Indicador primário | Como validar |
|---|---|---|---|---|
| Mix inicial e exposição | Taxas distintas por carteira e por oportunidade | Ofertas e scripts de atendimento orientados à família presente em M0 | Movimentação entre retidos e retenção entre encerrados, separadamente | Teste estratificado por mix, mantendo capacidade e elegibilidade |
| Movimentações com cancelamento parcial | 15,2% dos retidos movimentados têm alguma FLAG_CANC | Auditar tipo de transição e perda de produto | Retenção com cancelamento e delta por família | Comparar taxas e custos com decisão operacional revisada |
| Valor registrado negativo | 78,7% dos retidos que movimentaram têm Δ negativo | Investigar descontos, downgrade, fim de bônus e pacotes | Δ monetário reconciliado; receita líquida após contrato | Extração de faturamento e desenho de teste financeiro |
| Origens com maturidade diferente | Leads em aberto muito distintos por canal | Melhorar definição e atualização de encerramento | SLA de fechamento, abertos e retenção entre casos maduros | Acompanhar coortes após prazo fixo |
| Aceite não registrado | Proxies têm erros de classificação desconhecidos | Instrumentar ID e resultado de cada oferta | Taxa efetiva de aceite e receita incremental | Experimento randomizado com grupo comparável |
| Modelo de movimento entre retidos | AUC, AP, Brier por período no holdout | Estudar características associadas, sem aplicação preditiva ex-ante | Estabilidade do perfil e desempenho por período | Avaliar período posterior e reproduzir com chave oficial |

## 8. Conclusão e alcance dos resultados

**Resultados do estudo:** perfis observados dentro dos registros classificados como retidos, descrição condicional de movimentação por características iniciais, contraste de transições M0/M30, diferenças entre flags e troca de código, comparação de quatro modelos num mesmo teste temporal e recomendações testáveis.

**Fora do alcance desta base:** taxa verdadeira de aceite, efeito incremental/causal de ofertas, permanência futura, lucro/receita reconhecida e episódios únicos de atendimento. Essas limitações definem o alcance das conclusões observacionais.

A [fundamentação metodológica](benchmark_and_gap_review.md) contextualiza a escolha de estimandos, métricas e métodos.


