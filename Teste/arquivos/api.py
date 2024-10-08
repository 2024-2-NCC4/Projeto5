import requests
import json
import os
from datetime import datetime, timedelta

# Função para obter dados diários ajustados de ações
def obter_dados_acoes(api_key, simbolo):
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': simbolo,
        'outputsize': 'full',  # Para obter todos os dados disponíveis
        'apikey': api_key
    }

    response = requests.get(url, params=params, verify=False)
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))  # Imprimir a resposta completa para depuração
        return data.get('Time Series (Daily Adjusted)', None)  # Usando .get() para evitar KeyError
    else:
        print(f'Erro na requisição: {response.status_code}')
        return None

# Função para filtrar dados dos últimos 10 anos
def filtrar_dados_ultimos_10_anos(dados):
    data_atual = datetime.now()
    data_limite = data_atual - timedelta(days=365*10)
    
    dados_filtrados = {}
    for data, valores in dados.items():
        data_obj = datetime.strptime(data, '%Y-%m-%d')
        if data_obj >= data_limite:
            dados_filtrados[data] = valores
            
    return dados_filtrados

# Salvar os dados em um arquivo JSON
def salvar_dados_json(dados, caminho):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    
    with open(caminho, 'w') as json_file:
        json.dump(dados, json_file, indent=4)

# Chave da API (substitua pela sua)
api_key = 'HIVGUYJE4ET71KD8'

# Solicitar o símbolo da ação
simbolo = input("Digite o símbolo da ação que você deseja consultar (ex: MSFT): ")

# Obter e filtrar os dados
dados = obter_dados_acoes(api_key, simbolo)
if dados:
    dados_filtrados = filtrar_dados_ultimos_10_anos(dados)

    # Caminho para salvar o arquivo JSON
    caminho_arquivo = f'C:/Users/23024522/Desktop/teste/{simbolo}_dados_10_anos.json'  # Substitua pelo caminho desejado
    salvar_dados_json(dados_filtrados, caminho_arquivo)

    print(f'Dados salvos em {caminho_arquivo}')
else:
    print("Não foram encontrados dados para salvar.")
