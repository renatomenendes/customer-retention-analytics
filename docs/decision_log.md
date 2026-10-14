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
| DEC-009 | GitHub | Repositório inexistente entre os acessíveis. **Nenhum push ou criação automatizada**. | **Aguardando criação privada e acesso** |
| DEC-010 | Confidencialidade | Publicação de amostra/resultados vs. documentação e código apenas. **Dados excluídos do Git**. | **Em vigor até autorização** |

## Informações essenciais a solicitar ao responsável pelo negócio

1. Qual identificador distingue duas passagens diferentes do mesmo cliente pelo funil? Há `id_lead`, protocolo, ID de atendimento ou timestamp inequívoco?
2. Qual evento/status caracteriza retenção e por quanto tempo é acompanhado? `LEAD EM ABERTO` é pendência de processo, atraso de atualização ou outro cenário?
3. `FLAG_MOV_*` captura mudança de produto/plano, mudança de preço, oferta aceita ou outros eventos? E `FLAG_CANC_*`?
4. `VALOR_*` significa mensalidade recorrente, cobrança, receita líquida ou valor de catálogo? Inclui descontos, impostos, créditos ou bundles?
5. Como a amostra foi extraída? Há filtros, quotas, pesos ou defasagem de atualização em dezembro?
6. O material e os resultados agregados podem ser versionados em repositório privado? Há limiar de divulgação por grupo e autorização para portfólio público?

## Padrão de atualização

Registrar data, decisão, proprietário, evidência, alternativas, impacto técnico e possíveis reversões quando uma definição for confirmada.

## Decisões científicas a partir da reexecução condicional em 2026-10-14

- **DEC-014 — Perfil central:** estimar e apresentar `P(FLAG_MOV=1 | RETIDO=1, X_M0)` para caracterizar a população solicitada pelo case. O evento composto permanece análise secundária, não substituto do perfil entre retidos.
- **DEC-015 — Aceite de oferta:** não existe campo observável da decisão de aceite. Foi testada uma proxy de troca de código/plano sem cancelamento; ela coincide exatamente com a flag ampla de movimentação no grupo retido e **não produz evidência independente**. Cenários de aceite não podem receber status de resultados observados.
- **DEC-016 — Comparação condicional:** baseline de prevalência, regressão logística regularizada, árvore curta e gradient boosting avaliados no mesmo holdout temporal. Escolha por Brier na validação; todos os modelos foram avaliados no teste para comparação de métodos.
- **DEC-017 — Receita:** o DOCX define `valor` como valor monetário pago ao cliente associado ao lead; diferenças entre M0/M30 são descritas como valores registrados, sem declarar impacto incremental sobre faturamento, margem ou efeitos de uma oferta.
- **DEC-018 — Divulgação:** síntese, tabelas de grupos grandes e notebook executado com agregados foram mantidos no repositório privado; a base, IDs de cliente e métricas por grupos pequenos permanecem fora do Git.
