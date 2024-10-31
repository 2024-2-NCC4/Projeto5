import pandas as pd
from tqdm import tqdm

def csv_to_sql(csv_file, sql_file, table_name):
    # Lê o arquivo CSV, incluindo todos os índices (sem definir uma coluna de índice)
    df = pd.read_csv(csv_file)

    # Abre o arquivo SQL para escrita
    with open(sql_file, 'w') as sqlfile:
        # Escreve a instrução para criar a tabela com uma coluna ID autoincrementável
        columns = df.columns
        sqlfile.write(f"CREATE TABLE {table_name} (\n")
        
        # Adiciona a coluna de ID como chave primária autoincrementável
        sqlfile.write("    id INT AUTO_INCREMENT PRIMARY KEY,\n")

        # Adiciona as colunas do CSV como tipo TEXT
        for col in columns:
            sqlfile.write(f"    {col} TEXT,\n")

        # Remove a última vírgula e fecha a definição da tabela
        sqlfile.seek(sqlfile.tell() - 2)  # Remove a última vírgula
        sqlfile.write("\n);\n\n")

        # Adiciona a barra de progresso
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Processando linhas"):
            values = [f"'{str(value)}'" for value in row]
            sqlfile.write(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});\n")

    print(f"Arquivo SQL '{sql_file}' gerado com sucesso com os dados de '{csv_file}'.")

# Exemplo de uso:
csv_to_sql('Dados/concatenado.csv', 'dados.sql', 'tabela_projeto')
