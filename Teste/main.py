import pandas as pd
import glob

# Caminho onde os arquivos CSV estão localizados
caminho = 'Teste/*.csv'


# Usar glob para encontrar todos os arquivos CSV no diretório
arquivos_csv = glob.glob(caminho)

print(arquivos_csv)

# Lista para armazenar os DataFrames
dataframes = []

# Ler cada arquivo e adicionar à lista
for arquivo in arquivos_csv:
    df = pd.read_csv(arquivo)
    dataframes.append(df)

# Concatenar todos os DataFrames em um único DataFrame
resultado = pd.concat(dataframes, ignore_index=True)

# Salvar o resultado em um novo arquivo CSV
resultado.to_csv('resultado_concatenado.csv', index=False)