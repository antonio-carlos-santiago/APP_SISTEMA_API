import json
from time import sleep

import requests
from bs4 import BeautifulSoup
from flet import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from root_app.pages import URL_APP, dados_de_acesso_autorizado


class Autenticacao(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.botao_autenticacao = ElevatedButton(
            text='Autenticar Sessão',
            height=60)

        self.avisos_autenticacao = Text()

    def autentica(self, e):
        self.botao_autenticacao.disabled = True
        self.update()
        try:
            url = f"{URL_APP}/sessao/nova-sessao"
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            service = Service()
            options.add_argument('--start-maximized')
            driver = webdriver.Chrome(service=service, options=options)
            driver.implicitly_wait(30)
            driver.get('https://nconsig.fenixsoft.com.br/Login.aspx')
            while len(driver.find_elements(By.XPATH, '//*[@id="userLabel"]')) < 1:
                sleep(1)
            site = BeautifulSoup(driver.page_source, 'html.parser')
            convenio = site.find('span', attrs={"id": "descricaoOrgaoLabel"}).text.split()
            payload = json.dumps({
                "sessao": driver.get_cookies()[0]['value'],
                "convenio": convenio[0],
                "email": dados_de_acesso_autorizado['email']
            })
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            requests.request("PATCH", url, headers=headers, data=payload)
            self.avisos_autenticacao.value = f"Parabens!!, o convenio {convenio[0]} foi autenticada com sucesso"
            self.update()
            sleep(5)

        except:
            self.avisos_autenticacao.value = "Não foi realizada nenhuma autenticação"
            self.update()
            sleep(5)

        self.avisos_autenticacao.value = ""
        self.botao_autenticacao.disabled = False
        self.update()

    def build(self):
        self.botao_autenticacao.on_click = self.autentica
        return Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Container(
                    height=30,
                    width=20
                ),
                Row(
                    alignment=MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        Checkbox(label='Fenix', value=True, disabled=True),
                        Checkbox(label='Consiglog', value=False, disabled=True)
                    ]
                ),
                Container(
                    height=20,
                    width=20
                ),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        self.botao_autenticacao
                    ]
                ),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        self.avisos_autenticacao
                    ]
                )
            ]
        )
