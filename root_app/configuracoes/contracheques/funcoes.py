import base64
import json
import os
from datetime import datetime

import requests

from root_app import Contracheque
from root_app.pages import dados_de_acesso_autorizado
from root_app.shared.database import SessionLocal

sessao = SessionLocal()


def decode_code(codigo, matricula, nome_cliente, mes, ano):
    codificado = base64.b64decode(codigo)
    caminho_da_pasta = f'/CLIENTES/{nome_cliente.upper()}'
    if not os.path.exists(caminho_da_pasta):
        os.makedirs(caminho_da_pasta)

    caminho_data_emitido = f'{caminho_da_pasta}/{mes}-{ano}'
    if not os.path.exists(caminho_data_emitido):
        os.makedirs(caminho_data_emitido)

    caminho_da_matricula = f'{caminho_data_emitido}/{matricula}'
    if not os.path.exists(caminho_da_matricula):
        os.makedirs(caminho_da_matricula)

    caminho_do_arquivo = os.path.join(caminho_data_emitido, f'{matricula}.pdf')
    with open(caminho_do_arquivo, 'wb') as documento:
        documento.write(codificado)
        return


# def encode_code(arquivo):
#     with open(arquivo, "rb") as documento:
#         bytes_arquivo = documento.read()
#         arquivo_base64 = base64.b64encode(bytes_arquivo).decode('utf-8')
#         return arquivo_base64


def verificar_retorno(retorno):
    if not retorno['error']:
        return True
    return False


def get_contracheque(cpf, mes, ano, idproposta=None):
    link_api = "https://rhmobile.prodam.am.gov.br/econtracheque/api/v2/contracheque/contracheques/"
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'host': 'rhmobile.prodam.am.gov.br',
        'user-agent': 'Dart/2.17 (dart:io)',
        'accept-encoding': 'gzip'
    }
    metodos = {
        'consulta': 'consultar',
        'download': 'download'
    }

    tipo_data = {
        'consulta': {
            "ano": ano,
            "cpf": cpf,
            "cpfServidor": cpf,
            "dispositivo": "M",
            "mes": mes
        },
        'download': {
            "cpfServidor": cpf,
            "dispositivo": "M",
            "id": idproposta,
            "tipo": "M"
        }
    }
    parametro = None
    if idproposta is None:
        parametro = 'consulta'
    else:
        parametro = 'download'

    payload = json.dumps(tipo_data[parametro])

    informacoes_servidor = requests.post(f"{link_api}{metodos[parametro]}", headers=headers, data=payload)
    return informacoes_servidor.json()


def consulta(cpf, mes, ano):
    solicitacao = get_contracheque(cpf, mes, ano)
    autenticacao = verificar_retorno(solicitacao)
    if autenticacao:
        for matricula in solicitacao['contracheques']:
            contracheque = get_contracheque(cpf, mes, ano, matricula['id'])
            print(contracheque['imagem'], type(contracheque['imagem']))
            data_referencia_formatada = datetime.strptime(f"{mes}-{ano}", "%m-%Y")
            data_download = datetime.strptime(dados_de_acesso_autorizado['data_atual'], "%Y-%m-%d")
            novo_contracheque = Contracheque(
                imagem_contracheque=contracheque['imagem'],
                matricula=matricula['id'],
                data_referencia=data_referencia_formatada,
                data_baixada=data_download,
                cpf=cpf
            )
            sessao.add(novo_contracheque)
            sessao.commit()
        return {'status': True}
    else:
        return {'status': False}
