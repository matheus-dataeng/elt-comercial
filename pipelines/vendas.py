import pandas as pd 
import pyodbc

caminho_arquivo = r"C:\Users\mathe\OneDrive\Desktop\Matheus\Curso engenharia de dados\Treinamento - Exercicios\Arquivos - Atividade\vendas.csv"
df = pd.read_csv(caminho_arquivo, delimiter=',')

colunas_tratadas = {
    "venda_id" : "Venda_id",
    "cliente_id" : "Cliente_id",
    "produto_id" : "Produto_id",
    "quantidade" : "Quantidade",
    "data_venda" : "Data_venda",
    "canal" : "Canal"
}

df.rename(columns=colunas_tratadas, inplace=True)
df['Validacao_venda'] = df['Quantidade'].apply(lambda quantidade: "Venda invalida" if quantidade <=0 else "Venda valida")
df['Canal'] = df['Canal'].str.title()
df['Tipo_venda'] = df['Canal'].apply(lambda canal: "Fisica" if canal == "Loja" else "Online")

colunas_selecionadas = [
    "Venda_id",
    "Cliente_id",
    "Produto_id",
    "Quantidade",
    "Validacao_venda",
    "Canal",
    "Tipo_venda",
    "Data_venda"

]

df_vendas = df.reindex(columns=colunas_selecionadas)

server = "MATHEUS"
database = "Produto_atividade"
conexao_banco = pyodbc.connect(
    "DRIVER={ODBC DRIVER 17 For SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

cursor = conexao_banco.cursor()

for _, dados_vendas in df_vendas.iterrows():
    cursor.execute("SELECT Venda_id FROM dbo.Vendas WHERE Venda_id = ?", (int(dados_vendas['Venda_id']),))
    result_vendas = cursor.fetchone()

    if not result_vendas:
        cursor.execute(
            '''
            INSERT INTO dbo.Vendas 
                (Venda_id, Cliente_id, Produto_id, Quantidade, Validacao_venda, Canal, Tipo_venda, Data_venda)
            VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?)    
            ''',
            (
                dados_vendas['Venda_id'],
                dados_vendas['Cliente_id'],
                dados_vendas['Produto_id'],
                dados_vendas['Quantidade'],
                dados_vendas['Validacao_venda'],
                dados_vendas['Canal'],
                dados_vendas['Tipo_venda'],
                dados_vendas['Data_venda']
            )
        )

conexao_banco.commit()
cursor.close()
conexao_banco.close()
print("Carga realizada!")

