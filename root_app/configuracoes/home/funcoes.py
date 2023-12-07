import json

import requests
from flet import *
from validate_docbr import CPF

from root_app.configuracoes.home.models import *
from root_app.shared.database import SessionLocal

sessao = SessionLocal()


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


def salvar_dados_retornados(dados):
    for dados_linha in dados:
        print(dados_linha)
        salva_cliente(
            cpf=dados_linha['dados_cliente']['cpf'],
            nome=dados_linha['dados_cliente']['nome']
        )
        salvar_matricula(
            cpf=dados_linha['dados_cliente']['cpf'],
            matricula=dados_linha['dados_cliente']['matricula']
        )
        salvar_emprestimos(dados_linha)
        registrar_consulta_diaria(
            cpf=dados_linha['dados_cliente']['cpf'],
            matricula=dados_linha['dados_cliente']['matricula'],
            convenio=dados_linha['consignataria']['convenio']
        )


def salva_cliente(cpf, nome):
    busca_cliente = sessao.query(Cliente).filter_by(cpf=cpf).first()
    if not busca_cliente:
        novo_cliente = Cliente(
            cpf=cpf,
            nome=nome
        )
        sessao.add(novo_cliente)
        sessao.commit()


def salvar_matricula(cpf: str, matricula: str):
    verificar_matricula = sessao.query(Matricula).filter_by(matricula=matricula).first()
    if not verificar_matricula:
        cliente = sessao.query(Cliente).filter_by(cpf=cpf).first()
        nova_matricula = Matricula(matricula=matricula, cliente_responsavel_id=int(cliente.id_cliente))
        sessao.add(nova_matricula)
        sessao.commit()


def salvar_emprestimos(dados):

    matricula = sessao.query(Matricula).filter_by(matricula=dados['dados_cliente']['matricula']).first()
    id_cliente = matricula.cliente_responsavel_id
    id_matricula = matricula.id_matricula
    lista_emprestimos = dados['dados_emprestimos']
    for emprestimo in lista_emprestimos:
        linha_emprestimo = Emprestimo(
            margem_emprestimo=dados['dados_margens'][0]['Margem 35% Empréstimos e Outros']['margem_atual'],
            margem_cartao=dados['dados_margens'][1]['Margem 5% Cartão']['margem_atual'],
            mes_referencia=dados['dados_cliente']['mes_referencia'],
            ade=emprestimo['ade'],
            deferido=emprestimo['data_deferimento'],
            servico=emprestimo['servicos'],
            consignataria=emprestimo['consignataria'],
            pagas=emprestimo['parcela_atual'],
            total=emprestimo['parcela_total'],
            valor=emprestimo['valor'],
            status=emprestimo['status'],
            cliente_responsavel_id=id_cliente,
            matricula_responsavel_id=id_matricula
        )
        sessao.add(linha_emprestimo)
        sessao.commit()


def registrar_consulta_diaria(cpf, matricula, convenio):
    nova_consulta = Consulta(
        cpf=cpf,
        matricula=matricula,
        convenio=convenio
    )
    sessao.add(nova_consulta)
    sessao.commit()
