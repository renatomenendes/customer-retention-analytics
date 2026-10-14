# Revisão crítica e benchmarking externo — retenção com movimentação

**Data:** 2026-10-14  
**Natureza:** avaliação de desenho analítico e literatura, não um novo resultado de modelagem.  
**Classificação:** nenhum dado individual nem resultado agregado da empresa neste documento.

## 1. Revisão da qualidade do estudo existente

O estado implementado até o primeiro ciclo de modelagem demonstra leitura completa da planilha, auditoria de status e M0/M30, análise univariada por segmentos, uma baseline constante, regressão logística e árvore rasa com recorte temporal. Isso não permite declarar que todos os requisitos de investigação, modelagem e inteligência de negócio estejam atendidos.

| Gravidade | Fragilidade | Impacto | Remediação verificável |
|---|---|---|---|
| **Crítica** | Alvo composto `RETIDO ∧ FLAG_MOV` interpretado como perfil de movimentação **entre retidos** | Mistura a capacidade de retenção com a propensão condicional à movimentação | Reportar separadamente `P(RETIDO | M0)`, `P(MOV | RETIDO, M0)` e `P(RETIDO ∩ MOV | M0)`; explicitar qual é descritivo e qual é preditivo |
| **Crítica** | Ausência de chave oficial do episódio | Deduplicação, inferência e divisão temporal podem operar em granularidade errada | Auditoria de chaves candidatas e sensibilidade para eventos repetidos; decisão explícita antes de KPI final |
| **Alta** | Número de produtos disponíveis afeta matematicamente `qualquer movimentação` | Perfil de muitas famílias tende a ser favorecido por maior exposição a eventos | Medir `flags de movimentação / famílias presentes em M0`, taxas por família e carteira de origem; estratificar por mix |
| **Alta** | `LEAD EM ABERTO` varia por origem/mês | Viés de seleção na retenção entre atendimentos encerrados | Calcular elegibilidade e proporção de abertos por origem e mês; análises de sensibilidade e maturidade |
| **Alta** | Apenas uma escolha de modelo por Brier em outubro e teste nov/dez | Comparação parcial; não estabelece estabilidade nem generalização | Baseline por coorte, regressão penalizada, árvore interpretável, boosting, comparação por mês e rolling-origin |
| **Alta** | Brier empregado como evidência única de calibração | Brier combina calibração e resolução; não prova confiabilidade das probabilidades | Curvas de confiabilidade por faixa, calibração-in-the-large, inclinação, ECE com definição e incerteza |
| **Alta** | Comparação financeira de campos `VALOR_*` sem significado contratual validado | Risco de atribuir a renda ou margem aquilo que pode ser preço de plano | Tratar como valor observado em snapshot; conciliar famílias, descontos, cancelamentos e mudanças sem troca de código |
| **Alta** | Falta incerteza ajustada por cliente e teste de estabilidade de perfis | Falsa precisão por observações repetidas; grupos podem não se reproduzir | Bootstrap por cliente, validação por mês/origem, limiares de exposição, intervalos e análise de heterogeneidade |
| **Média** | Atributos não verificados quanto à disponibilidade exata em M0 | Potencial fuga de informação ou confusão temporal | Contrato de features: origem, momento, preenchimento, relevância, estabilidade e proibição de campos posteriores ao desfecho |
| **Média** | Apresentação precedeu avaliação de robustez | Risco de promover resultados preliminares a recomendações operacionais | Manter material marcado *preliminar*, depois sincronizar resultados finais e qualificações com notebooks |

### Descomposição de alvos

Para uma carteira inicial de atributos **X**:

- **A — Desfecho do atendimento:** `R = 1{status = RETIDO}` entre leads encerrados. Não corresponde a retenção sustentada após o período.
- **B — Movimentação condicionada:** `M = 1{alguma FLAG_MOV = 1}` entre leads `R = 1`; objetivo descritivo primário do enunciado, não alvo operacional disponível antes do atendimento.
- **C — Desfecho composto:** `Y = R × M` entre leads encerrados; estimando preditivo distinto, eventualmente utilizável em M0 se os atributos estiverem realmente disponíveis nesse instante.
- **D — Mudança econômica observada:** `ΔV = Σ VALOR_*_M30 − Σ VALOR_*_M0`; **não** é margem, LTV ou receita realizada até confirmação da unidade econômica.

A igualdade `P(R = 1, M = 1 | X) = P(R = 1 | X) × P(M = 1 | R = 1, X)` é exata como identidade probabilística; os modelos para seus fatores não se tornam causais por esse fato.

### Viés de exposição à movimentação

Se cada família disponível permitisse, *hipoteticamente* e de forma independente, movimentação com probabilidade **p**, a chance de ao menos uma mudança em **k** famílias seria `1 − (1 − p)^k`. Essa identidade demonstra o viés de oportunidade, **não** estabelece independência empírica, mesmo p entre famílias ou relacionamento causal. A investigação precisa comparar flags por oportunidade, famílias e mix inicial, não somente o evento `any`.

### Fatores que dificultam a interpretação

- Ausência de data individual da resolução do lead, impossibilitando concluir que M30 equivale a 30 dias corridos.
- Falta de informação sobre oferta apresentada, oferta aceita, custo, desconto, alternativas disponíveis e política de decisão; tratamento de oferta e uplift não são identificáveis.
- Ausência de desenho amostral/ponderação para extrapolar ao universo.
- Histórico limitado a sete meses e observações repetidas de clientes tornam o holdout temporal útil, mas insuficiente para generalização anual.
- Campos categóricos com ausência estrutural devem ser considerados como categorias distintas, não imputados arbitrariamente como comportamento do cliente.

## 2. Benchmark científico — perguntas e contribuições

| Fonte | O que acrescenta | Como será aplicado | O que não deve ser transportado |
|---|---|---|---|
| Verbeke et al. (2012), *European Journal of Operational Research*, DOI: [10.1016/j.ejor.2011.09.031](https://doi.org/10.1016/j.ejor.2011.09.031) | Seleção orientada a lucro em campanhas de churn | Incorporar matriz de custo, capacidade e cenário de valor quando houver parâmetros confiáveis | Parâmetros de outro operador e “lucro observado” não disponível |
| Jain, Khunteta e Sharma (2026), *Telecommunication Systems*, DOI: [10.1007/s11235-026-01491-3](https://doi.org/10.1007/s11235-026-01491-3) | Revisão sistemática de 199 estudos, bases e famílias de métodos | Construir checklist de benchmark, escolhas e restrições | Não usar métricas alheias como meta numérica do nosso dataset |
| Verhelst et al. (2025), *ECML PKDD*, DOI: [10.1007/978-3-031-74640-6_21](https://doi.org/10.1007/978-3-031-74640-6_21) | Benchmark de uplift em campanha de telecom | Especificar dados adicionais para mensurar incremento causal de ofertas | Não inferir efeito de tratamento quando falta alocação/intervenção válida |
| Pacella et al. (2026), *Applied Sciences*, [artigo](https://www.mdpi.com/2076-3417/16/10/4918) | Estabilidade de política, valor econômico e interpretabilidade | Repetição de treino e avaliação de estabilidade de targeting quando modelo evoluir | Não copiar desempenho sem contexto de dados/cenário experimental |
| Scikit-learn, [Calibration](https://scikit-learn.org/stable/modules/calibration.html) | Brier não basta para afirmar calibração; curva de confiabilidade é necessária | Relatório de calibração além de métricas agregadas | Não equiparar Brier menor a calibração necessariamente melhor |
| Scikit-learn, [validação temporal](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-of-time-series-data) | Avaliar no futuro, não misturar temporalidade | Splits por mês, separação de clientes e análise de maturidade de desfecho | Não aplicar TimeSeriesSplit genérico sem respeitar agrupamento de clientes |

### Benchmarks de portfólio — comparação de decisões, não de AUC

- [TheoVerhelst/Churn-Uplift-Dataset-Paper](https://github.com/TheoVerhelst/Churn-Uplift-Dataset-Paper): implementação vinculada a artigo de benchmark com dados de campanha; útil como referência de protocolo experimental com tratamento.
- [Jysee/telecom-churn-uplift-modeling](https://github.com/Jysee/telecom-churn-uplift-modeling): distingue propensão ao churn de benefício incremental, usa holdout e intervalos para não recomendar campanha sem evidência.
- [baichuan23/telecom-churn-retention-analysis](https://github.com/baichuan23/telecom-churn-retention-analysis): separação entre desempenho de churn e análise de sensibilidade econômica; estima ponto de equilíbrio sob premissas ilustrativas.
- [felipesbonatti/telco-customer-churn](https://github.com/felipesbonatti/telco-customer-churn): exemplo de workflow reproduzível com prevenção de leakage e reconhecimento de que uma única fotografia da carteira não equivale a previsão temporal.

**Regra:** as AUCs relatadas por terceiros **não são diretamente comparáveis** às do case: bases, objetivos, prevalências, desenho amostral, horizonte, tratamento e variáveis-alvo diferem. Benchmark válido requer protocolo comum aplicado aos **mesmos registros elegíveis**, com iguais splits, métricas e orçamento computacional.

## 3. Benchmark interno proposto

### Tarefas separadas

1. **Perfil entre retidos**: sumarização e modelagem descritiva condicionada a R = 1, com estratificação por quantidade/mix de produtos; não divulgar como ferramenta de decisão M0 se depende do desfecho R.
2. **Retenção inicial**: classificação R entre encerrados, sem fatores pós-atendimento.
3. **Retido com movimentação**: classificação do alvo composto Y e comparação com modelo em dois estágios; distinguir predição de decisão.
4. **Evolução monetária**: métricas de ΔV entre estados, inclusive redução sem mudança de código e retenção com cancelamento parcial; nenhuma alegação de receita causal.

### Protocolos mínimos

- **Datas:** treino jun–set, validação out, teste nov–dez como primeiro recorte; acrescentar *rolling-origin* por mês e avaliar estabilidade por período e origem.
- **Agrupamento:** não compartilhar clientes entre treino e avaliação; quantificar a seleção induzida pela exclusão de clientes recorrentes e repetir sensibilidade com regra predefinida de primeiro episódio observado.
- **Referências simples:** prevalência por treino, taxa por quantidade de famílias e taxa por mix M0 (com regularização/suavização).
- **Modelos:** regressão logística penalizada, árvore explicável e gradient boosting tabular; modelos mais complexos só quando justificam custo e ganhos em robustez.
- **Métricas:** AUROC, PR-AUC sempre acompanhada da prevalência, log loss, Brier, curvas de calibração, lift e precision@k, dispersão mensal e intervalo por cluster de cliente.
- **Explicação:** comparação de distribuição e estabilidade de características, importância por permutação no holdout para modelo candidato; colinearidade de carteiras, preço e mix exige cautela.
- **Segurança:** resultados agregados apenas no ambiente local autorizado; nunca subir notebook executado com outputs confidenciais.
- **Regras de decisão:** resultados com uma única janela de teste serão rotulados provisórios; custos, benefício marginal e causalidade só após parâmetros/documentação específica.

## 4. Portões de qualidade antes da apresentação definitiva

| Gate | Critério de aceite verificável | Situação após revisão |
|---|---|---|
| QG-01 Definição | Alvos A/B/C/D com população e denominador separados | **Especificado; validação de negócio pendente** |
| QG-02 Integridade | Eventos repetidos e tratamento de censura/abertos documentados | **Auditoria inicial, sem chave oficial** |
| QG-03 Exposição | Indicadores ajustados a família disponível e comparação por mix | **Implementação local; execução e interpretação pendentes** |
| QG-04 Modelos | Três referências não triviais, mesmas divisões e mesmo protocolo | **Pendente** |
| QG-05 Robustez | Rolling-origin, variação mês/origem e CI por cliente | **Pendente** |
| QG-06 Calibração | Curvas por bins e medida independente de ajuste médio | **Pendente** |
| QG-07 Economia | Unidades financeiras verificadas ou explicitação de hipótese | **Pendente de negócio** |
| QG-08 Divulgação | Storytelling sincronizado com análises robustas | **Apresentação atual preliminar** |

## 5. Critério para decidir o método, não o inverso

- **Descrever associação?** Taxas estratificadas, distribuições e estimativas de incerteza, com explicação das limitações.
- **Antecipar o resultado M0?** Benchmark preditivo temporal robusto e calibração.
- **Medir efetividade de ofertas?** Necessários histórico de tratamentos, elegibilidade, oferta atribuída e grupo comparável; preferir experimento randomizado de campo quando viável. Sem isso, não calcular uplift como efeito causal.
- **Estudar tempo até cancelamento?** Exige datas de início/evento/corte e censura válida; Kaplan–Meier/Cox não se justificam apenas porque a planilha contém M0/M30.
- **Decidir por margem econômica?** Exige custo das intervenções, horizonte, desconto e medida validada de receita/margem; caso contrário, somente sensibilidade parametrizada e claramente ilustrativa.

**Status:** fundamentação técnica e benchmarking de método, não conclusão ou aprovação estatística do case. Próximas entregas exigem execução e testes na base real, com rastreabilidade sem divulgação.
