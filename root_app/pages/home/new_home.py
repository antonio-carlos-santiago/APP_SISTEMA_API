import ast
from datetime import datetime, timedelta

from flet import *

from root_app.configuracoes.home.funcoes import buscar_selecionado, deletar_consulta
from root_app.configuracoes.home.models import Consulta
from root_app.configuracoes.login.funcoes import ler_imagem
from root_app.pages import dados_de_acesso_autorizado
from root_app.pages.home.abas.abas_gerais import AbaFather
from root_app.pages.home.pesquisa.elementos_pesquisas import Pesquisas
from root_app.shared.database import SessionLocal

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
        self.page = page
        self.calendario = calendario()
        self.cor_conteiner = '#696969'
        self.cor_do_botao = '#800000'
        self.dados_autenticados = dados_de_acesso_autorizado
        self.pesquisas = Pesquisas(self.page)
        self.abas = AbaFather(self.page)

        self.conteiner_autenticacao = Container(
            bgcolor=self.cor_conteiner,
            width=500,
            height=300,
            border_radius=15,
            padding=padding.only(right=20, left=20, bottom=20),
        )

        self.conteiner_pesquisa = Container(
            bgcolor=self.cor_conteiner,
            width=500,
            height=300,
            border_radius=15,
            padding=padding.only(right=20, left=20, bottom=10),
        )

        self.coluna_scroll = Column(
            scroll=ScrollMode.ALWAYS,
            auto_scroll=True,
            spacing=5,
            alignment=MainAxisAlignment.CENTER
        )
        self.imagem_svg_no_data = ler_imagem(r'assets\imagem_no_data')
        self.campo_data = None
        self.conteiner_lista_clientes = None
        self.data_seguinte = None
        self.data_anterior = None
        self.barra_de_carregamento = None
        self.avisos_adicionais = None
        self.lista_convenio = None
        self.botao_busca = None
        self.formulario_cpf = None

        self.page.overlay.append(self.calendario)
        self.calendario.on_change = self.change_date
        self.adiciona_elemento(datetime.today())



    def botao_selecionado(self, botao: ControlEvent):
        botao_string = str(botao.control)[10:]
        botao_dicionario = ast.literal_eval(botao_string)
        buscar_selecionado(botao_dicionario['key'])
        self.page.go('/cliente')

    def deletar_consulta(self, botao: ControlEvent):
        botao_string = str(botao.control)[10:]
        botao_dicionario = ast.literal_eval(botao_string)
        deletar_consulta(botao_dicionario['key'])
        self.adiciona_elemento(self.calendario.value)
        self.update()

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
                                            Text(value=f'Margem cartão: {cliente.margem_cartao}')
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
                                                            Text('Del Cons', size=10)
                                                        ],
                                                        spacing=1,
                                                        alignment=MainAxisAlignment.CENTER,
                                                        key=str(cliente.id_consulta)
                                                    ),
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
        self.conteiner_autenticacao.content = self.abas
        self.conteiner_pesquisa.content = self.pesquisas

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
                    self.conteiner_pesquisa,
                    self.conteiner_autenticacao
                ]),
                Column([
                    conteiner_titulo_cliente,
                    self.conteiner_lista_clientes
                ])
            ]
        )
