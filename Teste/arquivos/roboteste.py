from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options

# Configuração do WebDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver_path = "Teste\\arquivos\\chromedriver\\chromedriver.exe"  # Substitua pelo caminho do seu chromedriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Acessa a página de login do Google
    driver.get("https://accounts.google.com/signin")

    # Espera até que o campo de email esteja presente e o seleciona
    email_field = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@type='email']"))
    )
    email_field.send_keys("fecapgrupo5@gmail.com")  # Substitua pelo seu e-mail
    email_field.send_keys(Keys.RETURN)

    # Espera até que o campo de senha esteja presente e o seleciona
    password_field = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))
    )
    password_field.send_keys("")  #TODO Substitua pela sua senha
    password_field.send_keys(Keys.RETURN)

    print("Login realizado com sucesso!")

    # Acessa o site br.investing.com
    driver.get("https://br.investing.com")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'topBar')]"))
    )
    print("Site br.investing.com acessado com sucesso!")

    # Clica no botão de login no site br.investing.com
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='login']"))
    )
    login_button.click()
    print("Botão de login clicado com sucesso!")

except TimeoutException:
    print("Erro: O campo não foi encontrado a tempo.")

finally:
    # Fecha o navegador
    driver.quit()