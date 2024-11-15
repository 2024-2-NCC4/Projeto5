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
        html.Div("Análise de crescimento médio anual por setor...", className="mt-2 mb-4")
    ])),

    dbc.Row(dbc.Col([
        dcc.Graph(figure=fig_crescimento_previsoes),
        html.Div("Projeções de crescimento médio anual com previsões...", className="mt-2 mb-4")
    ])),

    html.Hr(),

    dbc.Row(dbc.Col([
        dcc.Graph(figure=fig_grau_influencia),
        html.Div("Gráfico de grau de influência entre setores...", className="mt-2 mb-4")
    ])),

    dbc.Row(dbc.Col([
        dcc.Graph(figure=fig_matriz_correlacao),
        html.Div("Matriz de correlação entre os setores...", className="mt-2 mb-4")
    ])),

    html.Hr(),

    dbc.Row(dbc.Col(html.H2("Tabela de Correlação e Beta por Setor", className="text-center mt-4"))),

    dbc.Row(dbc.Col(
        dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in df_tabela_final.columns],
            data=df_tabela_final.to_dict("records"),
            style_table={"width": "80%", "margin": "auto"},
            style_cell={'textAlign': 'center', 'padding': '5px'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
        ), width=12
        )
    ),html.Div("Matriz de correlação entre os setores...", className="mt-2 mb-4"),
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
