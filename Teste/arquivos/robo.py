from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

# Configurar para ignorar a verificação SSL
os.environ['WDM_SSL_VERIFY'] = '0'

# Inicializando o driver do Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\23024522\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("profile-directory=Lucca")

driver = webdriver.Chrome(options=options)

# Abrindo uma página (exemplo: Google)
driver.get("https://br.investing.com/")

# Manter o navegador aberto para visualização
input("Pressione Enter para fechar o navegador...")

# Fechar o navegador
driver.quit()