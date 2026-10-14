# Registro de decisões metodológicas

**Estado:** decisões propostas, ainda **não aprovadas**. Não converter uma hipótese em regra oficial sem a validação correspondente.

| ID | Tema | Alternativas e decisão provisória | Status |
|---|---|---|---|
| DEC-001 | Granularidade | Lead/episódio vs. cliente único. **Propor episódio**, se houver chave verificável; não fazer deduplicação por ID isolado. | **Pendente:** chave do lead |
| DEC-002 | Retenção | Status do funil vs. atividade pós-atendimento. **Usar status como proxy apenas após validação**. | **Pendente:** semântica de status |
| DEC-003 | Leads abertos | Tratar como não retidos vs. desfecho desconhecido. **Propor separar e analisar viés**. | **Pendente:** maturidade/SLA |
| DEC-004 | Movimentação | Flags operacionais vs. comparação M0/M30. **Auditar e reconciliar as duas visões**; não misturar variação de valor. | **Pendente:** regra de negócio |
| DEC-005 | Receita | Valor do plano vs. receita efetiva. **Reportar apenas diferença de valor observado**, até definição. | **Pendente:** unidade e competência |
| DEC-006 | Amostra | Amostra aleatória vs. quotas por mês/origem. **Não extrapolar** ao universo até conhecer seleção e pesos. | **Pendente:** plano amostral |
| DEC-007 | Modelagem | Perfil descritivo vs. predição em M0. **Começar pela caracterização descritiva**, avaliar predição após validação. | **Provisório** |
| DEC-008 | Validação | Split aleatório vs. temporal/cliente. **Preferir temporal com segregação por cliente**, examinar viabilidade. | **Provisório** |
| DEC-009 | GitHub | Repositório privado `renatomenendes/customer-retention-analytics` acessível em 2026-10-14. **Usar branch e PR; preservar `main`.** | **Confirmado para manutenção de código e documentação** |
| DEC-010 | Confidencialidade | Publicação de amostra/resultados vs. documentação e código apenas. **Dados brutos e resultados identificáveis excluídos do Git**, inclusive privado. | **Em vigor; requer liberação específica de dados** |

## Informações essenciais a solicitar ao responsável pelo negócio

1. Qual identificador distingue duas passagens diferentes do mesmo cliente pelo funil? Há `id_lead`, protocolo, ID de atendimento ou timestamp inequívoco?
2. Qual evento/status caracteriza retenção e por quanto tempo é acompanhado? `LEAD EM ABERTO` é pendência de processo, atraso de atualização ou outro cenário?
3. `FLAG_MOV_*` captura mudança de produto/plano, mudança de preço, oferta aceita ou outros eventos? E `FLAG_CANC_*`?
4. `VALOR_*` significa mensalidade recorrente, cobrança, receita líquida ou valor de catálogo? Inclui descontos, impostos, créditos ou bundles?
5. Como a amostra foi extraída? Há filtros, quotas, pesos ou defasagem de atualização em dezembro?
6. Há autorização da proprietária dos dados para publicar resultados agregados? Qual limiar de divulgação por grupo? A autorização para manter o repositório privado não constitui liberação de dados nem de resultados comerciais.

## Padrão de atualização

Registrar data, decisão, proprietário, evidência, alternativas, impacto técnico e possíveis reversões quando uma definição for confirmada.
## Registro de execução — 2026-10-14

- Repositório verificado pela integração GitHub: privado; branch `main`; conteúdo inicial apenas `LICENSE` (Unlicense); sem PRs abertos no momento da inspeção.
- Autorização concedida pelo responsável pelo projeto para criação de branches, commits e PRs de documentação/código relacionados ao projeto.
- Manter a base e o manifesto de fingerprints localmente; não versionar nem publicar dados brutos, IDs de clientes ou resultados identificáveis.
- Restrições de negócio DEC-001 a DEC-006 continuam pendentes de confirmação pelo detentor da definição oficial.
