# Escolhas metodológicas e definições analíticas

| Tema | Critério utilizado | Consequência para a interpretação |
|---|---|---|
| Unidade de análise | Registro do funil; `id_cliente` não equivale a episódio único | Frequências por registro; dependência entre registros repetidos precisa ser considerada |
| Retenção | `NM_SUB_INDICADOR_NEGOCIO = RETIDO` | Desfecho operacional, sem evidência de permanência futura |
| Atendimentos em aberto | Categoria separada de `RETIDO` e `NAO RETIDO` | Comparações entre canais devem considerar maturidade desigual |
| Movimentação | Qualquer `FLAG_MOV_*` positiva | Evento distinto de cancelamento e de aceite de oferta |
| Cancelamento | `FLAG_CANC_*` por produto | Não equivale automaticamente à perda integral do relacionamento |
| Valores | Diferença M30−M0 quando há pares válidos | Variação de valor registrado, sem atribuição causal a ofertas |
| MPlay | `MARCADO` = faturas unificadas; `NAO-MARCADO` = elegível; vazio = não elegível | Ausência estrutural é categoria de negócio, não valor estatístico desconhecido |
| Perfil central | `P(MOV=1 | RETIDO=1, X_M0)` | Caracterização retrospectiva entre retidos |
| Modelo | Baseline, regressão logística, árvore e boosting; seleção por Brier em outubro | Avaliação comum em novembro–dezembro, com partições sem clientes compartilhados |
| Desbalanceamento | Modelos separados por família presente em M0; prevalência preservada no teste | Ponderação sem recalibração posterior não melhorou o Brier |
| Inferência comercial | Recomendações associadas a evidências descritivas | Aceite, lucro incremental e efeito de tratamento exigem dados adicionais |

## Limites de identificação

A base não identifica a oferta apresentada ou aceita, a duração individual de permanência, a competência contábil do faturamento ou uma chave inequívoca do episódio. Essas variáveis são necessárias para avaliar eficácia causal de intervenções e resultados financeiros incrementais.

A análise temporal evita compartilhar IDs de clientes entre treino, validação e teste, mas não substitui validação externa ou comprovação de estabilidade anual.
