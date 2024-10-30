import pandas as pd

def csv_to_sql(csv_file, sql_file, table_name):
    # Lê o arquivo CSV, mantendo os índices
    df = pd.read_csv(csv_file, index_col=0)

    # Abre o arquivo SQL para escrita
    with open(sql_file, 'w') as sqlfile:
        # Escreve a instrução para criar a tabela
        columns = df.columns
        sqlfile.write(f"CREATE TABLE {table_name} (\n")
        
        # Adiciona a coluna do índice
        sqlfile.write(f"    index_column INT PRIMARY KEY,\n")

        # Adiciona as colunas com os tipos
        for col in columns:
            sqlfile.write(f"    {col} TEXT,\n")
        sqlfile.write(");\n\n")

        # Escreve os comandos INSERT para cada linha
        for index, row in df.iterrows():
            values = [f"'{str(index)}'"] + [f"'{str(value)}'" for value in row]
            sqlfile.write(f"INSERT INTO {table_name} VALUES ({', '.join(vmysalues)});\n")

    print(f"Arquivo SQL '{sql_file}' gerado com sucesso com os dados de '{csv_file}'.")

# Exemplo de uso:
csv_to_sql('Dados\concatenado.csv', 'dados.sql', 'tabela_projeto')
