from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

# Configurar para ignorar a verificação SSL
os.environ['WDM_SSL_VERIFY'] = '0'

# Configurar o ChromeOptions para usar o perfil
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\23024522\\AppData\\Local\\Google\\Chrome\\User Data")  # Caminho para a pasta de dados do usuário
options.add_argument("profile-directory=Lucca")  # Nome do diretório do perfil

# Especificar o caminho do executável do Chrome (caso necessário)
options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # Altere para o caminho do executável do Chrome no seu sistema

# Inicializando o driver do Chrome com as opções configuradas
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Abrindo uma página (exemplo: Google)
driver.get("https://br.investing.com/")

# Manter o navegador aberto para visualização
input("Pressione Enter para fechar o navegador...")

# Fechar o navegador
driver.quit()
