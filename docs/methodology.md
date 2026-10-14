# Protocolo metodológico — versão inicial

## Estado das definições

**Nenhuma regra abaixo é uma definição oficial de negócio.** São hipóteses de trabalho para validação antes do cálculo de KPIs finais.

### 1. Retenção

- **Unidade candidata:** episódio/lead que entra no funil, não `id_cliente` isoladamente; a chave real do episódio ainda não foi fornecida.
- **Desfecho operacional provisório:** `NM_SUB_INDICADOR_NEGOCIO == "RETIDO"`; `"NAO RETIDO"` é outra categoria; `"LEAD EM ABERTO"` é resultado não concluído, não imputável como perda.
- **Evento de relacionamento:** não há informação independente de atividade pós-processo; status do processo **não prova permanência futura**.
- **Janela:** entrada entre junho e dezembro de 2025; observar eventual maturidade incompleta de leads que entraram perto de 31/12.
- **Novos, reativados e inativos:** não identificáveis com segurança pelo dicionário disponível; não inventar regras de cohort de clientes ativos.
- **Clientes com múltiplos leads:** manter episódios como observações distintas somente quando chave/processo forem reconciliados; agrupar inferência/validação por cliente.

### 2. Movimentação de produtos

- **Hipótese provisória:** para BL/TV/FONE/MV, as respectivas `FLAG_MOV_* == 1` indicam alguma movimentação conforme regras operacionais; o significado preciso deve ser validado.
- **Movimentação composta (provisória):** pelo menos uma flag de movimentação igual a 1 no episódio. Não inferir que o cliente aceitou uma oferta.
- **Cancelamento de produto:** `FLAG_CANC_* == 1`; não equivale, automaticamente, a `NAO RETIDO`.
- **Inclusão, retirada e alteração de mix:** examinar comparações de IDs M0/M30 com regras para nulos e códigos de pacote; não inferir volume, quantidade ou compra recorrente se a base não possui tais campos.
- **Mudança de valor com o mesmo produto:** reportar separadamente como variação monetária observada, não como movimentação contratual.

### 3. Preservação de receita

- **Medida observada:** `VALOR_{BL,TV,FONE,MV}_{M0,M30}`; moeda, incidência (mensal, pontual) e eventual composição de descontos pendentes.
- **Proxy, sujeita a validação:** `soma_valores_M30 - soma_valores_M0` por episódio e família; reportar como **variação observada de valor informado**, não como receita incremental causada pela retenção.
- **Preço/volume/mix:** somente decompor com informações comparáveis; a base não garante preços unitários, volume, histórico de pagamentos, devoluções, sazonalidade ou custos.
- **Base de referência:** M0 do mesmo episódio, desde que os valores estejam na mesma unidade e competência que M30.
- **Análise:** descritiva, eventualmente preditiva; nunca causal sem intervenção ou identificação válida.

## Desenho analítico e salvaguardas

1. Registrar fontes, versões, população inicial e motivo de toda exclusão.
2. Auditar unicidade real da chave, reapresentações de leads, situações abertas, janela, tipos, nulos estruturais, flags contraditórias e receitas negativas.
3. Reconciliar eventos de produto M0→M30 com flags; registrar divergências por família e origem.
4. Separar indicadores distintos: retenção entre leads resolvidos, movimentação entre retidos e variação de valor entre episódios válidos; sempre indicar denominador.
5. Iniciar perfilamento descritivo por variáveis **de entrada**, com tamanho de grupo e incerteza; avaliar seleção e confusão entre origens/regiões/mix.
6. Somente se definido horizonte/uso operacional: comparar taxa-base, regressão logística e modelo baseado em árvores; split out-of-time e ausência de clientes comuns entre treino/teste, com período final preservado para teste quando viável.
7. Não exigir clustering se regras/árvores proporcionarem perfis mais interpretáveis. Se houver clustering: avaliar escalas, estabilidade e utilidade de segmentos.
8. Priorizar recomendações com elegibilidade, população, evidência, KPI de acompanhamento e plano de experimento A/B ou avaliação prospectiva.

## Critérios mínimos de aceitação

- Sem definição de episódio e corte M0/M30: **bloquear modelagem preditiva**.
- Sem definição do significado de `VALOR`: **bloquear alegações de preservação financeira**.
- Sem plano de amostragem: não generalizar métricas pontuais para a base corporativa.
- Sem dados de resultado da oferta por tratamento: não reportar uplift causal.
