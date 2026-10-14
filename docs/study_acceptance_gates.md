# Critérios de conclusão do estudo frente ao enunciado do case

**Referência:** `Objetivo do Case.docx`, três páginas. **Recorte:** junho a dezembro de 2025. Esta matriz descreve o escopo *mensurável na fonte recebida*, não o ciclo de desenvolvimento do repositório.

| Pergunta ou entrega | Evidência produzida | Limite documentado |
|---|---|---|
| Caracterização descritiva da amostra | Auditoria da planilha completa, 303.652 registros no recorte, status, repetições e evolução mensal | Registro do funil sem chave oficial de episódio |
| Identificar retidos com movimentação | 249.309 `RETIDO`; 86.540 com alguma `FLAG_MOV`, 34,7% entre retidos | O rótulo é o status do atendimento, não sobrevivência futura |
| Identificar perfis entre retidos | Mix inicial, quantidade de famílias, região/UF, MPlay, origem, classificação e posse móvel; taxas com denominadores explícitos | Grupos não têm efeito causal; MPlay tem grande parcela sem informação |
| Conferir se a maior movimentação de multiprodutos é estrutural | Taxa por qualquer movimentação e incidência por família presente em M0 | Normalização por oportunidade não elimina seleção de ofertas |
| Aceite de ofertas | Hipótese explicitada, testadas flags e proxy de alteração contratual; coincidência das duas na amostra | **Não identificável** como taxa verdadeira sem oferta apresentada e decisão registrada; qualquer simulação é rotulada hipótese |
| Explorar produtos BL, TV, Fone, MV | Transições de códigos M0/M30, flags de movimento e cancelamento, variações de valor por família | Cancelamento parcial não representa churn de relacionamento |
| Examinar valor pago associado ao lead | Δ valores M0/M30, sinal de redução, resumo por transição e família | Sem conciliação de faturamento, não se afirma margem ou efeito incremental |
| Modelagem analítica adequada à pergunta central | Baseline, regressão regularizada, árvore curta e boosting para `MOV` entre retidos, mesmo teste temporal, AP/AUC/Brier/log-loss/lift e calibração | **Retenção condicionante** conhecida apenas após atendimento; não aplicar pontuação ex-ante à população geral |
| Robustez e explicação | Teste nov–dez, métricas por mês/origem, split disjunto por cliente e sensibilidade primeiro registro retido por ID | Não há histórico pós-dezembro nem chave oficial do episódio |
| Notebook documentado e apresentação | Notebooks 01–06, síntese executada com agregados, relatório e apresentação de 20 slides | Dados confidenciais não versionados; artefatos descrevem associação e hipóteses |
| Estratégia de retenção | Seis recomendações associadas a evidência, público/tema, KPI e desenho de validação | Ganhos incrementais exigem medição causal e financeira adicional |

## Limites da fonte, não itens disfarçados de análise concluída

Sem **ID do lead**, **registro da oferta apresentada/aceita**, **data individual de encerramento**, **faturamento conciliado por competência**, **histórico de retenção posterior** e **plano amostral**, certas afirmações não são estimáveis. O estudo deve demonstrar esses limites e **não inventar valores** para satisfazer formalmente o enunciado.

O repositório privado mantém a investigação observacional e sua documentação. Qualquer divulgação pública de números agregados exige liberação específica.
