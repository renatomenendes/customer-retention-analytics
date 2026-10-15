# Cobertura analítica e alcance dos resultados

**Período:** junho a dezembro de 2025. **Unidade:** registro do funil de retenção.

A tabela relaciona as perguntas de pesquisa às evidências disponíveis e aos limites de interpretação.

| Dimensão | Resultado ou procedimento | Alcance |
|---|---|---|
| Universo e desfechos | 303.652 registros no período; 249.309 classificados como `RETIDO`; 48.091 como `NAO RETIDO`; 6.252 em aberto | Frequências por registro, não necessariamente por cliente único |
| Movimentação entre retidos | 86.540 retidos com alguma `FLAG_MOV_*` (34,7%) | Evento contratual observado; não comprova aceite de oferta |
| Perfis iniciais | Mix, quantidade de famílias, região, MPlay, origem, classificação e posse móvel | Associações observacionais dentro do grupo retido |
| Exposição por família | Taxas por produto presente em M0 e por composição inicial de carteira | Famílias não mutuamente exclusivas; elegibilidade muda o denominador |
| Cancelamentos e movimentações | Cruzamentos `FLAG_MOV_*` × `FLAG_CANC_*`, transições de códigos M0/M30 | Cancelamento de produto não implica necessariamente perda do relacionamento |
| Valores M0/M30 | Distribuição da diferença registrada, por segmento e transição | Não representa margem ou receita incremental causal |
| Modelagem global | Prevalência, regressão logística, árvore e boosting no mesmo teste cronológico | Discriminação retrospectiva de `MOV | RETIDO`, não recomendação operacional em M0 |
| Modelagem por família | AUROC, AP, Brier, lift e sensibilidade a pesos de classe | Prevalências diferentes; ponderação comparada sem recalibração posterior |
| Validação | Treino junho–setembro, validação outubro, teste novembro–dezembro; exclusão de clientes compartilhados entre partições | Uma janela temporal, sem evidência de estabilidade anual |
| Aplicações comerciais | Hipóteses de segmentação, monitoramento de cancelamentos e avaliação de ofertas | Exigem mensuração prospectiva antes da adoção operacional |

## Limitações de identificação

O conjunto de dados não contém identificador inequívoco do episódio, registro da oferta apresentada e da decisão de aceite, data individual de encerramento, série de faturamento conciliado nem acompanhamento posterior do relacionamento. Essas ausências impedem estimar aceite verdadeiro, efeito causal das ofertas, permanência futura e lucro incremental.

As conclusões se restringem à população e aos eventos registrados, preservando a distinção entre associação, predição retrospectiva e resultado comercial efetivo.
