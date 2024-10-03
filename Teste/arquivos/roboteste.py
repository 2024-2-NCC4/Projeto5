from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# Caminho para o ChromeDriver
chromedriver_path = "C:/Users/vitor/Downloads/chromedriver-win64/chromedriver.exe"

# Configurar o ChromeOptions
options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# **Remova ou comente as linhas abaixo para não carregar o perfil**
options.add_argument("user-data-dir=C:/Users/vitor/AppData/Local/Google/Chrome/User Data")
options.add_argument("profile-directory=automacaofecap")  # Ou o nome do seu perfil

# Inicializar o driver
driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

# Esperar o navegador iniciar
time.sleep(5)

# Tentar abrir o site
try:
    print("Tentando navegar para o site...")
    driver.get("https://br.investing.com/")
    print("Página carregada com sucesso.")
except Exception as e:
    print(f"Erro ao carregar a página: {e}")
x
# Manter o navegador aberto para visualização
input("Pressione Enter para fechar o navegador...")
driver.quit()
