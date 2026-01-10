import pandas as pd
import pyodbc

caminho_arquivo = r"C:\Users\mathe\OneDrive\Desktop\Matheus\Curso engenharia de dados\Treinamento - Exercicios\Arquivos - Atividade\produtos.csv"
df = pd.read_csv(caminho_arquivo, delimiter=',')

colunas_tratadas = {
    "produto_id" : "Produto_id",
    "nome_produto" : "Nome_produto",
    "categoria" : "Categoria",
    "preco_unitario" : "Preco_unitario",
    "ativo" : "Ativo"
}

df.rename(columns=colunas_tratadas, inplace=True)
df['Categoria'] = df['Categoria'].fillna("Categoria não informada")
df['Ativo'] = df['Ativo'].replace({
    True : "Produto ativo",
    False : "Produto inativo"
})

df['Validacao_produto'] = df['Preco_unitario'].apply(lambda preco: "Produto invalido" if preco <=0 else "Produto valido")

colunas_selecionadas = [
    "Produto_id",
    "Nome_produto",
    "Categoria",
    "Preco_unitario",
    "Validacao_produto",
    "Ativo"
]

df_produtos = df.reindex(columns=colunas_selecionadas)

#CARGA BANCO 
server = "MATHEUS"
database = "Produto_atividade"
conexao_banco = pyodbc.connect(
    "DRIVER={ODBC DRIVER 17 For SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes"
)

cursor = conexao_banco.cursor()

for _, dados_produtos in df_produtos.iterrows():
    cursor.execute("SELECT Produto_id FROM dbo.Produtos WHERE Produto_id = ? ", (int(dados_produtos['Produto_id']),))
    result_produtos = cursor.fetchone()

    if not result_produtos:
        cursor.execute(
            '''
            INSERT INTO dbo.Produtos
                (Produto_id, Nome_produto, Categoria, Preco_unitario, Validacao_produto, Ativo)
            VALUES
                (?, ?, ?, ?, ?, ?)    
            ''',
            (
                dados_produtos['Produto_id'],
                dados_produtos['Nome_produto'],
                dados_produtos['Categoria'],
                dados_produtos['Preco_unitario'],
                dados_produtos['Validacao_produto'],
                dados_produtos['Ativo']
            )
        ) 

conexao_banco.commit()
conexao_banco.close()
print("Carga realizada!")