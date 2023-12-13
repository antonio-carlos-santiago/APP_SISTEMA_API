import ast
from datetime import datetime, timedelta

from flet import *

from root_app.configuracoes.home.funcoes import buscar_selecionado, valida_cpf, consultar_margem, \
    salvar_dados_retornados, deletar_consulta
from root_app.configuracoes.home.models import Consulta
from root_app.configuracoes.login.funcoes import ler_imagem
from root_app.pages import dados_de_acesso_autorizado
from root_app.shared.database import SessionLocal
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import json

session = SessionLocal()


def calendario():
    return DatePicker(
        first_date=datetime(2023, 10, 1),
        last_date=datetime(2024, 10, 1),
        value=datetime.today()
    )


class NewHome(UserControl):

    def __init__(self, page):
        super().__init__()
        self.avisos_autenticacao = None
        self.botao_autenticacao = None
        self.dados_autenticados = dados_de_acesso_autorizado
        self.conteiner_autenticacao = None
        self.coluna_scroll = Column(
            scroll=ScrollMode.ALWAYS,
            auto_scroll=True,
            spacing=5,
            alignment=MainAxisAlignment.CENTER
        )
        self.imagem_svg_no_data = ler_imagem(r'root_app\imagens\imagem_no_data')
        self.campo_data = None
        self.conteiner_lista_clientes = None
        self.data_seguinte = None
        self.data_anterior = None
        self.barra_de_carregamento = None
        self.avisos_adicionais = None
        self.lista_convenio = None
        self.botao_busca = None
        self.formulario_cpf = None
        self.page = page
        self.cor_conteiner = '#696969'
        self.cor_do_botao = '#800000'
        self.calendario = calendario()
        self.page.overlay.append(self.calendario)
        self.calendario.on_change = self.change_date
        self.adiciona_elemento(datetime.today())

    def autentica(self, e):
        self.botao_autenticacao.disabled = True
        self.update()
        try:
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
            requests.request("PATCH", url, headers=headers, data=payload)
            self.avisos_autenticacao.value = f"Parabens!!, o convenio {convenio[0]} foi autenticada com sucesso"

        except:
            self.avisos_autenticacao.value = "Não foi realizada nenhuma autenticação"

        self.botao_autenticacao.disabled = False
        self.update()

    def tab_autenticacao(self):
        self.botao_autenticacao = ElevatedButton(text='Autenticar Sessão', on_click=self.autentica, height=60)
        self.avisos_autenticacao = Text()
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

    def elementos_tab(self):
        tabelas = Tabs(
            selected_index=0,
            animation_duration=300,
            width=200,
            height=600,
            label_color=self.cor_do_botao,
            indicator_border_radius=10,
            tabs=[
                Tab(text="Autenticação",
                    content=Container(
                        width=200,
                        height=600,
                        border_radius=10,
                        content=self.tab_autenticacao()
                    )
                    ),
                Tab(text='Emitir CC',
                    content=Container(
                        width=200,
                        height=600,
                        border_radius=10,
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Text(value="Ainda em desenvolvimento"),
                                Text(value="Em breve poderá emitir contracheques com mais eficiencia")
                            ]
                        )

                    )),
                Tab(text='Perfil',
                    content=Container(
                        width=200,
                        height=600,
                        border_radius=10)
                    ),
                Tab(text='Pagamentos',
                    content=Container(
                        width=200,
                        height=600,
                        border_radius=10,
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Text(value="Ainda em desenvolvimento"),
                                Text(value="Em breve hávera meios de pagamentos disponiveis :)")
                            ]
                        )
                    )
                    ),
            ]
        )

        return tabelas

    def buscar_margem(self, e):
        data_vencimento = datetime.strptime(dados_de_acesso_autorizado['vencimento'], "%Y-%m-%d")
        data_servidor = datetime.strptime(dados_de_acesso_autorizado['data_atual'], "%Y-%m-%d")
        if data_vencimento >= data_servidor:
            cpf = valida_cpf(self.formulario_cpf.value)
            if self.lista_convenio.value == 'Selecione o Convenio':
                self.lista_convenio.error_text = 'Verifique o convenio'
                self.update()
            elif not cpf:
                self.formulario_cpf.error_text = 'Verifique o CPF'
                self.update()
            else:

                self.barra_de_carregamento.visible = True
                self.botao_busca.visible = False
                self.update()
                resultado = consultar_margem(cpf, self.lista_convenio.value)
                if 'status' in resultado:
                    if not resultado['status']:
                        self.avisos_adicionais.value = resultado['info']
                        self.barra_de_carregamento.visible = False
                        self.avisos_adicionais.visible = True
                        self.botao_busca.visible = True
                        self.update()
                else:
                    salvar_dados_retornados(resultado)
                    self.avisos_adicionais.value = 'Cliente consultado'
                    self.barra_de_carregamento.visible = False
                    self.avisos_adicionais.visible = True
                    self.botao_busca.visible = True
                    self.adiciona_elemento(datetime.today())
                    self.campo_data.value = datetime.today().strftime('%d/%m/%Y')
                    self.calendario.value = datetime.today()
                    self.update()
        else:
            self.avisos_adicionais.value = "Usuario com pendencias"
            self.avisos_adicionais.visible = True
            self.update()

    def trata_erros(self, e):
        self.avisos_adicionais.visible = False
        self.formulario_cpf.error_text = None
        self.lista_convenio.error_text = None
        self.avisos_autenticacao.value = None
        self.update()

    def botao_selecionado(self, botao: ControlEvent):
        botao_string = str(botao.control)[10:]
        print(botao_string)
        botao_dicionario = ast.literal_eval(botao_string)
        buscar_selecionado(botao_dicionario['key'])
        self.page.go('/cliente')

    def deletar_consulta(self, botao: ControlEvent):
        botao_string = str(botao.control)[10:]
        print(botao_string)
        botao_dicionario = ast.literal_eval(botao_string)
        deletar_consulta(botao_dicionario['key'])
        self.adiciona_elemento(self.calendario.value)
        self.update()

    def elementos_pesquisa(self):
        self.formulario_cpf = TextField(
            hint_text='Insira o CPF',
            prefix_icon=icons.NUMBERS,
            border_color='white',
            input_filter=NumbersOnlyInputFilter(),
            cursor_color='black',
            max_length=11,
            width=300,
            text_size=20,
            text_align=TextAlign.CENTER,
            autofocus=True,
            counter_style=TextStyle(color='black'),
            border_radius=10,
            filled=True,
            on_change=self.trata_erros
        )
        self.lista_convenio = Dropdown(
            options=[dropdown.Option('Selecione o Convenio'), dropdown.Option('AMAZONPREV'),
                     dropdown.Option('MANAUS'),
                     dropdown.Option('PREFEITURA')],
            prefix_icon=icons.LIST,
            width=300,
            value='Selecione o Convenio',
            alignment=alignment.center,
            filled=True,
            border_color='white',
            border_radius=10,
            on_change=self.trata_erros
        )
        self.botao_busca = ElevatedButton(
            icon=icons.FIND_IN_PAGE,
            text='BUSCAR',
            width=200,
            height=40,
            elevation=10,
            bgcolor=self.cor_do_botao,
            color='white',
            on_click=self.buscar_margem,
        )
        self.barra_de_carregamento = Row([Icon(name=icons.FIND_IN_PAGE),
                                          ProgressBar(
                                              color="#8B0000",
                                              bgcolor="#778899",
                                              width=420,
                                              height=20,

                                          )],
                                         visible=False)
        self.avisos_adicionais = Text(
            value='Consulta Realizada com Sucesso!!',
            visible=False,
            text_align=TextAlign.CENTER,
            width=460,
            size=15,
            color='white'
        )

        elementos = Column(
            [
                Row([
                    self.formulario_cpf,
                ],
                    alignment=MainAxisAlignment.CENTER
                ),
                Row([
                    self.lista_convenio,
                ],
                    alignment=MainAxisAlignment.CENTER
                ),
                Container(
                    width=20,
                    height=30,
                    content=Column([
                        Row([self.avisos_adicionais]),
                        Row([self.barra_de_carregamento],
                            alignment=MainAxisAlignment.CENTER),

                    ],
                        alignment=MainAxisAlignment.CENTER),
                    alignment=alignment.center
                ),
                Column([
                    Row([
                        self.botao_busca
                    ],
                        alignment=MainAxisAlignment.CENTER
                    ),
                ],
                    alignment=MainAxisAlignment.CENTER)
            ], alignment=MainAxisAlignment.CENTER
        )
        return elementos

    def adiciona_elemento(self, data):
        data = datetime.date(data)
        self.coluna_scroll.controls.clear()
        clientes = session.query(Consulta).filter_by(data_consulta=data).all()
        if clientes:
            for cliente in clientes:
                linha = ExpansionPanelList(
                    controls=[
                        ExpansionPanel(
                            header=ListTile(title=Text(f'{cliente.nome} -- {cliente.matricula}')),
                            bgcolor=self.cor_do_botao,
                            content=Container(
                                content=Column(
                                    [
                                        Row([
                                            Text(value=f'Margem Emprestimo: {cliente.margem_emprestimo}'),
                                            Text(value=f'Margem cartão: {cliente.margem_emprestimo}')
                                        ]),
                                        Text(f"CPF : {cliente.cpf}"),
                                        Text(f"Convenio : {cliente.convenio}"),
                                        Container(
                                            content=Row(
                                                controls=[
                                                    Column(
                                                        controls=[
                                                            IconButton(
                                                                icon=icons.LIST,
                                                                icon_size=25,
                                                                on_click=self.botao_selecionado,
                                                                key=str(cliente.id_consulta)
                                                            ),
                                                            Text('Detalhes', size=10)
                                                        ],
                                                        spacing=1,
                                                        alignment=MainAxisAlignment.CENTER,
                                                        key=str(cliente.id_consulta)
                                                    ),
                                                    Column(
                                                        controls=[
                                                            IconButton(
                                                                icon=icons.DELETE_SHARP,
                                                                icon_size=25,
                                                                on_click=self.deletar_consulta,
                                                                key=str(cliente.id_consulta)
                                                            ),
                                                            Text('Detalhes', size=10)
                                                        ],
                                                        spacing=1,
                                                        alignment=MainAxisAlignment.CENTER,
                                                        key=str(cliente.id_consulta)
                                                    ),
                                                    Column(
                                                        controls=[
                                                            IconButton(
                                                                icon=icons.PRINT,
                                                                icon_size=25,
                                                                disabled=True,
                                                                tooltip="Ainda em desenvolvimento"
                                                            ),
                                                            Text('Imp CC', size=10)
                                                        ],
                                                        spacing=1,
                                                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                        key=str(cliente.id_consulta)
                                                    )
                                                ],
                                                alignment=MainAxisAlignment.SPACE_AROUND),
                                            bgcolor='black',
                                            border_radius=10,
                                            padding=padding.only(left=20, right=20)
                                        )
                                    ],
                                ),
                                padding=padding.only(left=20, bottom=20, right=20)
                            ),
                        )
                    ])
                self.coluna_scroll.controls.append(linha)
        else:
            self.coluna_scroll.controls.append(
                Container(
                    width=500,
                    height=500,
                    content=Image(src=self.imagem_svg_no_data)
                )
            )
        self.update()

    def change_date(self, e):
        self.campo_data.value = self.calendario.value.strftime('%d/%m/%Y')
        self.adiciona_elemento(self.calendario.value)
        self.update()

    def dininui_data(self, e):
        self.calendario.value = self.calendario.value - timedelta(days=1)
        self.campo_data.value = self.calendario.value.strftime('%d/%m/%Y')
        self.adiciona_elemento(self.calendario.value)
        self.update()

    def adiciona_data(self, e):
        self.calendario.value = self.calendario.value + timedelta(days=1)
        self.campo_data.value = self.calendario.value.strftime('%d/%m/%Y')
        self.adiciona_elemento(self.calendario.value)
        self.update()

    def elementos_titulo_cliente(self):
        self.data_anterior = IconButton(icon=icons.ARROW_LEFT, bgcolor=self.cor_do_botao, on_click=self.dininui_data)
        self.data_seguinte = IconButton(icon=icons.ARROW_RIGHT, bgcolor=self.cor_do_botao, on_click=self.adiciona_data)
        self.campo_data = Text(value=f"{datetime.today().strftime('%d/%m/%Y')}", bgcolor=self.cor_do_botao, size=20)

        elementos = Row(
            controls=[
                self.data_anterior,
                Container(
                    content=self.campo_data,
                    bgcolor=self.cor_do_botao,
                    height=40,
                    border_radius=20,
                    width=150,
                    alignment=alignment.center
                ),
                IconButton(icon=icons.CALENDAR_MONTH, bgcolor=self.cor_do_botao,
                           on_click=lambda _: self.calendario.pick_date()),
                self.data_seguinte
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN
        )
        return elementos

    def build(self):

        conteiner_pesquisa = Container(
            bgcolor=self.cor_conteiner,
            width=500,
            height=300,
            border_radius=15,
            padding=padding.only(right=20, left=20, bottom=10),
            content=self.elementos_pesquisa(),
            on_hover=self.trata_erros

        )

        self.conteiner_autenticacao = Container(
            bgcolor=self.cor_conteiner,
            width=500,
            height=300,
            border_radius=15,
            padding=padding.only(right=20, left=20, bottom=20),
            content=self.elementos_tab(),
            on_hover=self.trata_erros
        )

        conteiner_titulo_cliente = Container(
            bgcolor=self.cor_conteiner,
            width=500,
            height=50,
            border_radius=15,
            padding=padding.only(top=5, right=80, left=80, bottom=5),
            content=self.elementos_titulo_cliente()
        )

        self.conteiner_lista_clientes = Container(
            bgcolor=self.cor_conteiner,
            width=500,
            height=550,
            border_radius=15,
            padding=padding.only(top=20, right=20, left=20, bottom=20),
            content=self.coluna_scroll

        )
        return Row(
            [
                Column([
                    conteiner_pesquisa,
                    self.conteiner_autenticacao
                ]),
                Column([
                    conteiner_titulo_cliente,
                    self.conteiner_lista_clientes
                ])
            ]
        )
