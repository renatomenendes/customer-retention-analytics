# Limitações, vieses e riscos

| Código | Risco | Efeito potencial | Controle recomendado |
|---|---|---|---|
| R-01 | `id_cliente` não identifica episódio único | Duplicidade indevida; denominadores errados | Obter chave do lead e reconciliar múltiplas entradas |
| R-02 | Status de processo confundido com retenção sustentada | KPI inflado e inferência inadequada | Separar retenção do lead da permanência futura |
| R-03 | Leads em aberto e maturidade incompleta | Viés por mês/origem | Tratar pendência separadamente; análises de sensibilidade |
| R-04 | M0/M30 sem timestamps independentes | Horizonte não definido | Não rotular automaticamente como retenção em 30 dias |
| R-05 | Flags não validadas e divergências com produto | Alvo mal definido | Reconciliação M0/M30 por família |
| R-06 | Valor monetário sem unidade validada | Alegações financeiras não sustentadas | Rotular como variação de valor observado |
| R-07 | Amostra sem plano de extração | Generalização indevida | Apresentar apenas estatísticas amostrais |
| R-08 | Uso de variáveis pós-desfecho | Leakage e métricas artificiais | Contrato temporal de features e validação out-of-time |
| R-09 | Mesmo cliente em treino e teste | Otimismo artificial de generalização | Segregação por cliente e revisão da cobertura temporal |
| R-10 | Associação confundida com causalidade | Ações ineficazes ou danosas | Recomendar testes prospectivos; medir resultado incremental |
| R-11 | Dados comerciais/identificadores vazados | Risco legal e reputacional | Não versionar dados; revisão antes de cada push |
| R-12 | Classes e segmentos pequenos | Instabilidade e reidentificação | Limiar de supressão a estabelecer com governança |

**Aviso:** este documento descreve riscos e observações de estrutura, não certifica que a base tenha passado em testes nem que exista impacto financeiro mensurado.
