import yfinance as yf
import json
import os

# Função para baixar dados de um símbolo específico e salvar como JSON com o nome da empresa
def download_stock_data(symbol, branch_folder):
    # Datas hard coded: de 01/01/2014 até 01/10/2024
    start_date = "2014-01-01"
    end_date = "2024-10-01"

    # Baixando os dados históricos e informações da empresa
    stock_data = yf.Ticker(symbol)
    history = stock_data.history(start=start_date, end=end_date)
    
    # Obtendo o nome da empresa a partir do símbolo
    company_name = stock_data.info.get('shortName', symbol)  # Usa o símbolo como fallback se o nome não estiver disponível
    
    # Convertendo o DataFrame para um dicionário
    data_dict = history.to_dict(orient='index')

    # Convertendo as datas para strings
    data_dict = {str(date): value for date, value in data_dict.items()}

    # Verificando se o diretório do ramo existe, senão, cria o diretório
    if not os.path.exists(branch_folder):
        os.makedirs(branch_folder)

    # Criando um nome de arquivo simples com o nome da empresa
    file_name = f"{company_name}.json".replace(" ", "_")  # Substitui espaços no nome da empresa por "_"
    file_path = os.path.join(branch_folder, file_name)

    # Salvando como JSON na pasta do ramo
    with open(file_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)   

    print(f"Dados do símbolo '{symbol}' foram salvos como '{file_name}' em '{branch_folder}'")

# Função para ler o arquivo de símbolos e baixar os dados para cada um em sua pasta correspondente
def download_from_file():
    file_path = "C://Projetos/Projeto5/lista2.txt"  # Caminho hardcoded do arquivo .txt
    
    try:
        # Abrindo o arquivo .txt e lendo os símbolos
        with open(file_path, 'r') as file:
            lines = file.readlines()

        current_branch = None  # Inicialmente, não temos um ramo de atuação definido

        # Processando cada linha do arquivo
        for line in lines:
            line = line.strip()  # Remove espaços e quebras de linha
            if not line:
                continue  # Ignora linhas vazias

            # Verifica se a linha começa com "ramo", identificando um ramo de atuação
            if line.lower().startswith("ramo"):
                # Remove o prefixo "ramo" e os espaços em branco, mantendo apenas o nome relevante do ramo
                current_branch = line.replace("ramo", "").strip()
                print(f"\nRamo de atuação: {current_branch}")
                continue

            # Se a linha não for o ramo, tratamos como símbolo da empresa
            if current_branch:  # Certifica-se de que temos um ramo definido
                branch_folder = os.path.join("Dados/Brutos", current_branch)
                print(f"Baixando dados para símbolo: {line} no ramo: {current_branch}")
                download_stock_data(line, branch_folder)

    except FileNotFoundError:
        print(f"O arquivo {file_path} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Exemplo de uso
if __name__ == "__main__":
    download_from_file()