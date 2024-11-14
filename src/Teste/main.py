import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import pandas as pd
import plotly.express as px

# URL base e parâmetros
url_base = 'http://localhost:3000/query2'
data_inicio = '01.01.2014'
data_final = '31.12.2023'

empresas = [
    {'Simbolo': 'Airbus', 'Ramo': 'Aviacao'},
    {'Simbolo': 'Air Canada', 'Ramo': 'Aviacao'},
    {'Simbolo': 'Air China', 'Ramo': 'Aviacao'},
    {'Simbolo': 'Apple', 'Ramo': 'Tecnologia'},
    {'Simbolo': 'Amazon', 'Ramo': 'Tecnologia'},
]

# Requisição para cada empresa e armazenamento dos dados em um DataFrame
dados_empresas = []

for empresa in empresas:
    ramo = empresa['Ramo']
    simbolo = empresa['Simbolo']
    
    # Realiza a requisição enviando os parâmetros corretamente
    response = requests.get(url_base, params={
        'ramo': ramo,
        'simbolos': simbolo,
        'data_inicio': data_inicio,
        'data_final': data_final
    })
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        dados = response.json()
        
        # Verifica se há dados retornados
        if dados:
            df = pd.DataFrame(dados)
            df['Simbolo'] = simbolo  # Adiciona a coluna 'Simbolo' para identificação
            df['Data'] = pd.to_datetime(df['Data'], format='%d.%m.%Y')  # Converte a coluna Data para o formato de data
            dados_empresas.append(df)
        else:
            print(f"Atenção: Nenhum dado encontrado para a empresa {simbolo}.")
    else:
        print(f"Erro na requisição para {simbolo}: {response.status_code}")

# Concatena todos os DataFrames em um só, caso haja dados
if dados_empresas:
    df_total = pd.concat(dados_empresas, ignore_index=True)
else:
    df_total = pd.DataFrame()  # DataFrame vazio para evitar erros

# Cria o aplicativo Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Gráficos de Fechamento das Empresas"),
    dcc.Dropdown(
        id='empresa-dropdown',
        options=[{'label': empresa['Simbolo'], 'value': empresa['Simbolo']} for empresa in empresas],
        value=empresas[0]['Simbolo']
    ),
    dcc.Graph(id='fechamento-grafico')
])

@app.callback(
    Output('fechamento-grafico', 'figure'),
    [Input('empresa-dropdown', 'value')]
)
def atualizar_grafico(simbolo):
    # Verifica se o DataFrame total não está vazio e contém o símbolo selecionado
    if not df_total.empty and simbolo in df_total['Simbolo'].values:
        df_empresa = df_total[df_total['Simbolo'] == simbolo]

        # Agregação opcional por mês para suavizar o gráfico (média mensal)
        df_empresa = df_empresa.set_index('Data').resample('M').mean().reset_index()
        
        fig = px.line(df_empresa, x='Data', y='Fechamento', title=f"Fechamento da Empresa: {simbolo}")
        fig.update_layout(
            xaxis_title="Data",
            yaxis_title="Fechamento",
            xaxis=dict(tickformat="%Y-%m")  # Formato de data simplificado
        )
    else:
        # Gráfico vazio com mensagem caso não haja dados
        fig = px.line(title=f"Sem dados disponíveis para a empresa: {simbolo}")
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
