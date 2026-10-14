# Política de dados

Esta pasta contém apenas esta orientação versionável. O arquivo-fonte `.xlsx`, dados derivados, amostras de clientes e identificadores individuais permanecem em `data/raw/` ou outro local aprovado **fora do versionamento**.

- **Classificação preliminar:** confidencial, até confirmação pela responsável pelos dados.
- **Origem:** planilha do case compartilhada na conversa.
- **Uso autorizado:** análise no ambiente local fornecido; acesso ao repositório para código e documentação não implica autorização para carregar a planilha no GitHub ou em CI.
- **Publicação:** somente com autorização formal e revisão de reidentificação, inclusive em agregados e grupos pequenos.
- **Dados sintéticos:** permitidos em demonstrações se identificados explicitamente como sintéticos e sem correspondência com resultados reais.
- **Reprodutibilidade:** documentar fingerprint, aba, intervalo de datas e regras de seleção da base utilizada; nunca registrar valores ou IDs de clientes em logs versionados.
