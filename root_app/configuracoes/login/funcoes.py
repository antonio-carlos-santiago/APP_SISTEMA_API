import json

import requests

from root_app.pages import URL_APP


def ler_imagem(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        svg_codigo = arquivo.read()
    return svg_codigo


def efetua_login(usuario: str, senha: str):
    url = f"{URL_APP}/usuarios/login-user"

    payload = json.dumps({
        "email": f"{usuario.lower()}",
        "senha": senha
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


def dados_de_acesso(dados_resevados):
    print(dados_resevados)
    # email = dados_resevados.email
    # nome = dados_resevados.nome
    # nome_escritorio = dados_resevados.nome_escritorio
    # cpfoucnpf = dados_resevados.cpfoucnpf
    # vencimento = dados_resevados.vencimento
    # telefone = dados_resevados.telefone
