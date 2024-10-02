import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados do CSV
df = pd.read_csv('historico_AAPL.csv')  # Substitua pelo caminho correto do arquivo CSV

# Converter a coluna 'Data' para o tipo datetime, especificando que o dia vem primeiro
df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)

# Definir a 'Data' como índice para facilitar a plotagem
df.set_index('Data', inplace=True)

# Plotar o gráfico com o desempenho (Último)
plt.figure(figsize=(10, 6))

plt.plot(df.index, df['Último'], label='Último', linestyle='-', color='black')

# Personalizações do gráfico
plt.title('Desempenho da Empresa na Bolsa')
plt.xlabel('Data')
plt.ylabel('Valor')
plt.legend()
plt.grid(True)

# Exibir o gráfico
plt.show()