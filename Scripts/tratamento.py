import pandas as pd
import json
import os

def json_para_csv(json_file, csv_file):
    try:
        # Carregar o arquivo JSON
        with open(json_file, 'r') as file:
            dados = json.load(file)
        
        # Verificar se o JSON está vazio (somente {})
        if not dados:
            print(f"Arquivo {json_file} está vazio. Pulando arquivo.")
            return

        # Converter o JSON em um DataFrame
        df = pd.DataFrame.from_dict(dados, orient='index')

        # Resetar o índice para ter uma coluna com as datas
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Data'}, inplace=True)

        # Verificar se as colunas necessárias estão presentes
        required_columns = ['Open', 'Close', 'High', 'Low', 'Volume']
        if not all(column in df.columns for column in required_columns):
            print(f"Arquivo {json_file} não possui as colunas necessárias. Pulando arquivo.")
            return

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
    
    except Exception as e:
        print(f"Erro ao processar o arquivo {json_file}: {e}")

def converter_todos_json_para_csv():
    # Diretórios de origem e destino
    input_dir = 'Dados/Brutos'  # Pasta contendo os JSON
    output_dir = 'Dados/Limpos'  # Pasta onde os CSV serão salvos

    # Percorrer todas as subpastas e arquivos no diretório de entrada
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                # Caminho completo do arquivo JSON
                json_file = os.path.join(root, file)
                
                # Caminho relativo dentro de 'Brutos'
                relative_path = os.path.relpath(root, input_dir)
                
                # Criar o caminho correspondente na pasta de saída
                output_subdir = os.path.join(output_dir, relative_path)
                os.makedirs(output_subdir, exist_ok=True)

                # Definir o nome do arquivo CSV de saída
                csv_file = os.path.join(output_subdir, f"{os.path.splitext(file)[0]}.csv")

                print(f"Convertendo {json_file} para {csv_file}")
                
                # Converter o JSON para CSV
                json_para_csv(json_file, csv_file)

# Executar a função para converter todos os arquivos
converter_todos_json_para_csv()
