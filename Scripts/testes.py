import pandas as pd
import matplotlib.pyplot as plt

def plotar_desempenho_acoes():
    # Caminho do arquivo concatenado
    csv_file = 'C:\Projetos\Projeto5\Dados\concatenado.csv'
    
    # Ler o CSV concatenado
    df = pd.read_csv(csv_file)
    
    # Converter a coluna 'Data' para o formato datetime
    df['Data'] = pd.to_datetime(df['Data'], format='%d.%m.%Y')
    
    # Filtrar empresas de aviação e de petróleo
    aviacao_df = df[df['Ramo'] == 'Aviacao']
    petroleo_df = df[df['Ramo'] == 'Petroleo']
    
    # Configurar o gráfico
    plt.figure(figsize=(12, 6))
    
    # Plotar as ações de aviação
    for simbolo in aviacao_df['Simbolo'].unique():
        empresa = aviacao_df[aviacao_df['Simbolo'] == simbolo]
        plt.plot(empresa['Data'], empresa['Fechamento'], label=simbolo)
    
    # Plotar as ações de petróleo
    for simbolo in petroleo_df['Simbolo'].unique():
        empresa = petroleo_df[petroleo_df['Simbolo'] == simbolo]
        plt.plot(empresa['Data'], empresa['Fechamento'], label=simbolo)
    
    # Adicionar título e rótulos
    plt.title('Desempenho das Ações - Aviação e Petróleo')
    plt.xlabel('Data')
    plt.ylabel('Preço de Fechamento (USD)')
    
    # Adicionar legenda
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    # Exibir o gráfico
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Executar a função
plotar_desempenho_acoes()