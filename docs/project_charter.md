# Escopo e questões de pesquisa

## Objetivo

Caracterizar os perfis associados à movimentação de produtos entre atendimentos classificados como retidos, considerando a carteira inicial, as transições contratuais e as mudanças de valor registradas no processo.

## Questões investigadas

1. Qual é a composição dos atendimentos de retenção entre junho e dezembro de 2025?
2. Quais características iniciais distinguem registros retidos com e sem movimentação de produtos?
3. Como a presença de Banda Larga (internet fixa), TV, Telefonia Fixa e Móvel altera os denominadores e as taxas de movimentação?
4. Como movimentação e cancelamento de produtos se relacionam com a diferença de valores entre M0 e M30?
5. Qual é a capacidade discriminatória dos modelos e como ela varia entre famílias de produto?
6. Quais recomendações podem ser formuladas para avaliação prospectiva?

## População e definições

- **Unidade:** registro de atendimento; `id_cliente` pode ocorrer mais de uma vez e não representa uma chave de episódio confirmada.
- **Recorte:** registros com entrada no funil entre 1º de junho e 31 de dezembro de 2025.
- **Retenção operacional:** status `RETIDO`, distinto da permanência futura do cliente.
- **Movimentação:** ocorrência de ao menos uma `FLAG_MOV_*` entre os retidos.
- **Cancelamento de produto:** ocorrência de `FLAG_CANC_*`, evento distinto da movimentação e do status do atendimento.
- **M0/M30:** condições inicial e final informadas; a nomenclatura não comprova intervalo de trinta dias.
- **Valores:** campos monetários nos dois estados; suas diferenças não são uma estimativa de lucro ou de efeito causal.

## Desenho analítico

A investigação combina auditoria descritiva, estratificação por carteira e origem, análise de transições, estudo de valores, comparação de modelos em divisão temporal e avaliação de desempenho por família. O alvo central é `P(MOV=1 | RETIDO=1, X_M0)`, interpretado retrospectivamente.

As conclusões são limitadas à amostra demonstrativa. A ausência de aceite de oferta observado e de acompanhamento financeiro posterior impede estimar efeitos incrementais das intervenções.
