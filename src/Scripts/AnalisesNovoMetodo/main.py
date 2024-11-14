import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Dados simulados (substitua pelos seus dados reais)
df_resultados = pd.DataFrame({
    'Simbolo': ['NVIDIA', 'AMD', 'Victoria\'s Secret', 'Gol Linhas Aéreas',
                'Tesla', 'Petrobras', 'Nike', 'American Airlines',
                'Meta', 'Boeing', 'Microsoft', 'Apple', 'ExxonMobil',
                'Walmart', 'Coca-Cola', 'Ouro', 'Arroz', 'DHG Pharma',
                'HMM', 'China Steel'],
    'Ramo': ['Tecnologia', 'Tecnologia', 'Moda', 'Aviacao',
             'IndustriaAutomotiva', 'Petroleo', 'Moda', 'Aviacao',
             'MidiaEntretenimento', 'Aviacao', 'Tecnologia', 'Tecnologia',
             'Petroleo', 'ConsumoNaoCiclico', 'ConsumoNaoCiclico', 'Futures',
             'Futures', 'Saude', 'TransporteLogistica', 'Commodities'],
    'Correlacao': [0.634691, 0.487756, 0.449067, 0.347416,
                   0.466472, 0.301245, 0.558921, 0.532890,
                   0.512345, 0.478901, 0.456789, 0.426789,
                   0.398765, 0.365432, 0.345678, 0.006755,
                   0.021822, 0.013552, 0.003127, 0.058019],
    'Beta': [1.673684, 1.597835, 1.528704, 1.467404,
             1.463643, 1.213579, 1.208492, 1.186742,
             1.105678, 1.098765, 1.056789, 1.045678,
             0.987654, 0.876543, 0.765432, 0.005555,
             0.030391, 0.034632, 0.010314, 0.069320]
})

retornos_anormais_ramo = pd.DataFrame({
    'Ramo': ['Tecnologia', 'ConsumoNaoCiclico', 'Aviacao',
             'Petroleo', 'Moda', 'Futures'],
    'Retorno Anormal Médio': [-0.025, -0.015, -0.045, -0.035, -0.030, 0.005]
})

# Gráfico 1: Beta vs. Correlação por Empresa
fig1 = px.scatter(df_resultados, x='Beta', y='Correlacao', color='Ramo',
                  hover_data=['Simbolo'],
                  title='Beta vs. Correlação por Empresa',
                  labels={'Beta': 'Beta', 'Correlacao': 'Correlação'})

# Gráfico 2: Distribuição dos Betas por Ramo
fig2 = px.box(df_resultados, x='Ramo', y='Beta',
              title='Distribuição dos Betas por Ramo',
              labels={'Beta': 'Beta', 'Ramo': 'Ramo'})

# Gráfico 3: Retornos Anormais Médios Durante o Evento por Ramo
fig3 = px.bar(retornos_anormais_ramo, x='Ramo', y='Retorno Anormal Médio',
              title='Retornos Anormais Médios Durante o Evento por Ramo',
              labels={'Retorno Anormal Médio': 'Retorno Anormal Médio', 'Ramo': 'Ramo'})

# Aplicativo Dash
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Dashboard de Análise Financeira', style={'textAlign': 'center'}),

    html.H2('Beta vs. Correlação por Empresa'),
    dcc.Graph(id='beta-correlacao', figure=fig1),

    html.H2('Distribuição dos Betas por Ramo'),
    dcc.Graph(id='distribuicao-beta', figure=fig2),

    html.H2('Retornos Anormais Médios Durante o Evento por Ramo'),
    dcc.Graph(id='retornos-anormais', figure=fig3)
])

if __name__ == '__main__':
    app.run_server(debug=True)
