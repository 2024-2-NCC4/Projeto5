import dash
from dash import dcc, html, dash_table, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

# Inicializando o aplicativo
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Carregando os dados
df_crescimento_medio_anual = pd.read_excel("src/FrontEnd/Dashboard/Dados/crescimento_medio_anual_setor.xlsx")
df_crescimento_previsoes = pd.read_excel("src/FrontEnd/Dashboard/Dados/dados_crescimento_previsoes.xlsx").rename(columns={'Unnamed: 0': 'Ano'})
df_grau_influencia = pd.read_excel("src/FrontEnd/Dashboard/Dados/grau_influencia_setores.xlsx")
df_matriz_correlacao = pd.read_excel("src/FrontEnd/Dashboard/Dados/matriz_correlacao_setores.xlsx")
df_tabela_final = pd.DataFrame({
    "Ramo": ["Tecnologia", "ServicosFinanceiros", "MercadoImobiliario", "Saude", "EquipamentosIndustriais", "MidiaEntretenimento", "Moda", "Petroleo", "Aviacao", "TransporteLogistica", "IndustriaAutomotiva", "Commodities"],
    "Correlacao": [0.566543, 0.546324, 0.541161, 0.460372, 0.453829, 0.446175, 0.423850, 0.400867, 0.368576, 0.341771, 0.339434, 0.278060],
    "Beta": [0.996325, 1.032834, 0.961106, 0.649821, 0.856384, 0.835268, 0.789291, 0.696396, 1.003910, 0.602420, 0.712615, 0.507946]
})

# Dados de fechamento
df_fechamento = pd.read_excel("src/FrontEnd/Dashboard/Dados/dados.xlsx")

# Criando gráficos com Plotly
fig_crescimento_medio_anual = px.line(df_crescimento_medio_anual, x="Ano", y="Retorno", color="Ramo", title="Crescimento Médio Anual por Setor")
fig_crescimento_medio_anual.update_yaxes(range=[-0.003, None])

fig_crescimento_previsoes = px.line(df_crescimento_previsoes, x="Ano", y=df_crescimento_previsoes.columns[1:], title="Crescimento Médio Anual por Setor com Previsões Futuras")
fig_crescimento_previsoes.add_vline(x=2023, line_width=3, line_dash="dash", line_color="red", annotation_text="Início da Previsão", annotation_position="top right")
fig_crescimento_previsoes.update_yaxes(range=[-0.003, None])

fig_grau_influencia = px.bar(df_grau_influencia, x="Setor", y="Grau_Influencia", title="Grau de Influência dos Setores")

fig_matriz_correlacao = px.imshow(df_matriz_correlacao.set_index("Ramo"), title="Matriz de Correlação entre Setores", color_continuous_scale="Viridis")

# Layout do dashboard
app.layout = dbc.Container([
    html.H1("Análise de Comportamento do Mercado", className="text-center mt-4 mb-4"),
    
    # Filtros de fechamento
    dbc.Row([
        dbc.Col([
            html.Label("Ramo"),
            dcc.Dropdown(
                id="ramo-filter",
                options=[{"label": ramo, "value": ramo} for ramo in df_fechamento["Ramo"].unique()],
                placeholder="Selecione o Ramo"
            )
        ], width=3),

        dbc.Col([
            html.Label("Nome"),
            dcc.Dropdown(
                id="nome-filter",
                placeholder="Selecione o Nome"
            )
        ], width=3),

        dbc.Col([
            html.Label("Data Inicial"),
            dcc.DatePickerSingle(
                id="start-date",
                min_date_allowed=df_fechamento["Data"].min(),
                max_date_allowed=df_fechamento["Data"].max(),
                date=df_fechamento["Data"].min()
            )
        ], width=3),

        dbc.Col([
            html.Label("Data Final"),
            dcc.DatePickerSingle(
                id="end-date",
                min_date_allowed=df_fechamento["Data"].min(),
                max_date_allowed=df_fechamento["Data"].max(),
                date=df_fechamento["Data"].max()
            )
        ], width=3)
    ], className="mb-4"),

    dbc.Row(dbc.Col(dcc.Graph(id="fechamento-graph"))),

    html.Hr(),

    # Gráficos adicionais
    dbc.Row(dbc.Col([
        dcc.Graph(figure=fig_crescimento_medio_anual),
        html.Div("O gráfico apresenta o crescimento médio anual por setor de 2014 a 2023. Cada linha representa um setor econômico, com o eixo horizontal mostrando os anos e o eixo vertical indicando o crescimento médio anual. Observa-se uma variação moderada entre os setores ao longo do tempo. ", className="mt-2 mb-4")
    ])),

    dbc.Row(dbc.Col([
        dcc.Graph(figure=fig_crescimento_previsoes),
       html.Div([
            html.P("Tendência de Crescimento Estável: Os dados previstos mostram um crescimento leve e estável, em contraste com a volatilidade observada nos dados reais."),
            html.P("Divergência no Setor de Contratos Futuros: O setor de contratos futuros exibe um crescimento muito acentuado nas previsões, o que pode indicar uma falha no modelo, pois esse setor tende a ser volátil e é improvável que mantenha um crescimento constante."),
            html.P("Crescimento Uniforme entre Setores: O modelo parece suavizar os dados, prevendo um crescimento semelhante para todos os setores. Essa expectativa de uniformidade pode ser irrealista, considerando as diferenças características entre cada setor.")
        ], className="mt-2 mb-4")
    ])),

    html.Hr(),

    dbc.Row(dbc.Col([
        dcc.Graph(figure=fig_grau_influencia),
        html.Div([
            html.P("Setores Influentes: O setor de petróleo é classificado como o mais influente, pois suas flutuações, apesar da correlação negativa, têm grande impacto em outros setores devido à sua importância econômica."),
            html.P("Setores Influenciáveis: O setor automotivo é o mais influenciável, com alta correlação positiva com outros setores, refletindo sua sensibilidade e dependência das mudanças econômicas."),
            html.P("Setores Independentes: O setor de Equipamentos Industriais demonstra relativa independência, com correlação mediana com os outros setores, indicando menor sensibilidade às flutuações dos mercados.")
        ], className="mt-2 mb-4")

    ])),

    dbc.Row(dbc.Col([
        dcc.Graph(figure=fig_matriz_correlacao),
        html.Div([
            html.P("Crescimento Econômico e Setores Correlacionados: Setores como mídia/entretenimento e mercado imobiliário tendem a crescer simultaneamente em períodos de alta econômica. Isso ocorre porque, com mais investimentos e consumo de lazer, ambos se beneficiam diretamente do aumento no poder aquisitivo e no apetite por investimentos."),
            html.P("Influência Externa no Setor de Petróleo: O petróleo, por ser uma commodity global, é fortemente afetado por fatores externos, como geopolítica e políticas de energia. Esses elementos externos o tornam menos dependente de flutuações internas, fazendo com que seu desempenho se distancie do de outros setores."),
            html.P("Sensibilidade do Setor Financeiro e Conexão da Tecnologia com o Mercado: O setor de serviços financeiros reage rapidamente às variações econômicas gerais, refletindo a saúde econômica do mercado como um todo, já que bancos e seguradoras dependem de resultados positivos em outros setores. Já a tecnologia está altamente conectada com índices de mercado e consumo de mídia, impulsionada pela sua influência nas bolsas de valores e pelo crescente uso de tecnologias para entretenimento e consumo de mídia.")
        ], className="mt-2 mb-4")
    ])),

    html.Hr(),

    dbc.Row(dbc.Col(html.H2("Tabela de Correlação e Beta por Setor", className="text-center mt-4"))),

    dbc.Row(
    dbc.Col([
        html.Div([
            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in df_tabela_final.columns],
                data=df_tabela_final.to_dict("records"),
                style_table={"width": "80%", "margin": "auto"},
                style_cell={'textAlign': 'center', 'padding': '5px'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            ),
            html.P("Correlação e Sensibilidade ao Mercado: O valor da correlação reflete o grau de relação de cada setor com os índices do mercado, enquanto o Beta indica a sensibilidade desses setores a mudanças. A maioria das correlações é positiva, mostrando que o mercado se move geralmente na mesma direção, com Betas próximos ou abaixo de 1, sugerindo uma volatilidade moderada ou abaixo da média."),
            html.P("Setor de Tecnologia: Apresenta a maior correlação e um Beta consideravelmente alto, demonstrando uma alta sensibilidade às mudanças de sentimento no mercado. Esse comportamento é explicado pela percepção do setor como motor de crescimento futuro, refletindo rapidamente otimismo ou pessimismo econômico."),
            html.P("Setor de Commodities: Possui a menor correlação e o Beta mais baixo, devido à influência predominante de fatores globais, como mercados internacionais e condições macroeconômicas. Além disso, commodities são vistas como hedge contra a inflação, atraindo investidores em momentos distintos do mercado geral.")
        ], className="mt-4 mb-4")
     ]))
])


# Callback para atualizar a lista de "Nomes" com base no "Ramo" selecionado
@app.callback(
    Output("nome-filter", "options"),
    Input("ramo-filter", "value")
)
def update_nome_dropdown(selected_ramo):
    if selected_ramo:
        nomes_filtrados = df_fechamento[df_fechamento["Ramo"] == selected_ramo]["Simbolo"].unique()
        return [{"label": nome, "value": nome} for nome in nomes_filtrados]
    return []

# Callback para atualizar o gráfico com base nos filtros
@app.callback(
    Output("fechamento-graph", "figure"),
    [Input("ramo-filter", "value"),
     Input("nome-filter", "value"),
     Input("start-date", "date"),
     Input("end-date", "date")]
)
def update_graph(selected_ramo, selected_nome, start_date, end_date):
    # Filtrando os dados com base nos filtros selecionados
    filtered_df = df_fechamento.copy()
    if selected_ramo:
        filtered_df = filtered_df[filtered_df["Ramo"] == selected_ramo]
    if selected_nome:
        filtered_df = filtered_df[filtered_df["Simbolo"] == selected_nome]
    if start_date:
        filtered_df = filtered_df[filtered_df["Data"] >= start_date]
    if end_date:
        filtered_df = filtered_df[filtered_df["Data"] <= end_date]

    # Criando o gráfico de fechamento
    fig = go.Figure(data=[
        go.Scatter(x=filtered_df["Data"], y=filtered_df["Fechamento"], mode="lines", name="Fechamento")
    ])
    fig.update_layout(title="Valores de Fechamento", xaxis_title="Data", yaxis_title="Fechamento")
    return fig

# Executando o aplicativo
if __name__ == "__main__":
    app.run_server(debug=True)
