import pandas as pd
import json
import os

def formatar_valores(valor, ultima_grandeza):
    """Formatar o valor com base na última grandeza e retornar o valor formatado e o coeficiente."""
    nova_grandeza = None

    if valor < 10:  # Menos que 10
        nova_grandeza = 'menor_10'
        coeficiente = 0.1
        valor_formatado = round(valor * 10, 2)
    elif valor < 100:  # De 10 a 99
        nova_grandeza = 'menor_100'
        coeficiente = 1
        valor_formatado = round(valor, 2)
    elif valor < 1000:  # De 100 a 999
        nova_grandeza = 'menor_1000'
        coeficiente = 1  # Mantém o coeficiente como 1
        valor_formatado = round(valor, 2)  # Não divide por 10
    elif valor < 10000:  # De 1000 a 9999
        nova_grandeza = 'menor_10000'
        coeficiente = 100
        valor_formatado = round(valor / 100, 2)
    else:  # 10000 ou mais
        nova_grandeza = 'maior_10000'
        coeficiente = 1000
        valor_formatado = round(valor / 1000, 2)

    # Se o valor atual transita para uma nova grandeza, mantenha o coeficiente anterior
    if ultima_grandeza is not None and ultima_grandeza != nova_grandeza:
        coeficiente = 1  # Manter coeficiente como 1 se transitar

    return valor_formatado, coeficiente, nova_grandeza

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

        # Adicionando as colunas formatadas e coeficientes
        ultima_grandeza = None
        for coluna in ['Ultimo', 'Abertura', 'Fechamento', 'Maxima', 'Minima']:
            valores_formatados = []
            coeficientes = []
            for valor in df[coluna]:
                valor_formatado, coeficiente, ultima_grandeza = formatar_valores(valor, ultima_grandeza)
                valores_formatados.append(valor_formatado)
                coeficientes.append(coeficiente)

            df[f'{coluna}_Formatado'] = valores_formatados
            df[f'{coluna}_Coeficiente'] = coeficientes

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
