# Aula 08
# Adicionando o repositorio
# git clone + endereço do git hub na pasta raiz = 7P_Ciencia_Dados
# john@kurupira:~/Documents/IFTM/ADS/7P_Ciencia_de_Dados/CDados_Aula08$ git add .
# john@kurupira:~/Documents/IFTM/ADS/7P_Ciencia_de_Dados/CDados_Aula08$ git commit -m "Primeira atualização"
# [main (root-commit) 9c8e99f] Primeira atualização
#  1 file changed, 1 insertion(+)
#  create mode 100644 main.py
# john@kurupira:~/Documents/IFTM/ADS/7P_Ciencia_de_Dados/CDados_Aula08$ git push origin main
# Enumerating objects: 3, done.
# Counting objects: 100% (3/3), done.
# Writing objects: 100% (3/3), 246 bytes | 246.00 KiB/s, done.
# Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
# To https://github.com/Sulphuratus/CDados_Aula08.git
#  * [new branch]      main -> main
# john@kurupira:~/Documents/IFTM/ADS/7P_Ciencia_de_Dados/CDados_Aula08$ 

# pip install numpy # para instalar o numpy no terminal se necessário

import sys
import os
import numpy as np

"""# Configuração do Web-Driver"""
# Utilizando o WebDriver do Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Instanciando o Objeto ChromeOptions
options = webdriver.ChromeOptions()

# Passando algumas opções para esse ChromeOptions, existem muitos mais argumentos
# Estes sao os usados como padrão
options.add_argument('--headless')  # robô nao abre a pagina quando entrar, fica só na memória
options.add_argument('--no-sandbox')  # retirar o sandbox = área de testes do navegador
options.add_argument('--disable-dev-shm-usage') 
options.add_argument('--start-maximized')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-crash-reporter')
options.add_argument('--log-level=3')
options.add_argument('--disable-gpu')


# Criação d instância do WebDriver do Chrome
wd_Chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

"""# Importando as Bibliotecas"""

import pandas as pd
import time  # importante para o sleep dando tempo de carregar a página e buscar os dados
from tqdm import tqdm

"""# Iniciando a Raspagem de Dados"""

# Com o WebDrive a gente consegue a pedir a página (URL)
wd_Chrome.get("https://www.flashscore.com/") # Nome pode ser qquer um = WD_Chrome, chinelinho, etc
time.sleep(2)

# para pegar do próximo dia
# next_day = wd_Chrome.find_elements(By.CSS_SELECTOR,'button.calendar__navigation--tomorrow')

#  para pegar do dia anterior
day_before = wd_Chrome.find_elements(By.CSS_SELECTOR,'button.calendar__navigation--yesterday')

for button in day_before:
    wd_Chrome.execute_script("arguments[0].click();", button)
time.sleep(2)

# Novo codigo dia 21/06 = procurar botao scheduled = jogos futuros
# scheduled = wd_Chrome.find_elements(By.CSS_SELECTOR,'div.filters__text--default')[2]
# wd_Chrome.execute_script("arguments[0].click();", scheduled)
# print(scheduled.text)

finished = wd_Chrome.find_elements(By.CSS_SELECTOR,'div.filters__text--default')[1]
wd_Chrome.execute_script("arguments[0].click();", finished)

dados = {
    "HOME":[],
    "AWAY":[],
    "FTHG":[],
    "FTAG":[]
}

count = 0
# evento = wd_Chrome.find_elements(By.CSS_SELECTOR, 'div.event__match--twoLine')[0] # [0] = Só a primeira
eventos = wd_Chrome.find_elements(By.CSS_SELECTOR, 'div.event__match--twoLine')

# for evento in tqdm(eventos, total)

for evento in eventos:                      # for loop adicionado depois
    try:
        count += 1
        home = evento.find_element(By.CSS_SELECTOR, 'div.event__homeParticipant').text
        away = evento.find_element(By.CSS_SELECTOR, 'div.event__awayParticipant').text
        fthg = evento.find_element(By.CSS_SELECTOR, 'div.event__score--home').text  #Adicionado
        ftag = evento.find_element(By.CSS_SELECTOR, 'div.event__score--away').text  #Adicionado
        # golsHome = evento.find_element(By.CSS_SELECTOR, 'div.event__score--home').text  #Adicionado
        # golsAway = evento.find_element(By.CSS_SELECTOR, 'div.event__score--away').text  #Adicionado
        # print(f'Evento: {home} x {away}')  # Primeira raspagem
        # print(f'Evento: {home} {golsHome} x {golsAway} {away}')
        dados["HOME"].append(home)
        dados["AWAY"].append(away)
        dados["FTHG"].append(fthg)
        dados["FTAG"].append(ftag)
        
    except Exception as error:
        print(f'Evento: {home} x {away}\nErro: {error}')
        pass
    
print(f'{count} jogos.')

df = pd.DataFrame(dados)
filename = "datasetFlashscore.csv"
df.to_csv(filename, sep=";", index=False)


# Completar:
# Acessar páginas diferentes (ao vivo, encerrados, próximos, odds) com .click() ou execute_script()
# Pegar o placar do jogo
# Pegar o tempo de jogo
# Acessar a página específica de um jogo e pegar stats
# Acessar a página específica de um time e pegar placares passados