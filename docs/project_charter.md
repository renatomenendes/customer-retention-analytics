# Project charter — Estudo de retenção e movimentação

**Fonte primária:** `Objetivo do Case.docx`.  
**Situação:** fundamentação; hipóteses não aprovadas pela área de negócio.

## Problema e decisão

O material solicita analisar a amostra dos clientes que passaram pelo funil de retenção entre junho e dezembro de 2025 e identificar perfis de **clientes retidos com movimentação de produtos**, para apoiar a eficiência das ofertas e mitigar perda de receita. O estudo deve entregar notebook documentado e defesa para audiência técnica e de negócio.

## Perguntas de negócio

1. Quem integra a população elegível de leads e que proporção possui desfecho observável?
2. Como se relacionam o status de retenção e a ocorrência de movimentação por família de produto?
3. Quais atributos disponíveis em M0 caracterizam os perfis, sem vazamento de informações futuras?
4. Em que medida o valor monetário informado muda entre M0 e M30, por carteira e segmento? O que **não** pode ser interpretado como receita efetivamente preservada?
5. Quais hipóteses operacionais podem ser avaliadas prospectivamente, com controles adequados?

## Delimitação

- Janela de **entrada no funil** proposta: 2025-06-01 a 2025-12-31, inclusive; diferença entre data de entrada e momento do desfecho a confirmar.
- Famílias: Banda Larga (BL), TV, Telefone Residencial (FONE) e Telefone Móvel (MV).
- M0 = condição inicial do lead; M30 = condição final **conforme o enunciado**. Não presumir um intervalo de exatamente 30 dias.
- A amostra não é necessariamente representativa do universo de clientes.
- Não há no enunciado uma variável explícita de aceite de oferta nem dado de custo/margem.

## Não objetivos até nova autorização/definição

- Estimar efeito causal das ofertas de retenção.
- Calcular margem incremental, LTV ou ganho financeiro atribuível às ofertas sem insumos suficientes.
- Publicar dados brutos, métricas sigilosas ou resultados de grupos pequenos.
- Empregar variáveis pós-desfecho em modelos propostos para decisão inicial.

## Entregáveis por marcos

1. **Fundamentação:** escopo, definição de unidade e desfecho, auditoria comprovada, decisões e riscos.
2. **Investigação:** exploração por mês/segmento/produto e atributos reproduzíveis.
3. **Modelagem:** baseline, comparação, split temporal/grupo, métricas e limites.
4. **Inteligência de negócio:** perfis interpretáveis, evidências, propostas e testes.
5. **Portfólio:** notebook, apresentação, documentação e versão demonstrável aprovada para divulgação.

Marcos só são concluídos com evidência, validação e artefatos verificáveis.
