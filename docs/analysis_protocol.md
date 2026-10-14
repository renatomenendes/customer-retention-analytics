# Protocolo analítico — perfis, snapshots econômicos e modelo experimental

## Fontes e segregação

A planilha original permanece exclusivamente no ambiente local autorizado. O código gera agregados em `reports/private/` e não grava linhas individuais, IDs ou estimadores treinados. Os notebooks versionados não contêm outputs executados com dados reais; estes permanecem em `notebooks/.executed/`.

## Pergunta, população e unidade

**Pergunta descritiva:** quais atributos disponíveis em M0 estão associados à movimentação entre registros classificados como `RETIDO`?

**Unidade:** linha da planilha, **candidata** a episódio do funil. Não é cliente único nem observação longitudinal validada. Não deduplicar automaticamente por `id_cliente`.

**Elegibilidade temporal:** entrada entre junho e dezembro de 2025, inclusive. O desfecho operacional provisório usa `NM_SUB_INDICADOR_NEGOCIO`; movimentos usam OR lógico das quatro `FLAG_MOV`. `LEAD EM ABERTO` não é classificado como fracasso.

**Métricas:**

- Movimentação entre retidos = retidos com pelo menos uma flag de movimentação / todos os retidos.
- Evento composto entre fechados = retidos com movimentação / (`RETIDO` + `NAO RETIDO`).
- Variação monetária observada = soma de `VALOR_{BL,TV,FONE,MV}_M30` menos soma equivalente em M0, apenas quando todos os campos da comparação estão preenchidos. Não é receita faturada.
- Grupos descritivos com n < 100 são suprimidos. Intervalos de Wilson são descritivos e podem subestimar a incerteza por repetição de clientes.

## Transformações e atributos

Atributos de entrada: origem, UF, classificação de cidade, elegibilidade para faturas M0, flag móvel, número de famílias M0, presença de cada família em M0 e valores M0 de BL/TV/MV. IDs de cliente, status final, flags de movimentação, cancelamento e campos M30 **não entram como features preditivas**.

A informação de produto e valores em M0 depende de comprovação de disponibilidade no instante da decisão. A interpretação de `CLASSIFICACAO` e `MPLAY` requer validação do negócio. Geografia é uma variável sensível à transferência entre canais e à composição da amostra.

## Modelagem

Alvo experimental: evento composto `RETIDO` e qualquer `FLAG_MOV=1`, entre os episódios com status encerrado. Essa tarefa não deve ser confundida com `movimentação | RETIDO` e **não** estima efeito incremental de oferta.

- Treino: junho–setembro de 2025.
- Validação: outubro de 2025.
- Teste: novembro–dezembro de 2025.
- IDs de clientes que aparecem em períodos posteriores são removidos dos anteriores; registros repetidos dentro de um mesmo período permanecem.
- Baseline: probabilidade constante segundo prevalência do treino.
- Candidatos: regressão logística regularizada e árvore de decisão rasa, com imputação e one-hot codificadas pelo treino.
- Modelo é selecionado **uma vez** pelo menor Brier score de validação, teste reservado ao final.
- Discriminação: AUC-ROC, average precision e lift no decil superior; calibração: Brier e log-loss. Se scores são constantes, lift@10 é 1 por ausência de ranking.

## Limitações não resolvidas

1. Chave de episódio não foi formalizada; a exclusão de IDs entre splits reduz, mas não elimina, dependência de registros.
2. M30 não representa necessariamente exatamente 30 dias após M0; não há horizonte de evento individual validado.
3. Leads abertos são excluídos da modelagem, com potencial viés de fechamento por mês e origem.
4. Taxas de amostra não representam automaticamente o universo da empresa.
5. Campos monetários não definem periodicidade, descontos, impostos, créditos e bundles; delta não prova preservação de receita real.
6. Importância de feature ou desempenho preditivo não comprova causalidade ou impacto de negócio.
7. A validação abrange apenas a série de sete meses; não permite alegação de estabilidade, justiça de tratamento ou viabilidade de produção.

## Reprodutibilidade e privacidade

```bash
python -m pip install -e '.[analysis,dev]'
retention-audit --input data/raw/retention_case.xlsx --output reports/private/audit_summary.json
retention-analyze --input data/raw/retention_case.xlsx --out-dir reports/private
python -m pytest -q
ruff check src tests
```

Depois, executar sequencialmente os notebooks `01`, `02`, `03` e `04`. Somente dados sintéticos fazem parte do CI. A execução sobre dados reais, relatórios, figuras, modelos ajustados e apresentações confidenciais permanecem locais, sem push.
