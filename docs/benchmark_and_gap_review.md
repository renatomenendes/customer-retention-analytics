# Fundamentação científica e escolha dos métodos

O desenho combina caracterização retrospectiva da movimentação entre retidos, estudo das transições de produto, análise de valores M0/M30 e validação temporal de modelos. Cada pergunta exige população, desfecho e evidência compatíveis.

## Definições estatísticas e exposição por produto

### Descomposição de alvos

Para uma carteira inicial de atributos **X**:

- **A — Desfecho do atendimento:** `R = 1{status = RETIDO}` entre leads encerrados. Não corresponde a retenção sustentada após o período.
- **B — Movimentação condicionada:** `M = 1{alguma FLAG_MOV = 1}` entre leads `R = 1`; objetivo descritivo primário do enunciado, não alvo operacional disponível antes do atendimento.
- **C — Desfecho composto:** `Y = R × M` entre leads encerrados; estimando preditivo distinto, eventualmente utilizável em M0 se os atributos estiverem realmente disponíveis nesse instante.
- **D — Mudança econômica observada:** `ΔV = Σ VALOR_*_M30 − Σ VALOR_*_M0`; **não** é margem, LTV ou receita realizada até confirmação da unidade econômica.

A igualdade `P(R = 1, M = 1 | X) = P(R = 1 | X) × P(M = 1 | R = 1, X)` é exata como identidade probabilística; os modelos para seus fatores não se tornam causais por esse fato.

### Viés de exposição à movimentação

Se cada família disponível permitisse, *hipoteticamente* e de forma independente, movimentação com probabilidade **p**, a chance de ao menos uma mudança em **k** famílias seria `1 − (1 − p)^k`. Essa identidade demonstra o viés de oportunidade, **não** estabelece independência empírica, mesmo p entre famílias ou relacionamento causal. A comparação considera flags por oportunidade, famílias e mix inicial, além do evento agregado.

### Fatores que dificultam a interpretação

- Ausência de data individual da resolução do lead, impossibilitando concluir que M30 equivale a 30 dias corridos.
- Falta de informação sobre oferta apresentada, oferta aceita, custo, desconto, alternativas disponíveis e política de decisão; tratamento de oferta e uplift não são identificáveis.
- Ausência de desenho amostral/ponderação para extrapolar ao universo.
- Histórico limitado a sete meses e observações repetidas de clientes tornam o holdout temporal útil, mas insuficiente para generalização anual.
- Campos categóricos com ausência estrutural devem ser considerados como categorias distintas, não imputados arbitrariamente como comportamento do cliente.


## Referências metodológicas

| Fonte | O que acrescenta | Utilidade metodológica | O que não deve ser transportado |
|---|---|---|---|
| Verbeke et al. (2012), *European Journal of Operational Research*, DOI: [10.1016/j.ejor.2011.09.031](https://doi.org/10.1016/j.ejor.2011.09.031) | Seleção orientada a lucro em campanhas de churn | Referência para análise econômica quando custos e ganhos forem observados | Parâmetros de outro operador e “lucro observado” não disponível |
| Jain, Khunteta e Sharma (2026), *Telecommunication Systems*, DOI: [10.1007/s11235-026-01491-3](https://doi.org/10.1007/s11235-026-01491-3) | Revisão sistemática de 199 estudos, bases e famílias de métodos | Comparação de desenho, métricas e limitações | Não usar métricas alheias como meta numérica do nosso dataset |
| Verhelst et al. (2025), *ECML PKDD*, DOI: [10.1007/978-3-031-74640-6_21](https://doi.org/10.1007/978-3-031-74640-6_21) | Benchmark de uplift em campanha de telecom | Definição dos requisitos para estimar efeito incremental | Não inferir efeito de tratamento quando falta alocação/intervenção válida |
| Pacella et al. (2026), *Applied Sciences*, [artigo](https://www.mdpi.com/2076-3417/16/10/4918) | Estabilidade de política, valor econômico e interpretabilidade | Referência para estabilidade e avaliação econômica | Não copiar desempenho sem contexto de dados/cenário experimental |
| Scikit-learn, [Calibration](https://scikit-learn.org/stable/modules/calibration.html) | Brier não basta para afirmar calibração; curva de confiabilidade é necessária | Relatório de calibração além de métricas agregadas | Não equiparar Brier menor a calibração necessariamente melhor |
| Scikit-learn, [validação temporal](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-of-time-series-data) | Avaliar no futuro, não misturar temporalidade | Splits por mês, separação de clientes e análise de maturidade de desfecho | Não aplicar TimeSeriesSplit genérico sem respeitar agrupamento de clientes |

### Benchmarks de portfólio — comparação de decisões, não de AUC

- [TheoVerhelst/Churn-Uplift-Dataset-Paper](https://github.com/TheoVerhelst/Churn-Uplift-Dataset-Paper): implementação vinculada a artigo de benchmark com dados de campanha; útil como referência de protocolo experimental com tratamento.
- [Jysee/telecom-churn-uplift-modeling](https://github.com/Jysee/telecom-churn-uplift-modeling): distingue propensão ao churn de benefício incremental, usa holdout e intervalos para não recomendar campanha sem evidência.
- [baichuan23/telecom-churn-retention-analysis](https://github.com/baichuan23/telecom-churn-retention-analysis): separação entre desempenho de churn e análise de sensibilidade econômica; estima ponto de equilíbrio sob premissas ilustrativas.
- [felipesbonatti/telco-customer-churn](https://github.com/felipesbonatti/telco-customer-churn): exemplo de workflow reproduzível com prevenção de leakage e reconhecimento de que uma única fotografia da carteira não equivale a previsão temporal.

**Regra:** as AUCs relatadas por terceiros **não são diretamente comparáveis** às do case: bases, objetivos, prevalências, desenho amostral, horizonte, tratamento e variáveis-alvo diferem. Benchmark válido requer protocolo comum aplicado aos **mesmos registros elegíveis**, com iguais splits, métricas e orçamento computacional.


## Aplicabilidade dos métodos

- **Descrever associação?** Taxas estratificadas, distribuições e estimativas de incerteza, com explicação das limitações.
- **Antecipar o resultado M0?** Benchmark preditivo temporal robusto e calibração.
- **Medir efetividade de ofertas?** Necessários histórico de tratamentos, elegibilidade, oferta atribuída e grupo comparável; preferir experimento randomizado de campo quando viável. Sem isso, não calcular uplift como efeito causal.
- **Estudar tempo até cancelamento?** Exige datas de início/evento/corte e censura válida; Kaplan–Meier/Cox não se justificam apenas porque a planilha contém M0/M30.
- **Decidir por margem econômica?** Exige custo das intervenções, horizonte, desconto e medida validada de receita/margem; na ausência desses dados, apenas sensibilidade a parâmetros hipotéticos.

