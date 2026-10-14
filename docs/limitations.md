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

## Limites resolvidos por formulação e não por imputação

- **Aceite de ofertas:** o DOCX descreve o perfil de quem aceita ofertas, mas a planilha não registra apresentação, proposta, aceite ou recusa. A coincidência exata da flag ampla com a proxy contratual restritiva nos retidos prova que as duas não são sinais independentes; **não autoriza inferir aceite real**.
- **Predição condicionada ao status final:** a regressão/árvore/boosting de `MOV | RETIDO` descreve retrospectivamente características e não é pontuação operacional para todos os clientes em M0, porque `RETIDO` só será conhecido ao fim do atendimento.
- **Valores e produto:** o DOCX identifica `valor` como montante pago, mas a planilha não possui conciliação contábil ou custo de oferta; diferenças observadas por produto não estimam preservação de receita incremental.
- **Estabilidade/representatividade:** testes novembro–dezembro e cortes por origem validam a divisão observacional; não demonstram estabilidade em períodos futuros nem corrigem a seleção da amostra e episódios repetidos.
