import pandas as pd
import pyodbc
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe

server = "Matheus"
database = "Produto_atividade"
conexao_banco = pyodbc.connect(
    "DRIVER={ODBC DRIVER 17 For SQL Server};" 
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

query = '''

SELECT 
	Pro.Produto_id,
	Pro.Nome_produto,
	Pro.Categoria,
	Pro.Preco_unitario,
	Ven.Quantidade,
	Pro.Preco_unitario * Ven.Quantidade AS Valor_total,
	Ven.Tipo_venda,
	CASE
		WHEN Pro.Preco_unitario <= 0 THEN 'Venda invalida'
		WHEN Pro.Ativo = 'Produto inativo' THEN 'Venda invalida'
		WHEN Ven.Validacao_venda = 'Venda invalida' THEN 'Venda invalida'
		ELSE 'Venda valida'
		END AS Status,
	Ven.Data_venda
FROM dbo.Vendas AS Ven
LEFT JOIN dbo.Produtos AS Pro
	ON Pro.Produto_id = Ven.Produto_id 

'''


df = pd.read_sql(query, conexao_banco)
conexao_banco.close()

credencial_json = r"C:\Users\mathe\Downloads\pythonpraticas-1b22846ff6a0.json"
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(credencial_json, scope)
gc = gspread.authorize(credentials)
planilha = gc.open_by_key("1AM5kLcvHgR5J1EWbLtmkCivJDFwVPWdhNN7eItShnyE")
planilha_guia = planilha.worksheet("Relatorio_Geral")
dados = planilha_guia.get_all_values

set_with_dataframe(
    planilha_guia,
    df,
    include_index= False,
    include_column_header= True,
    resize= True
)

print("Carga realizada!")