# Desbalanceamento e representação das famílias de produtos

**Fonte:** amostra de atendimentos de junho a dezembro de 2025. **Unidade:** registro classificado como `RETIDO`, não cliente único confirmado. Os dados brutos permanecem fora do Git.

## Pergunta científica

As diferenças de volume entre Banda Larga (BL, **internet fixa**), TV, Fone e Móvel são diferenças de *propensão a movimentar* ou de exposição a produtos no início do atendimento? A avaliação global de qualquer movimentação esconde diferenças de previsão por família? Atribuir peso à classe minoritária melhora os resultados ou apenas altera a calibração?

## Observações da população retida

| Família presente em M0 | Registros elegíveis | Movimentos | Sem movimento | Movimentos / elegíveis |
|---|---:|---:|---:|---:|
| Banda Larga (internet fixa) | 239.562 | 74.255 | 165.307 | 31,0% |
| TV | 138.754 | 24.595 | 114.159 | 17,7% |
| Fone | 88.578 | 10.007 | 78.571 | 11,3% |
| Móvel | 10.964 | 4.387 | 6.577 | 40,0% |

Essas são **quatro classificações binárias, potencialmente simultâneas**, não uma classificação multiclasse com categorias exclusivas. Um mesmo registro pode movimentar mais de uma família. O volume bruto destaca BL, mas a taxa condicionada à presença em M0 é maior em Móvel. Portanto, rankings por volumes e rankings por incidência **não respondem à mesma pergunta**.

Há dois tipos de desbalanceamento: (1) diferente prevalência das famílias no portfólio inicial; (2) taxa de movimentação positiva versus negativa dentro de cada família elegível. O primeiro não é corrigido simplesmente aplicando `class_weight=balanced` ao modelo global.

## Protocolo de validação por família

Cada família tem alvo `FLAG_MOV_{família}=1` e população `RETIDO` com presença dessa família em M0. Divisão cronológica: treino junho–setembro, validação outubro e teste novembro–dezembro de 2025, retirando IDs compartilhados entre partições.

A comparação mantém o conjunto de teste e sua prevalência natural e avalia três referências: prevalência constante, regressão logística sem pesos e regressão logística com `class_weight='balanced'`. O ajuste de pesos acontece somente no treino. As medidas são AUROC, average precision (AP), AP/prevalência, Brier, precision@10%, recall@10% e lift@10%; Brier e AP devem ser interpretados **dentro de cada família**, considerando sua prevalência.

Desbalanceamento não implica necessariamente viés estatístico, e ponderação não garante melhora. Aumentar o peso da classe positiva pode melhorar um critério de decisão e prejudicar a confiabilidade da probabilidade. A decisão dependerá da comparação temporal e do uso de negócio.

## Limites para decisão

O funil não dispõe de aceite confirmado da oferta, custo de intervenção, chave oficial do episódio ou acompanhamento pós-retenção. A condição `RETIDO` é conhecida ao final do atendimento, portanto esta modelagem é **retrospectiva, descritiva e associativa**. Não oferece uplift causal, nem justifica política comercial automática por família.

A comparação entre famílias precisa considerar também substituição versus cancelamento parcial: `FLAG_MOV_*` e `FLAG_CANC_*` são eventos distintos.

**Artefatos:** [módulo reproduzível](../src/retention_analytics/family_balance.py), [notebook 08](../notebooks/08_family_imbalance.ipynb) e [resultados agregados](../reports/family_imbalance_2025.json).