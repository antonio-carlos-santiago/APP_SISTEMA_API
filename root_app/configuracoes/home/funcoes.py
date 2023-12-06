import json

import requests
from flet import *
from validate_docbr import CPF


def listar_convenios():
    url = "http://127.0.0.1:8000/convenios/convenio"
    payload = {}
    headers = {'accept': 'application/json'}
    response = requests.request("GET", url, headers=headers, data=payload)
    convenios = [data['convenio'] for data in response.json() if data['convenio']]
    return convenios


def consultar_margem(cpf, convenio):
    url = "http://127.0.0.1:8000/servicosconsuta"
    payload = json.dumps({
        "cpf": cpf,
        "convenio": convenio,
        "email_responsavel": "carlos.santiago013@gmail.com"
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


def valida_cpf(cpf):
    cpf_validator = CPF()
    while len(cpf) != 11:
        cpf = f"0{cpf}"
    if cpf_validator.validate(cpf):
        return cpf
    else:
        return False


def autenticacao_sessao(e):
    print('olá')


def verifica_sessoes(convenios):
    lista_de_funcoes = []
    url = "http://127.0.0.1:8000/sessao/listar-sessoes"

    payload = {}
    headers = {
        'accept': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    convenios_ativos = response.json()
    for convenio in convenios:
        for convenio_retornado in convenios_ativos:
            if convenio_retornado['convenio'] == convenio:
                linha = Row([Icon(name=icons.CHECK), Text(value=convenio, width=100)],
                            alignment=MainAxisAlignment.SPACE_EVENLY)
                lista_de_funcoes.append(linha)

    return lista_de_funcoes
