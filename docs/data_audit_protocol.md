# Auditoria e consistência da base

## Escopo e granularidade

A unidade é a linha da planilha de atendimentos, com entrada entre junho e dezembro de 2025. Um mesmo `id_cliente` pode aparecer em mais de um registro. O campo `DATA_FUNIL_SOLAR` delimita o período, sem substituir a data de encerramento do atendimento.

O processamento completo considera **303.652 registros no recorte**. O conjunto de estados operacionais inclui `RETIDO`, `NAO RETIDO` e `LEAD EM ABERTO`.

## Verificações de qualidade e interpretação

| Dimensão | Verificação | Consequência analítica |
|---|---|---|
| Janela temporal | Datas válidas e registros fora do período | Denominador condicionado à entrada entre junho e dezembro |
| Identificadores | Valores ausentes, IDs repetidos e sobreposição entre partições | Não tratar linhas como clientes únicos; separar clientes entre treino e teste |
| Estado do funil | Contagens por status e por origem/mês | Casos em aberto permanecem categoria própria |
| Produtos M0/M30 | Presença e códigos de cada família | Identificar inclusão, retirada, troca e ausência |
| Flags | `FLAG_MOV_*` e `FLAG_CANC_*` cruzadas com as transições | Eventos distintos; discrepâncias são quantificadas |
| MPlay | Marcado, não marcado e vazio | Vazio significa **não elegível** à unificação, conforme a definição do campo |
| Valores | Nulos, zeros, diferenças e sinais por família | Comparações monetárias apenas com pares válidos |
| Modelagem | Preditores em M0, status final e campos M30 separados | Evitar informação posterior ao desfecho nas variáveis do modelo |
| Generalização | Mês, origem, composição de carteira e clientes repetidos | Explicitar o alcance do teste temporal |

## Rastreabilidade

As regras estão implementadas em `src/retention_analytics/audit.py`, `profiles.py`, `study_profiles.py` e `extended_eda.py`. Resultados sintéticos e métricas agregadas são apresentados em `reports/`; os testes unitários encontram-se em `tests/`.

As contagens descritivas não resolvem, isoladamente, a ausência de uma chave formal do episódio, nem identificam oferta aceita, faturamento efetivo ou permanência posterior.
