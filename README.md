ETL Comercial
Projeto de ETL que processa dados comerciais de produtos e vendas, realizando extração, transformação, carga e validação de dados para análises e relatórios.

Descrição
  - Extração de dados de arquivos CSV (Produtos e Vendas).
  - Transformação e limpeza dos dados, incluindo cálculo de valor total e padronização de campos.
  - Validação de vendas com regras de negócio:
  - Produtos com preço unitário menor ou igual a zero são considerados inválidos.
  - Produtos inativos são desconsiderados.
  - Vendas marcadas como inválidas também são desconsideradas.
  - Carga dos dados transformados em SQL Server ou Google Sheets.
  - Geração de relatórios prontos para análise.

Validação de Vendas
- O ETL aplica regras para determinar se cada venda é válida ou inválida:
- Preço unitário do produto <= 0 → Venda inválida
- Produto inativo → Venda inválida
- Vendas já marcadas como inválidas → Venda inválida
- Vendas que não se enquadram em nenhum desses critérios são consideradas válidas.
