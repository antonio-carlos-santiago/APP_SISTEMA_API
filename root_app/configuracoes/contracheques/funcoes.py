import base64
import json
import subprocess
import os
from datetime import datetime

import requests

from root_app import Contracheque
from root_app.pages import dados_de_acesso_autorizado
from root_app.shared.database import SessionLocal

sessao = SessionLocal()


def decode_code(codigo, matricula, mes, ano):
    codificado = base64.b64decode(codigo)
    caminho_local = os.getcwd()
    caminho_da_pasta = f'{caminho_local}/CLIENTES/{matricula}'
    if not os.path.exists(caminho_da_pasta):
        os.makedirs(caminho_da_pasta)
    pasta_cliente = os.path.join(caminho_local, 'CLIENTES', f'{matricula}')
    caminho_do_arquivo = os.path.join(caminho_da_pasta, f'{matricula}.pdf')
    with open(caminho_do_arquivo, 'wb') as documento:
        documento.write(codificado)
    return pasta_cliente


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
            matriculas_no_banco = sessao.query(Contracheque).filter_by(matricula=matricula['id']).first()
            if not matriculas_no_banco:
                contracheque = get_contracheque(cpf, mes, ano, matricula['id'])
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
                caminho_cc_pdf = decode_code(contracheque['imagem'], matricula['id'], mes, ano)
                subprocess.Popen(['explorer', caminho_cc_pdf], shell=True)
            else:
                caminho_cc_pdf = decode_code(
                    matriculas_no_banco.imagem_contracheque,
                    matriculas_no_banco.matricula,
                    mes,
                    ano
                )
                subprocess.Popen(['explorer', caminho_cc_pdf], shell=True)
        return True
    else:
        return False
