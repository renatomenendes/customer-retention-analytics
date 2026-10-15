# Desenho analítico e reprodutibilidade

## População e indicadores

A população central contém registros classificados como `RETIDO`, com entrada no funil de junho a dezembro de 2025. A unidade é o registro, e não necessariamente um cliente único ou episódio individual confirmado.

- **Movimentação entre retidos:** registros `RETIDO` com alguma `FLAG_MOV_*` positiva / total de registros `RETIDO`.
- **Evento composto:** registros retidos com movimentação / total de atendimentos encerrados; indicador distinto do perfil entre retidos.
- **Cancelamento de produto:** ao menos uma `FLAG_CANC_*`, separado de movimentação e do status `RETIDO`.
- **Diferença de valor:** `VALOR_M30 − VALOR_M0`, em produtos e totais com valores comparáveis; não equivale a lucro ou efeito de oferta.
- **Exposição por família:** somente registros que possuíam o produto em M0 entram no denominador da respectiva movimentação.

## Atributos e interpretação

Os modelos de perfil utilizam origem, UF, classificação regional, posse móvel, mix/tamanho da carteira e valores de produtos no estado M0. As variáveis de status, flags finais, cancelamento e campos M30 não são preditores.

MPlay em M0 possui três estados: `MARCADO` (faturas unificadas), `NAO-MARCADO` (elegível) e vazio (`NAO_ELEGIVEL`). As categorias de negócio não devem ser tratadas indistintamente como ausência estatística.

## Validação dos modelos

O alvo principal é `MOV | RETIDO`, de natureza retrospectiva. O estado `RETIDO` não é conhecido no início do atendimento; o classificador não foi validado como ferramenta para pontuar todos os clientes antes do encerramento.

| Partição | Período |
|---|---|
| Treino | Junho a setembro de 2025 |
| Validação | Outubro de 2025 |
| Teste | Novembro e dezembro de 2025 |

Clientes presentes em períodos posteriores foram excluídos das partições anteriores. Registros repetidos dentro de uma mesma partição podem permanecer.

O comparativo global inclui frequência-base, regressão logística regularizada, árvore rasa e boosting tabular. A seleção utiliza Brier na validação; o teste compara AUROC, average precision, log loss, Brier, lift por capacidade e calibração.

Quatro análises adicionais condicionam a população à presença da respectiva família em M0. Nelas, a regressão sem pesos e a ponderada são comparadas sobre o mesmo teste com prevalência natural. A ponderação foi testada **sem recalibração posterior**.

## Limitações estatísticas

A inexistência de chave oficial do episódio, a seleção por desfecho `RETIDO`, a maturidade desigual dos registros em aberto e a janela limitada a sete meses restringem as inferências. O modelo não identifica aceite de oferta, tratamento causal nem retenção posterior. Não há plano amostral que sustente extrapolação para uma operadora real.

## Reprodução

```bash
python -m pip install -e '.[analysis,dev]'
retention-audit --input data/raw/retention_case.xlsx --output reports/private/audit_summary.json
retention-analyze --input data/raw/retention_case.xlsx --out-dir reports/private
python -m pytest -q
ruff check src tests
```

O repositório inclui módulos em `src/`, testes em `tests/`, notebooks de investigação em `notebooks/` e agregados em `reports/`. A planilha de origem não integra o controle de versão.
