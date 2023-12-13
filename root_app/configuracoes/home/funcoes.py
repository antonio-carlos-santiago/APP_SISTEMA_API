import json

import requests
from flet import *
from validate_docbr import CPF

from root_app.configuracoes.home.models import *
from root_app.pages import URL_APP
from root_app.shared.database import SessionLocal

sessao = SessionLocal()


def listar_convenios():
    url = f"{URL_APP}/convenios/convenio"
    payload = {}
    headers = {'accept': 'application/json'}
    response = requests.request("GET", url, headers=headers, data=payload)
    convenios = [data['convenio'] for data in response.json() if data['convenio']]
    return convenios


def consultar_margem(cpf, convenio):
    url = f"{URL_APP}/servicosconsuta"
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
    url = f"{URL_APP}/sessao/listar-sessoes"

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
        salva_cliente(
            cpf=dados_linha['dados_cliente']['cpf'],
            nome=dados_linha['dados_cliente']['nome']
        )
        salvar_matricula(
            cpf=dados_linha['dados_cliente']['cpf'],
            matricula=dados_linha['dados_cliente']['matricula']
        )
        registrar_consulta_diaria(
            cpf=dados_linha['dados_cliente']['cpf'],
            matricula=dados_linha['dados_cliente']['matricula'],
            convenio=dados_linha['dados_consulta']['convenio'],
            nome=dados_linha['dados_cliente']['nome'],
            margem_emprestimo=dados_linha['dados_margens'][0]['Margem 35% Empréstimos e Outros']['margem_atual'],
            margem_cartao=dados_linha['dados_margens'][1]['Margem 5% Cartão']['margem_atual'],
            mes_referencia=dados_linha['dados_cliente']['mes_referencia'],
            emprestimos=dados_linha['dados_emprestimos'],
            cartoes=dados_linha['dados_cartoes']
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


def registrar_consulta_diaria(cpf, matricula, convenio, nome, margem_emprestimo,
                              margem_cartao, mes_referencia, emprestimos, cartoes):

    nova_consulta = Consulta(
        cpf=cpf,
        matricula=matricula,
        convenio=convenio,
        nome=nome,
        margem_emprestimo=margem_emprestimo,
        margem_cartao=margem_cartao,
        mes_referencia=mes_referencia,
        emprestimos=emprestimos,
        cartoes=cartoes
    )
    sessao.add(nova_consulta)
    sessao.commit()


def consultas_diarias_realizadas():
    todas_as_consultas = sessao.query(Consulta).all()
    return todas_as_consultas


def buscar_selecionado(id_selecionado):
    matricula_registrada = sessao.query(Selecionado).first()
    if not matricula_registrada:
        nova_matricula = Selecionado(id_selecionado_cliente=int(id_selecionado))
        sessao.add(nova_matricula)
        sessao.commit()
    else:
        matricula_registrada.id_selecionado_cliente = int(id_selecionado)
        sessao.commit()


def deletar_consulta(id_selecionado):
    consulta_selecionada = sessao.query(Consulta).filter_by(id_consulta=int(id_selecionado)).first()
    sessao.delete(consulta_selecionada)
    sessao.commit()
