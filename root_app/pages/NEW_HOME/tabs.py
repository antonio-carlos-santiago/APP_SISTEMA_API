from time import sleep

from flet import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import json
from root_app.pages import dados_de_acesso_autorizado


def autentica(e):
    url = "http://127.0.0.1:8000/sessao/nova-sessao"
    options = Options()
    service = Service()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(30)
    driver.get('https://nconsig.fenixsoft.com.br/Login.aspx')
    while len(driver.find_elements(By.XPATH, '//*[@id="userLabel"]')) < 1:
        sleep(1)
    site = BeautifulSoup(driver.page_source, 'html.parser')
    convenio = site.find('span', attrs={"id": "descricaoOrgaoLabel"}).text.split()
    print(convenio[0])
    payload = json.dumps({
        "sessao": driver.get_cookies()[0]['value'],
        "convenio": convenio[0],
        "email": dados_de_acesso_autorizado['email']
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)




def tab_autenticacao():
    return Column(
        horizontal_alignment=CrossAxisAlignment.CENTER,
        controls=[
            Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Checkbox(label='Fenix', value=True, disabled=True),
                    Checkbox(label='Consiglog', value=False, disabled=True)
                ]
            ),
            Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    ElevatedButton(text='Autenticar Sessão', on_click=autentica)
                ]
            )
        ]
    )
