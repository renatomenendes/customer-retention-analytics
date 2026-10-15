# Metodologia

## População e unidade de análise

O estudo considera registros de atendimentos de retenção iniciados entre junho e dezembro de 2025. Cada linha representa uma observação do funil; a repetição de `id_cliente` impede tratar todos os registros como clientes únicos. O status `RETIDO` caracteriza o desfecho operacional do atendimento, não a permanência futura do relacionamento.

Os registros `NAO RETIDO` e `LEAD EM ABERTO` são categorias distintas. A proporção de atendimentos em aberto varia por origem e mês, o que limita a comparabilidade direta das taxas entre canais.

## Desfechos

- **Movimentação:** ao menos uma `FLAG_MOV_{BL,TV,FONE,MV}=1` entre os registros retidos.
- **Cancelamento de produto:** `FLAG_CANC_*=1`, evento separado de movimentação e da classificação do atendimento.
- **Transições de carteira:** inclusões, retiradas, substituições e permanências identificadas pela comparação dos códigos de produto/plano M0 e M30.
- **Mudança de valor:** diferença entre os campos `VALOR_*` nos estados M0 e M30 para pares válidos. O intervalo temporal entre esses estados não está confirmado como trinta dias.

A modelagem central estima `P(MOV=1 | RETIDO=1, X_M0)`. O condicionamento ao status final torna o classificador **retrospectivo**: ele descreve os perfis dos retidos, sem constituir uma recomendação aplicável a todos os clientes no início do funil.

## Composição da carteira e MPlay

A análise de movimentação por família usa somente os registros com aquela família presente em M0. As quatro famílias não constituem classes exclusivas; um registro pode movimentar mais de uma.

A variável `DSC_CLI_MPLAY_M0` diferencia três estados: `MARCADO`, faturas unificadas; `NAO-MARCADO`, elegível à unificação; **campo vazio**, não elegível. O vazio é codificado como `NAO_ELEGIVEL`, preservando seu significado operacional.

## Comparação de modelos

Treino: junho–setembro; validação: outubro; teste: novembro–dezembro de 2025. IDs de clientes presentes em períodos posteriores foram excluídos das partições anteriores. Registros repetidos dentro da mesma partição podem permanecer.

Os modelos globais comparados são prevalência constante, regressão logística regularizada, árvore de decisão e gradient boosting. A seleção utiliza o Brier de validação, e a avaliação comum inclui AUROC, average precision, log loss, Brier, lift no decil superior e inspeção de calibração.

Os modelos específicos por família utilizam a mesma divisão temporal. Foram comparadas regressões sem e com ponderação de classes, com prevalência natural no teste. **Não houve recalibração posterior das probabilidades ponderadas.** O resultado desse confronto não determina o desempenho de alternativas recalibradas.

## Inferência e limitações

Os contrastes de perfil, origem, movimentação, cancelamento e valor são **associações observacionais**. A inexistência de registro de oferta apresentada/aceita, de um desfecho de permanência posterior e de faturamento conciliado impede estimar aceite verdadeiro, uplift causal e lucro incremental.

A ausência de chave única oficial de episódio e de amostragem probabilística identificada limita a independência das observações e a generalização para operações reais.
