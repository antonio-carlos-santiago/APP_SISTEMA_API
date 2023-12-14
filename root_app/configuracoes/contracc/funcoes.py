import requests
import json
import base64
import os


def decode_code(codigo, nome, nome_cliente):
    codificado = base64.b64decode(codigo)
    caminho_da_pasta = f'/CLIENTES/{nome_cliente.upper()}'
    if not os.path.exists(caminho_da_pasta):
        os.makedirs(caminho_da_pasta)

    caminho_do_arquivo = os.path.join(caminho_da_pasta, f'{nome}.pdf')
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


def consulta(cpf, mes, ano, nome_cliente):
    solicitacao = get_contracheque(cpf, mes, ano)
    autenticacao = verificar_retorno(solicitacao)
    if autenticacao:
        for matricula in solicitacao['contracheques']:
            contracheque = get_contracheque(cpf, mes, ano, matricula['id'])
            decode_code(contracheque['imagem'], f"{mes}-{ano}-{matricula['matricula']}", nome_cliente)
        return {'status': True}
    else:
        return {'status': False}


