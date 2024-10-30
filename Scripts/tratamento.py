import pandas as pd
import json
import os

def padronizar_valores(df, colunas):
    """Padronizar os valores das colunas usando Z-score."""
    for coluna in colunas:
        media = df[coluna].mean()
        desvio_padrao = df[coluna].std()
        df[f'{coluna}_Padronizado'] = df[coluna].apply(lambda x: (x - media) / desvio_padrao)

    return df

def json_para_csv(json_file, csv_file):
    try:
        with open(json_file, 'r') as file:
            dados = json.load(file)

        if not dados:
            print(f"Arquivo {json_file} está vazio. Pulando arquivo.")
            return

        df = pd.DataFrame.from_dict(dados, orient='index')
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Data'}, inplace=True)

        required_columns = ['Open', 'Close', 'High', 'Low', 'Volume']
        if not all(column in df.columns for column in required_columns):
            print(f"Arquivo {json_file} não possui as colunas necessárias. Pulando arquivo.")
            return

        df = df[['Data', 'Open', 'Close', 'High', 'Low', 'Volume']]
        df.columns = ['Data', 'Abertura', 'Fechamento', 'Maxima', 'Minima', 'Volume']
        
        # Arredondar os valores originais para 2 casas decimais
        df[['Abertura', 'Fechamento', 'Maxima', 'Minima']] = df[['Abertura', 'Fechamento', 'Maxima', 'Minima']].applymap(lambda x: round(x, 2))
        df['Ultimo'] = df['Fechamento'].apply(lambda x: round(x, 2))

        # Padronizar os valores das colunas relevantes
        colunas_para_padronizar = ['Ultimo', 'Abertura', 'Fechamento', 'Maxima', 'Minima']
        df = padronizar_valores(df, colunas_para_padronizar)

        df['Volume'] = df['Volume'].astype(int)
        df['Data'] = pd.to_datetime(df['Data'].str[:-6]).dt.strftime('%d.%m.%Y')

        df.to_csv(csv_file, index=False)

    except Exception as e:
        print(f"Erro ao processar o arquivo {json_file}: {e}")

def converter_todos_json_para_csv():
    input_dir = 'Dados/Brutos'
    output_dir = 'Dados/Limpos'

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                json_file = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                csv_file = os.path.join(output_subdir, f"{os.path.splitext(file)[0]}.csv")

                print(f"Convertendo {json_file} para {csv_file}")
                json_para_csv(json_file, csv_file)

# Executar a função para converter todos os arquivos
converter_todos_json_para_csv()
