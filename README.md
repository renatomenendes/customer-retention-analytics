# Customer Retention Analytics

**Status:** fundamentação inicial; regras de negócio pendentes de validação.  
**Janela-alvo:** leads com entrada entre 2025-06-01 e 2025-12-31, inclusive.  
**Repositório:** `renatomenendes/customer-retention-analytics` (privado; acesso confirmado em 2026-10-14).

## Propósito

Identificar e caracterizar perfis associados à classificação de clientes como retidos e à movimentação de produtos durante o processo de retenção. Examinar, separadamente, a variação de valores monetários entre as posições M0 e M30, sem atribuir causalidade às ofertas.

## Fontes e acesso

- Documento de especificação e planilha originais fornecidos pelo responsável, armazenados apenas no ambiente autorizado.
- Planilha: aba `bd_case_final_1`, conforme documentação recebida; conferir fisicamente na auditoria reproduzível.
- Auditorias preexistentes: relatório e arquivos estruturados locais; **não são evidência revalidada nesta entrega**.
- Dados **não** fazem parte deste repositório. O processamento local só deve utilizar arquivos autorizados. Não carregar dados de clientes para GitHub, CI ou serviços externos.

## Estrutura atual

```text
.
├── .gitignore
├── README.md
├── data/
│   └── README.md
└── docs/
    ├── project_charter.md
    ├── methodology.md
    ├── data_dictionary.md
    ├── data_audit_protocol.md
    ├── decision_log.md
    └── limitations.md
```

Notebooks, módulos, testes, apresentação e automações serão adicionados **quando houver implementação substantiva e requisitos confirmados**. Não há notebooks vazios nem CI decorativa.

## Como reproduzir a próxima etapa

1. Validar as decisões pendentes em `docs/decision_log.md`.
2. Colocar a planilha original em `data/raw/retention_case.xlsx` no ambiente local autorizado, fora do Git (ou configurar outro caminho local).
3. Registrar e conferir o fingerprint em manifesto **local não versionado**.
4. Implementar e executar a auditoria em notebook, com verificações automatizadas em `src/` e `tests/`.
5. Versionar **apenas código e documentação revisados**, por branch e pull request; conferir o diff antes da integração.

Ainda não há ambiente Python fixado nem comandos de execução do notebook: documentá-los sem implementação seria enganoso.

## Proteção de informação

Arquivos tabulares, caches, saídas, registros detalhados, checkpoints, credenciais e segredos estão ignorados por padrão. Revisar `git status` e `git diff --cached` antes de cada commit; a existência de `.gitignore` não substitui revisão.

## Critérios de aceite

Consultar `docs/methodology.md` e `docs/data_audit_protocol.md`. Nenhum resultado financeiro ou preditivo deve ser publicado antes da validação da granularidade, da semântica das flags e da unidade do valor monetário.
## Governança do GitHub

- Branch padrão: `main`; desenvolver alterações em branches e revisar via pull request.
- A licença `LICENSE` existente (Unlicense) é preservada, sem inferir que dados, documentação confidencial ou resultados possam ser divulgados. Seu enquadramento deve ser revisado antes de eventual publicação pública.
- A autorização para manutenção do repositório **não autoriza** enviar dados de clientes, alterar visibilidade nem tornar resultados confidenciais públicos.
- Não há workflows de CI, notebooks executados ou resultados de modelo nesta entrega.
