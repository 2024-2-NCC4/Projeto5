import requests

# Defina os parâmetros da consulta
ramo = 'Futures'
simbolo = 'Cocoa_Dec_24'
data_inicio = '01.01.2024'
data_final = '31.06.2024'

# URL do endpoint
url = f'http://localhost:3000/query?ramo={ramo}&simbolo={simbolo}&data_inicio={data_inicio}&data_final={data_final}'

print(url)

# Fazer a requisição GET
response = requests.get(url)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    # Imprimir os resultados
    results = response.json()
    print("Resultados da consulta:")
    for item in results:
        print(f"Data: {item['Data']}, Fechamento: {item['Fechamento']}")
else:
    print(f"Erro ao consultar o endpoint: {response.status_code} - {response.text}")
