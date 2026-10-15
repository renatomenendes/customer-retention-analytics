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

## Resultados no teste de novembro e dezembro de 2025

As quatro tarefas foram treinadas e avaliadas separadamente, cada uma apenas entre retidos que possuíam aquela família no estado M0. A frequência observada no teste não foi artificialmente balanceada.

| Família | N teste | Taxa positiva | AP baseline | AP sem pesos | AP com pesos | AUC sem pesos | AUC com pesos | Brier sem pesos | Brier com pesos |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Banda Larga (internet fixa) | 66.696 | 28,7% | 0,287 | 0,386 | 0,385 | 0,606 | 0,605 | **0,1987** | 0,2332 |
| TV | 38.086 | 17,8% | 0,178 | 0,266 | 0,259 | 0,618 | 0,612 | **0,1420** | 0,2404 |
| Fone | 23.852 | 12,1% | 0,121 | 0,171 | 0,177 | 0,551 | 0,574 | **0,1061** | 0,2219 |
| Móvel | 3.560 | 40,7% | 0,407 | 0,474 | 0,468 | 0,569 | 0,571 | **0,2381** | 0,2563 |

**Resultado dos pipelines testados:** os pesos balanceados, **sem recalibração posterior das probabilidades**, pioraram o Brier **nas quatro famílias**. Como a ponderação altera a probabilidade estimada, esta comparação não demonstra que um modelo ponderado e posteriormente calibrado teria necessariamente desempenho inferior. Em Fone, elevaram a AUC de 0,551 para 0,574 e a precision@10% de 20,0% para 21,9%, mas o Brier passou de 0,1061 para 0,2219. Ganho de ranking não equivale a boa probabilidade.

Em Móvel, o Brier da validação de outubro favoreceu marginalmente o modelo balanceado (0,24868 versus 0,24947), mas novembro–dezembro favoreceu o modelo sem pesos (0,23812 versus 0,25632). A pequena vantagem de validação não se sustentou temporalmente.

**Implicação:** não aplicar `class_weight='balanced'` por padrão. Se a intervenção tiver capacidade limitada, avaliar ranking e precision/recall@k; se a probabilidade for usada na decisão, preservar calibração e Brier por família. Nenhum desses modelos foi validado como ação comercial ex-ante ou como probabilidade de aceite.

A implementação usa variáveis categóricas iniciais e faixas de valor M0, codificação esparsa e regressão logística via SGD, em vez de replicar a regressão do alvo global. O arquivo agregado contém os desempenhos das três referências, incluindo AP/prevalência e recall@10%. Os números publicados foram arredondados; a execução local conserva precisão integral.

## Limites para decisão

O funil não dispõe de aceite confirmado da oferta, custo de intervenção, chave oficial do episódio ou acompanhamento pós-retenção. A condição `RETIDO` é conhecida ao final do atendimento, portanto esta modelagem é **retrospectiva, descritiva e associativa**. Não oferece uplift causal, nem justifica política comercial automática por família.

A comparação entre famílias precisa considerar também substituição versus cancelamento parcial: `FLAG_MOV_*` e `FLAG_CANC_*` são eventos distintos.

**Artefatos:** [módulo reproduzível](../src/retention_analytics/family_balance.py), [notebook 08](../notebooks/08_family_imbalance.ipynb) e [resultados agregados](../reports/family_imbalance_2025.json).