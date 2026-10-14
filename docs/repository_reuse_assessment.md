# Reutilização crítica de referências técnicas

**Revisão:** 2026-10-14  
**Situação:** referências consultadas; análise e modelos do case não foram reexecutados por esta revisão.  
**Escopo:** aprendizagem metodológica e arquitetural, sem cópia de código, dados, imagens ou configurações entre repositórios.

## Critérios para incorporação

Uma prática só entra no `customer-retention-analytics` quando (1) responde a uma necessidade real do case, (2) é compatível com granularidade e temporalidade, (3) tem implementação mais simples que as alternativas, (4) pode ser testada sem dados sensíveis em CI, e (5) preserva atribuição, licença e confidencialidade.

| Referência consultada | Evidência examinada | Uso no case | Estado |
|---|---|---|---|
| [AnaliseSobrevivencia](https://github.com/renatomenendes/AnaliseSobrevivencia) | [README](https://github.com/renatomenendes/AnaliseSobrevivencia/blob/main/README.md), [notebook `customer_churn.ipynb`](https://github.com/renatomenendes/AnaliseSobrevivencia/blob/main/customer_churn.ipynb) | Kaplan–Meier, Cox, distinção evento/censura, verificação de riscos proporcionais | **Condicionado à existência de duração e desfecho datado** |
| [framework_pinhao](https://github.com/renatomenendes/framework_pinhao) | [README](https://github.com/renatomenendes/framework_pinhao/blob/main/README.md), [checklist](https://github.com/renatomenendes/framework_pinhao/blob/main/checklist.md) | Contrato de entrada, métrica/cálculo documentados, homologação, rastreabilidade e apresentação orientada a perguntas executivas | **Adotar princípios na documentação e revisão** |
| [Analytics-Engineering-Blueprint](https://github.com/renatomenendes/Analytics-Engineering-Blueprint) | [README](https://github.com/renatomenendes/Analytics-Engineering-Blueprint/blob/main/README.md), [contratos de DataFrame](https://github.com/renatomenendes/Analytics-Engineering-Blueprint/blob/main/docs/technical/dataframe-contracts.md), [contrato de execução](https://github.com/renatomenendes/Analytics-Engineering-Blueprint/blob/main/docs/technical/execution-contract.md) | Verificação de grain, contratos m:1 para joins, não deduplicar silenciosamente, dry-run sintético determinístico, falhar antes de persistir | **Adotar padrões em `src/` e `tests/` quando implementados** |
| [pbi-profiling](https://github.com/renatomenendes/pbi-profiling) | [Metodologia](https://github.com/renatomenendes/pbi-profiling/blob/main/docs/METHODOLOGY.md), [arquitetura](https://github.com/renatomenendes/pbi-profiling/blob/main/docs/ARCHITECTURE.md) | Rotular afirmações como fato extraído, inferência analítica ou definição declarada pelo negócio; ligar indicadores à fonte e à regra | **Adotar como padrão de evidências** |
| [Pricing-B2B-MLStudio](https://github.com/renatomenendes/Pricing-B2B-MLStudio) | [README](https://github.com/renatomenendes/Pricing-B2B-MLStudio/blob/main/README.md) | Separação de `config`, `io`, etapas de pipeline e documentação técnica | **Referência arquitetural; não transpor configuração/código** |

## Consequências metodológicas

### Análise de sobrevivência: decisão condicional

O notebook de referência usa `lifelines.KaplanMeierFitter`, `lifelines.CoxPHFitter` e a variável `tenure` em um conjunto externo de churn de telecomunicações. No case atual, a documentação conhecida distingue M0 (início) de M30 (final) e fornece data de entrada no funil, **sem comprovação de data individual do evento final ou duração observável**.

- A classificação `LEAD EM ABERTO` **não é automaticamente censura à direita**. Censura exige conhecer o tempo acompanhado sem evento, sua definição e hipóteses de observação apropriadas.
- **Tempo até cancelamento do relacionamento** e **tempo até resolução do lead** são estimandos distintos: não misturar.
- Para considerar Kaplan–Meier/Cox, demonstrar identificador único do episódio, origem do tempo, datas do evento/corte, censura, maturidade de acompanhamento e risco de truncamento à esquerda.
- Havendo eventos concorrentes (ex.: diferentes tipos de saída/movimentação), avaliar formulação apropriada antes de usar a sobrevida convencional.
- Reportar *hazard ratio* como razão de riscos instantâneos condicionais, não como razão direta de probabilidades de cancelamento. Validar riscos proporcionais antes de interpretar Cox.
- Não extrapolar resultados do notebook externo à amostra do case.

**Decisão atual:** não instalar `lifelines` nem implementar curvas de sobrevivência até os requisitos acima serem verificados. O objetivo principal continua sendo perfil descritivo de retidos com movimentação.

### Framework Pinhão: operacionalizar governança

- Adotar contrato de atributos (nome, origem, tipo, regra, unidade, tempo de disponibilidade e usos permitidos) no dicionário.
- Para cada KPI e gráfico, documentar denominador, filtro, janela temporal, cálculo, resultado esperado e evidência de validação.
- Distinguir etapa de desenvolvimento, revisão/homologação e entrega executiva.
- Construir wireframe e guia visual somente quando os KPIs forem validados; não introduzir BI, dashboards ou infraestrutura que não atendam ao objetivo do case.
- O checklist do repositório de referência descreve procedimentos daquele projeto; suas caixas marcadas **não** comprovam conclusão de tarefas neste case.

### Engenharia de Analytics: contratos antes dos resultados

- Declarar grain e unicidade por etapa. Impedir multiplicação silenciosa em joins e preservar contagens quando o contrato exigir.
- Evitar `drop_duplicates()` sem justificativa explícita, em especial nos registros repetidos de `id_cliente`.
- Separar funções reutilizáveis em `src/` e testes de dados sintéticos em `tests/`; notebooks ficam com investigação e comunicação.
- Exigir falha explícita em violações bloqueantes e não persistir saídas não validadas.
- Usar data de execução como parâmetro, não relógio implícito, para repetibilidade.

### Disciplina das evidências

Todas as afirmações que se tornarem resultados executivos devem indicar classe e lastro:
1. **Fato observado:** resultado efetivamente computado na fonte do case, com população e regra reproduzíveis.
2. **Inferência analítica:** estimativa ou interpretação condicionada a modelo e premissas.
3. **Definição declarada de negócio:** conceito autorizado por responsável e data.
4. **Hipótese/recomendação:** proposta a testar, nunca implicando causalidade observacional.

O `pbi-profiling` fornece o princípio de separação entre fatos, inferências e contexto declarado; a quarta classe é adaptação deste projeto.

## Limites de reutilização e licenciamento

- `AnaliseSobrevivencia`, `framework_pinhao` e `Analytics-Engineering-Blueprint` não apresentaram arquivo `LICENSE` na árvore examinada; **não inferir permissão para copiar código ou conteúdo**.
- `pbi-profiling` informa licença MIT, mas seus scripts e dependências não são necessários aqui. Reutilizar ideias e citar fonte.
- O README de `Pricing-B2B-MLStudio` traz aviso de direitos reservados; não copiar código, dados, configurações, nomes internos ou exemplos operacionais.
- Em uma versão pública de portfólio, referências a repositórios privados e qualquer material de negócio devem passar por revisão de divulgação.
- **Nenhum código, documento, dado ou imagem de outros repositórios foi transferido ao case nesta avaliação.**

## Condições para reavaliação

1. Concluir auditoria reexecutável da planilha e confirmar a unidade de análise.
2. Obter regras oficiais para `RETIDO`, `LEAD EM ABERTO`, flags de movimentação e valores M0/M30.
3. Levantar datas de evento/censura antes de analisar sobrevivência.
4. Revisar testes, regras de divulgação e separação temporal antes de avançar para modelagem.
