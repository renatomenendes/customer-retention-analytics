# Protocolo de auditoria reproduzível

## Estado

A planilha está acessível localmente. Há um relatório anterior e arquivos JSON de auditoria, mas este pacote não reexecutou as métricas. Seus números permanecem **resultados preexistentes pendentes de reprodução**.

## Inventário mínimo

- Fonte: planilha `.xlsx` disponibilizada ao responsável; caminho e fingerprint mantidos em manifesto local não versionado.
- Aba informada: `bd_case_final_1`.
- Datas-alvo: entrada no funil entre 2025-06-01 00:00:00 e 2025-12-31 23:59:59, no fuso a confirmar.
- Colunas candidatas: `id_cliente`, `DATA_FUNIL_SOLAR`, `NM_SUB_INDICADOR_NEGOCIO`, `FLAG_ORIGEM`, produtos M0/M30, flags por família e valores M0/M30.
- Chave primária do episódio: **não demonstrada**.

## Sequência de testes (a implementar e executar)

| ID | Teste | Evidência esperada | Critério inicial |
|---|---|---|---|
| DQ-01 | Abrir planilha completa, não apenas intervalo nomeado | Aba, linhas, colunas, fingerprint | Nenhuma truncagem silenciosa |
| DQ-02 | Contar linhas por data de entrada | Distribuição mensal e fora da janela | Excluir fora de escopo com contagem |
| DQ-03 | Verificar IDs nulos, repetidos, timestamps e status conflitantes | Quantidade por padrão de repetição | Não descartar antes de definir episódio |
| DQ-04 | Classificar valores ausentes e sentinelas | Taxa por coluna e família | Distinguir ausência estrutural de falha |
| DQ-05 | Conferir domínio das flags/status | Frequências e violações | Valores não documentados em quarentena |
| DQ-06 | Reconciliar transições M0/M30 | Tabelas por produto e tipo de alteração | Divergências documentadas |
| DQ-07 | Verificar valor monetário por unidade/família | Nulos, zero, negativos, extremos | Não imputar/desconsiderar sem regra |
| DQ-08 | Verificar origem × mês × status aberto | Cobertura e maturidade | Sem comparações enviesadas não sinalizadas |
| DQ-09 | Validar fuga de informação temporal | Lista de variáveis M0 versus M30 | Nenhuma variável futura em features preditivas |
| DQ-10 | Avaliar risco de divulgação | Granularidade de agregações | Nenhum identificador ou grupo sensível divulgado |

## Rastreabilidade

Cada execução deve registrar hash SHA-256 da fonte local, versões do ambiente, instante de execução, regras de recorte, contagem inicial/final, testes e motivos de exceção. Logs e resultados detalhados permanecem em diretórios ignorados pelo Git.

## Bloqueadores

- Confirmar identidade de lead/episódio e data efetiva de desfecho.
- Validar significados dos campos financeiros e das flags.
- Confirmar processo de seleção da amostra e condições de divulgação.
