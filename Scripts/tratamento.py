import pandas as pd
import json

def json_para_csv():
    # Caminho do arquivo JSON
    json_file = 'Dados/Brutos/Aviacao/AIR_CANADA.json'  # Substitua pelo caminho do seu arquivo
    # Caminho do arquivo CSV de saída
    csv_file = 'Dados/Limpos/AIR_CANADA.csv'  # Substitua pelo caminho desejado para o CSV

    # Carregar o arquivo JSON
    with open(json_file, 'r') as file:
        dados = json.load(file)
    
    # Converter o JSON em um DataFrame
    df = pd.DataFrame.from_dict(dados, orient='index')

    # Resetar o índice para ter uma coluna com as datas
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Data'}, inplace=True)

    # Reorganizar as colunas no formato desejado
    df = df[['Data', 'Open', 'Close', 'High', 'Low', 'Volume']]
    df.columns = ['Data', 'Abertura', 'Fechamento', 'Maxima', 'Minima', 'Volume']

    # Adicionar a coluna 'Ultimo' como o fechamento mais recente
    df['Ultimo'] = df['Fechamento']

    # Reorganizar as colunas
    df = df[['Data', 'Ultimo', 'Abertura', 'Fechamento', 'Maxima', 'Minima', 'Volume']]

    # Arredondar os valores numéricos para a segunda casa decimal
    df[['Abertura', 'Fechamento', 'Maxima', 'Minima', 'Ultimo']] = df[['Abertura', 'Fechamento', 'Maxima', 'Minima', 'Ultimo']].round(2)
    df['Volume'] = df['Volume'].astype(int)  # Garantir que o volume seja inteiro

    # Remover a parte do fuso horário e mudar a formatação das datas
    df['Data'] = pd.to_datetime(df['Data'].str[:-6]).dt.strftime('%d.%m.%Y')

    # Salvar o DataFrame em um arquivo CSV
    df.to_csv(csv_file, index=False)

# Executar a função
json_para_csv()
