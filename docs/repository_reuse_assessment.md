# Princípios de reprodutibilidade e interpretação

## Granularidade e integridade

Cada indicador deve especificar sua unidade de análise, população, período, numerador e denominador. No estudo de retenção, a linha do funil não pode ser equiparada automaticamente a cliente único ou a episódio de atendimento. A ausência de uma chave inequívoca limita deduplicações e análises longitudinais.

A consistência entre `FLAG_MOV_*`, `FLAG_CANC_*` e códigos de produto M0/M30 é verificada por família. Inclusão, retirada, substituição e permanência constituem transições distintas.

## Temporalidade e validação

A construção das variáveis diferencia informações de entrada (M0) dos estados posteriores (M30). O comparativo de modelos usa treino, validação e teste em ordem temporal, sem compartilhar clientes entre partições. Essa precaução reduz vazamento de informação, mas não constitui validação em período externo.

## Inferência e decisão

- **Descrição:** taxas condicionais por família, composição de carteira e origem.
- **Predição retrospectiva:** discriminação de movimentação entre registros já classificados como retidos.
- **Causalidade:** requer intervenção observável e estratégia de identificação apropriada.
- **Sobrevivência:** requer tempos de origem, evento e censura; a existência de snapshots M0/M30 não fornece essas durações.
- **Economia:** comparações de valor registrado não substituem receita reconhecida, margem ou custo de intervenção.

## Critérios de comunicação científica

Os resultados são apresentados com denominadores e períodos compatíveis. Diferenças de desempenho entre produtos devem considerar prevalência, tamanho dos grupos e a métrica escolhida. Recomendações operacionais são hipóteses avaliáveis, não efeitos identificados pelos dados observacionais.
