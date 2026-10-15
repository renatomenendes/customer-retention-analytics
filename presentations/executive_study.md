# Roteiro de apresentação — Retenção de clientes

**Tema:** Perfis, transições contratuais e valor observado.  
**Período da amostra:** junho a dezembro de 2025.  
**Público:** banca de avaliação técnica e representantes de negócio.

Este roteiro acompanha a sequência dos slides. É um guia de fala, não um texto para ser lido literalmente. Valores e percentuais referem-se a registros do funil, não a clientes únicos.

## Apresentação principal

### Slide 01 — Retenção de clientes: perfis, transições contratuais e valor observado

O objetivo deste estudo é identificar características associadas à movimentação de produtos entre os atendimentos classificados como retidos e investigar o que acontece com a carteira e os valores registrados entre o início e o encerramento do processo. A análise cobre junho a dezembro de 2025 e considera quatro famílias de produtos.

*Transição:* A primeira distinção essencial é separar o status operacional dos resultados contratuais.

### Slide 02 — Um atendimento retido pode produzir resultados comerciais diferentes

A amostra mostra que a retenção operacional não encerra a avaliação do resultado comercial. Entre os registros retidos, cerca de um terço apresenta movimentação e aproximadamente um quinto tem cancelamento de algum produto. Essas ocorrências podem coexistir. Precisamos observar conjuntamente o desfecho do atendimento, a configuração final dos produtos e a diferença de valor registrada.

*Transição:* Comecemos pela definição dos indicadores e pela população analisada.

### Slide 03 — O estudo examina três resultados complementares

O primeiro indicador é o status RETIDO no funil; o segundo combina as flags de movimentação e cancelamento, conferidas com os códigos de produto inicial e final; o terceiro mede M30 menos M0 dos campos de valor. A pergunta central de perfil é feita entre os registros retidos, comparando aqueles que tiveram movimentação e aqueles que não tiveram. M30 é um estado final do processo, e não um horizonte de trinta dias confirmado.

*Transição:* O universo da amostra mostra por que o denominador precisa ser explícito.

### Slide 04 — Os perfis são estudados entre 249.309 registros retidos

A planilha continha 303.654 linhas, das quais duas estavam fora do intervalo analisado. Na janela, 249.309 registros apresentam status RETIDO, 48.091 NÃO RETIDO e 6.252 EM ABERTO. O estudo de perfis condiciona a análise à população RETIDO. Como há IDs de cliente repetidos e não foi fornecida uma chave oficial do episódio de atendimento, os números são expressos por registro do funil.

*Transição:* Dentro dos retidos, a distinção entre movimentação e cancelamento revela a principal descoberta.

### Slide 05 — 45.479 retidos tiveram cancelamento de pelo menos um produto

Esta é a segmentação comercial decisiva. Mais de trinta e dois mil registros foram retidos sem movimentação, mas com cancelamento de algum produto. Outros treze mil registraram movimentação junto com cancelamento. A soma mostra 45.479 retidos com retirada de pelo menos um produto. Assim, o rótulo RETIDO não garante preservação integral do portfólio. Essas quatro situações orientarão a leitura econômica seguinte.

*Transição:* A distribuição dos valores observados confirma que as situações comerciais não são equivalentes.

### Slide 06 — Cancelamentos de produto acompanham as maiores quedas de valor

O grupo sem movimentação ou cancelamento apresenta mediana zero. Quando existe apenas cancelamento, a mediana da diferença M30 menos M0 chega a menos 104,90. Quando há movimentação sem cancelamento, é menos 22,48; quando os dois eventos coexistem, menos 88,96. São valores registrados na base, não perdas de receita causadas pelo atendimento. O padrão torna o cancelamento parcial um ponto prioritário de auditoria comercial.

*Transição:* Vamos localizar essas transições nas famílias de produto.

### Slide 07 — Banda Larga concentra trocas; em Fone, remoções superam substituições

Nas transições dos registros retidos, Banda Larga, isto é, internet fixa, concentra o maior volume de substituições de código. TV também apresenta substituições e remoções expressivas. Em Fone, as remoções superam as substituições. A remoção de uma família foi registrada em FLAG_CANC, não em FLAG_MOV; por isso, olhar só movimentações ocultaria parte da contração da carteira. Uma troca de código não é necessariamente upgrade ou downgrade sem interpretação dos planos.

*Transição:* Além das famílias, vale observar quais alterações aparecem sozinhas e quais ocorrem combinadas.

### Slide 08 — Em 60% dos retidos movimentados, só a internet fixa mudou

Entre os 86.540 registros retidos que tiveram alguma movimentação, 51.962 apresentaram flag exclusivamente de internet fixa, ou cerca de sessenta por cento. Outros 13.404 combinaram Banda Larga e TV. Portanto, internet fixa é central para o volume operacional observado. Isso não autoriza concluir que suas ofertas sejam causalmente melhores; reflete também a grande presença de BL na base.

*Transição:* Precisamos, então, trocar o denominador antes de comparar comportamentos.

### Slide 09 — Carteiras maiores registram mais casos com alguma alteração

Com quatro famílias presentes, quase setenta por cento dos registros retidos tiveram pelo menos uma movimentação; com uma família, foram 27,6 por cento. Entretanto, a taxa de flags sobre o número de famílias disponíveis em M0 não segue a mesma progressão. Isso mostra que uma carteira maior cria mais oportunidades observáveis de alteração e que a taxa por registro não é comparável isoladamente entre portes de carteira.

*Transição:* O mesmo raciocínio altera o ranking das famílias.

### Slide 10 — Móvel tem maior incidência entre elegíveis, mas menor base inicial

A taxa condicionada à presença do produto muda a leitura. Entre retidos que possuíam Móvel em M0, quarenta por cento registraram movimento de Móvel, mas a base elegível é de somente 10.964 registros. Em internet fixa, a taxa é de 31 por cento em uma base muito maior, de 239.562. O desbalanceamento de exposição não se resolve comparando somente números absolutos, e as famílias não formam classes exclusivas.

*Transição:* Agora podemos comparar as composições iniciais mais relevantes.

### Slide 11 — O mix inicial diferencia as taxas de movimentação entre retidos

As combinações iniciais exibem frequências distintas de movimentação. Por exemplo, somente BL aparece com cerca de 28,9 por cento, BL com TV em 36,3, e BL com Móvel em 55,5, mas com uma base muito menor. Esses dados servem para formular hipóteses e estruturar experimentos por elegibilidade. Não mostram que acrescentar um produto aumenta causalmente a probabilidade de movimentação.

*Transição:* Outros atributos comerciais também apresentam heterogeneidade, com importantes condições de cobertura.

### Slide 12 — A situação MPlay está associada a taxas distintas de movimentação

O dicionário define MARCADO como faturas unificadas, NÃO MARCADO como elegível para unificação e vazio como NÃO ELEGÍVEL. Entre os retidos, as taxas de movimentação são 54,0% nos 10.587 marcados, 15,2% nos 6.705 não marcados e 34,4% nos 232.017 não elegíveis. Esse último grupo representa 93,1% da população retida; 93,1% é participação do grupo, não taxa de movimentação. As diferenças observadas não estabelecem efeito causal da unificação.

*Transição:* Na comparação dos canais, também é necessário separar comportamento e composição.

### Slide 13 — A diferença entre canais cai após padronizar mês e carteira

Entre os retidos, a diferença bruta de movimentação a favor de SOLAR foi de 3,41 pontos percentuais. Após padronizar pela distribuição mensal e pela quantidade de famílias iniciais, ela caiu para 2,93 pontos. O intervalo de incerteza foi calculado com reamostragem agrupada por cliente. Esse exercício qualifica a comparação, mas não estima o efeito de usar SOLAR porque a origem não foi aleatorizada e os grupos podem diferir em outros fatores.

*Transição:* Também há assimetria importante nos atendimentos ainda abertos.

### Slide 14 — Atendimentos em aberto tornam a comparação de canais sensível

A proporção de atendimentos em aberto é muito diferente: SOLAR tem noventa casos e LEGADO mais de seis mil. Em dezembro, a participação de retidos em LEGADO poderia variar de 72,8 a 84,9 por cento se todos os casos ainda abertos terminassem, respectivamente, como não retidos ou retidos. Essa faixa ilustra uma ameaça concreta à comparabilidade de desempenho dos canais. Não é uma curva de sobrevivência, porque faltam datas individuais de resolução e seguimento.

*Transição:* Para além da descrição, testamos o quanto as características iniciais diferenciam movimentação.

### Slide 15 — A modelagem distingue movimentações com discriminação moderada

Comparamos quatro referências para o alvo movimento entre registros retidos. O teste foi cronológico, reservado para novembro e dezembro, e sem IDs de cliente compartilhados com treino e validação. Gradient boosting apresentou AUC de 0,650, average precision de 0,487 e Brier de 0,2065. Há informação nas características iniciais, mas a discriminação é moderada. Como a amostra é condicionada ao desfecho RETIDO, esse classificador descreve retrospectivamente os perfis e não é um recomendador automaticamente aplicável a todos os leads na entrada.

*Transição:* O resultado agregado precisa ser confrontado com a representação de cada família.

### Slide 16 — O desempenho preditivo varia entre as famílias elegíveis

No modelo por família, a telefonia fixa e Móvel apresentam AUC pouco acima de 0,55, enquanto TV e internet fixa ficam próximas de 0,61 a 0,62. A amostra de Móvel no teste contém somente 3.560 elegíveis. Essa heterogeneidade impede extrapolar o desempenho global para qualquer produto. O Brier também varia, mas a comparação direta entre famílias é limitada porque a prevalência do evento é diferente. A análise separada preserva a base elegível de cada produto.

*Transição:* Outra pergunta era se corrigir artificialmente o desbalanceamento melhoraria as previsões.

### Slide 17 — Pesar classes piorou o erro probabilístico nos quatro produtos

Testamos ponderação balanceada no treino e avaliamos os mesmos registros de novembro e dezembro. O Brier, que mede erro de probabilidade, piorou para internet fixa, TV, Fone e Móvel. Em Fone, por exemplo, a discriminação teve pequena melhora, mas o erro probabilístico praticamente dobrou. Não há justificativa para impor ponderação uniforme como regra comercial. O balanceamento é uma escolha dependente do custo de erro, da métrica e da calibração. A regressão ponderada não passou por recalibração posterior; portanto, os resultados não descartam a possibilidade de um modelo ponderado e calibrado apresentar comportamento melhor.

*Transição:* Há ainda um resultado que a base não observa: o aceite efetivo da oferta.

### Slide 18 — Movimentação contratual não comprova aceite de oferta

O enunciado relaciona movimentação ao aceite de ofertas, mas a fonte não registra a proposta apresentada nem a decisão do cliente. Examinamos a flag de movimentação e uma proxy contratual de troca não cancelada; ambas coincidiram integralmente nesta amostra. Essa coincidência esclarece a codificação operacional, mas não acrescenta observação independente sobre aceite. Para medir eficácia da oferta será necessário instrumentar exposição, proposta, decisão, custo e resultado posterior.

*Transição:* A tradução das descobertas em decisões utiliza exatamente essas fronteiras do que foi observado.

### Slide 19 — Quatro decisões tornam a retenção mensurável além do status

Os resultados sustentam quatro frentes: segmentar testes comerciais pelo mix e pela elegibilidade real; acompanhar cancelamentos parciais e variações de valores por família; comparar canais somente com coortes e desfechos comparáveis; e registrar as intervenções para medir aceite e efeitos incrementais. Cada frente depende de um indicador verificável e de validação com a área de negócios. A leitura conjunta dos eventos permite uma gestão mais precisa do que a contagem isolada de atendimentos retidos.

*Transição:* Encerramos retomando a principal contribuição do estudo.

### Slide 20 — Retenção, carteira e valor precisam ser avaliados juntos

A principal contribuição é demonstrar que o atendimento pode ser classificado como retido e, ainda assim, apresentar cancelamento de produto, troca contratual ou redução de valor. O resultado operacional e o resultado econômico não se substituem. Ao caracterizar os perfis de movimentação e separar as transições da carteira, o estudo estabelece uma base para testar ofertas mais adequadas e monitorar a preservação de valor. Essa é a conclusão sustentada pela amostra observada.

*Transição:* A apresentação principal termina aqui. O material seguinte é apoio técnico para perguntas da banca.

## Anexo técnico — consulta sob demanda

### Slide 21 — Anexo técnico — material de consulta

Esta seção pode ser aberta conforme as perguntas do público. Reúne definições e resultados metodológicos relevantes para interpretar as análises, sem competir com a sequência central de apresentação.

### Slide 22 — O alvo do modelo é movimentação entre registros classificados RETIDO

A probabilidade condicional de movimentação entre retidos é a resposta estatística direta à caracterização solicitada. Ela difere da ocorrência conjunta de retenção e movimentação, que envolve também a etapa de conseguir reter o cliente. Como o status RETIDO é um resultado do atendimento, o modelo condicionado ao desfecho não pode ser aplicado diretamente a todos os novos leads em M0. Essa distinção estabelece limites diferentes para caracterização retrospectiva e decisão em M0.

### Slide 23 — O teste temporal mede generalização dentro da janela observada

O modelo foi ajustado com dados de junho a setembro, selecionado usando outubro e avaliado em novembro e dezembro. Para reduzir vazamento, foram excluídos das partições anteriores os registros de clientes que apareciam nos períodos seguintes. As métricas do teste não demonstram estabilidade anual nem benefício de uma intervenção. Em paralelo, a calibração foi inspecionada por faixas de probabilidade, além do Brier.

### Slide 24 — A ponderação preservou a prevalência natural no teste

Para cada família, comparou-se regressão logística treinada na distribuição natural e com ponderação por classe. O conjunto de teste permaneceu com a prevalência real. A ponderação piorou o Brier nas quatro famílias, embora mudanças em outras métricas não sejam necessariamente do mesmo sinal. O resultado não condena todos os métodos de balanceamento; mostra que a aplicação indiscriminada não foi vantajosa para probabilidades neste experimento.

### Slide 25 — Efeito causal e lucro exigem observações além da movimentação

A planilha permite observar estados e transições de produto, não a oferta apresentada e aceita, custos comerciais ou o tempo até um possível cancelamento posterior. Por isso, não identifica uplift, lucro incremental nem curvas de sobrevivência do relacionamento. O estudo pode estabelecer limiares econômicos como cenários, desde que explicitamente hipotéticos. Para a decisão real, é necessário medir tratamento, controle, resultado e contribuição financeira.

## Orientações de condução

A apresentação principal termina no slide 20. Os slides 21 a 25 constituem anexo técnico e devem ser abertos apenas quando úteis à discussão.

Os títulos expressam conclusões sustentadas pelos gráficos e números. As explicações orais desenvolvem a interpretação, sem repetir mecanicamente o texto de cada slide. Não atribuir causalidade à origem, à movimentação ou à oferta quando a fonte não registra tratamento e controle.

Na interação com a banca, utilizar os anexos para esclarecer definições, avaliação temporal, prevalência por família e limites de identificação.

**Fontes dos resultados:** relatórios e agregados em reports/, notebooks analíticos 01–08 e enunciado *Objetivo do Case.docx*.