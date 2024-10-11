import os
import pandas as pd

def concatenar_csv():
    # Diretório onde os CSVs limpos estão organizados por ramo de atuação
    input_dir = 'Dados/Limpos'
    
    # Lista para armazenar os DataFrames
    df_list = []

    # Percorrer todas as subpastas e arquivos no diretório de entrada
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.csv'):
                # Caminho completo do arquivo CSV
                csv_file = os.path.join(root, file)
                
                # Extrair o ramo de atuação e o símbolo da empresa
                ramo = os.path.basename(root)  # Nome da pasta é o ramo de atuação
                simbolo = os.path.splitext(file)[0]  # Nome do arquivo é o símbolo da empresa
                
                # Ler o CSV em um DataFrame
                df = pd.read_csv(csv_file)
                
                # Adicionar as colunas 'Simbolo' e 'Ramo'
                df.insert(0, 'Simbolo', simbolo)
                df.insert(1, 'Ramo', ramo)
                
                # Adicionar o DataFrame à lista
                df_list.append(df)

    # Concatenar todos os DataFrames em um só
    df_concatenado = pd.concat(df_list, ignore_index=True)
    
    # Salvar o resultado em um único CSV
    output_file = 'Dados/concatenado.csv'
    df_concatenado.to_csv(output_file, index=False)
    
    print(f"Arquivo concatenado salvo em {output_file}")

# Executar a função
concatenar_csv()
