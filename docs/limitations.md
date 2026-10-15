# Alcance e limitações dos resultados

| Dimensão | Restrição observada | Implicação metodológica |
|---|---|---|
| Unidade de análise | `id_cliente` pode aparecer em múltiplos registros; sem identificador oficial de episódio | Frequências por registro, não contagens confirmadas de episódios ou clientes únicos |
| Retenção | O status representa encerramento do atendimento | Não mede permanência futura |
| Atendimentos em aberto | Proporções variáveis entre mês e origem | Comparações de desfecho dependem da maturidade do funil |
| Temporalidade | M0/M30 representam estados sem timestamps individuais completos | Não estimar duração de permanência nem curvas de sobrevivência |
| Movimentação | Flags e transições de códigos não representam necessariamente o mesmo evento | Examinar movimentação e cancelamento separadamente |
| Aceite de oferta | Não há histórico de propostas e decisões | Não estimar taxa verdadeira de aceite |
| Valores | Não há faturamento conciliado, custos ou margem | Diferenças M30−M0 são mudanças registradas, não resultado financeiro incremental |
| Amostragem | Não há plano probabilístico conhecido | Resultados caracterizam a amostra, sem extrapolação populacional |
| Modelagem | Condicionada ao status `RETIDO`, observado ao término | Aplicação retrospectiva, sem validação para decisão inicial |
| Validação | Teste de novembro–dezembro, dentro da série de sete meses | Não demonstra estabilidade anual nem generalização externa |
| Observações repetidas | Possível dependência entre registros do mesmo cliente | Segregação entre treino e teste reduz vazamento, mas não remove toda dependência |
| Inferência causal | Sem designação de ofertas e controles comparáveis | Associações não identificam impacto de intervenção |

## Consequências para a interpretação

As duas proxies de movimentação contratual coincidem nos registros retidos analisados e, portanto, não constituem medidas independentes de aceite de oferta. As variações de valor acompanham estados de carteira, mas não identificam efeitos financeiros atribuíveis a uma intervenção específica.

No teste por produto, diferenças de prevalência e de exposição exigem leitura conjunta de AUROC, average precision, Brier e medidas de capacidade. A comparação com ponderação refere-se aos pipelines executados, sem recalibração posterior.

As recomendações descrevem possibilidades de avaliação prospectiva, sem estimativas observadas de ganho incremental.
