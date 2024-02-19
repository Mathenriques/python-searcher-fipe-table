from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

def get_random_option(select_element):
  options_with_value = [option.text for option in select_element.options if option.get_attribute("value")]
  
  if options_with_value:
    selected_option = random.choice(options_with_value)
    select_element.select_by_visible_text(selected_option)
    return selected_option
  else:
    return None


def get_selected_text(select_element):
    return select_element.first_selected_option.text

def wait_and_click(element, timeout=10):
    time.sleep(timeout)
    element.click()

# Abrir o site
service = Service(executable_path="chromedriver")

# Inicializa o driver do Selenium
driver = webdriver.Chrome(service=service)
driver.get("https://veiculos.fipe.org.br/")

# Abre Modal
link = driver.find_element(By.CSS_SELECTOR, '[data-label="carro"]')
link.click()

for _ in range(10):

  # Selecionar marca aleatória
  select_brand_element = driver.find_element(By.ID, 'selectMarcacarro')
  select_brand = Select(select_brand_element)
  brandCar = get_random_option(select_brand)

  # Selecionar modelo aleatório
  select_model_element = driver.find_element(By.ID, 'selectAnoModelocarro')
  select_model = Select(select_model_element)
  selected_option_modelo = get_random_option(select_model)

  # Selecionar ano aleatório
  select_year_element = driver.find_element(By.ID, 'selectAnocarro')
  select_year = Select(select_year_element)
  selected_option_year = get_random_option(select_year)

  # Clicar no botão Pesquisar
  button_pesquisar = driver.find_element(By.ID, 'buttonPesquisarcarro')
  # Esperar até que o botão seja clicável
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'buttonPesquisarcarro')))
  button_pesquisar.click()

  # Aguardar e imprimir resultado
  wait_and_click(driver.find_element(By.ID, 'resultadoConsultacarroFiltros'))
  info_dict = {}

  for tr in driver.find_elements(By.XPATH, '//table[@width="100%"]/tbody/tr'):
      key = tr.find_element(By.XPATH, './/td[1]').text.strip().lower().replace(' ', '_')
      value = tr.find_element(By.XPATH, './/td[2]').text.strip()
      info_dict[key] = value

  print(info_dict)

# Aguardar antes de fechar o navegador
driver.quit()
