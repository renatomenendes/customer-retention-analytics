# Defesa executiva — Retenção com movimentação de produtos

**Junho–dezembro/2025 · estudo observacional · uso restrito**

Este roteiro sintetiza a apresentação PowerPoint de 20 slides. O recorte e o significado das variáveis seguem `Objetivo do Case.docx` e a documentação metodológica do estudo.

## Questão central

**Quais características distinguem registros `RETIDO` com movimentação dos registros `RETIDO` sem movimentação?** Os produtos abrangidos são Banda Larga, TV, Fone e Móvel. A população condicional é `RETIDO=1`, não todos os leads encerrados.

## Achados para discussão

1. Foram analisados 303.652 registros na janela. Destes, 249.309 foram classificados como retidos; 86.540 tiveram movimentação (34,7% entre retidos).
2. A composição inicial do portfólio altera a frequência de movimentação, mas o número de famílias também aumenta mecanicamente a chance de observar ao menos uma alteração. A incidência por oportunidade M0 e o mix precisam ser considerados juntos.
3. MPlay, posse de móvel e origem do atendimento mostram heterogeneidade observada. MPlay tem preenchimento estruturalmente desigual e a origem tem desfechos pendentes muito assimétricos.
4. Cerca de 15,2% dos retidos movimentados também possuem alguma flag de cancelamento de produto. Movimentar não é preservar integralmente a carteira.
5. O documento do case define `valor` como valor pago associado ao lead. Nos retidos que movimentaram, a mediana M30−M0 foi −25,46 e 78,7% apresentaram redução; sem competência de cobrança ou custo não há inferência de efeito incremental nem margem.
6. O **aceite verdadeiro da oferta não é observado**. A proxy de troca contratual não cancelada coincide com a flag de movimentação para os 86.540 registros: não gera informação adicional. Simulações de aceite são hipóteses, não resultados medidos.
7. O benchmark com o **alvo correto** comparou baseline, regressão regularizada, árvore curta e gradient boosting no mesmo teste cronológico. Boosting: AUC 0,650, AP 0,487, Brier 0,2065, lift top 10% 1,81×. Baseline: Brier 0,2216. O modelo é retrospectivo e associativo; não é avaliação de intervenções.
8. A taxa de movimentação mudou de 34,7% entre todos os registros retidos para 34,8% quando se selecionou apenas o primeiro retido observado por ID — exercício de sensibilidade, não definição oficial de episódio.

## Decisões testáveis

- Estratificar o estudo e futuros testes de oferta por composição inicial e elegibilidade real de famílias.
- Auditar downgrade, migração, cancelamento parcial e consequências monetárias de cada transição.
- Revisar maturidade dos leads antes de comparar `SOLAR` e `LEGADO`.
- Instrumentar oferta apresentada, aceite, desconto e faturamento; comparar propostas por experimento controlado, com retenção posterior e valor financeiro reconhecido.

## Respostas ao questionamento técnico

**Por que não modelar apenas `RETIDO ∧ MOV`?** Porque combina duas perguntas. A análise principal é `MOV | RETIDO`; a anterior é secundária.

**Por que não apresentar aceites?** Porque falta campo de decisão. A hipótese de aceite pode orientar investigação, mas a movimentação não é rótulo observado de aceite.

**O boosting causou mais movimentações?** Não. Seu desempenho discrimina eventos observados em outra janela; isso não mede efeito de oferta.

**Há perda de receita?** Há redução de valores registrados entre snapshots. Sem reconciliação contábil e atribuição causal, não afirmamos perda incremental ocasionada por ofertas.

**O que falta para decisão de implantação?** Identificador do episódio, rótulo de oferta, data e permanência do desfecho, faturamento e desenho experimental.

Consulte o [relatório detalhado](../docs/study_report.md), os [notebooks](../notebooks/) e os [resultados agregados](../reports/retained_profile_study_2025.json).
