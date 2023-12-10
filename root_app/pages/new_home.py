from datetime import datetime, timedelta

from flet import *

from root_app.configuracoes.home.models import Consulta
from root_app.shared.database import SessionLocal

session = SessionLocal()


def calendario():
    date_picker = DatePicker(
        first_date=datetime(2023, 10, 1),
        last_date=datetime(2024, 10, 1),
        value=datetime.today()
    )
    return date_picker


class NewHome(UserControl):

    def __init__(self, page):
        super().__init__()
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
            filled=True
        )
        self.lista_convenio = Dropdown(
            options=[dropdown.Option('Selecione o Convenio'), dropdown.Option('AMAZONPREV')],
            prefix_icon=icons.LIST,
            width=300,
            value='Selecione o Convenio',
            alignment=alignment.center,
            filled=True,
            border_color='white',
            border_radius=10
        )
        self.botao_busca = ElevatedButton(
            icon=icons.FIND_IN_PAGE,
            text='BUSCAR',
            width=200,
            height=40,
            elevation=10,
            bgcolor=self.cor_do_botao,
            color='white'
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
                            alignment=MainAxisAlignment.CENTER)
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

                    Divider(height=9, thickness=3),
                    Row([
                        Column([ElevatedButton(text='Checar Sessoes',
                                               bgcolor=self.cor_do_botao,
                                               icon=icons.CHECK,
                                               color='white')],
                               alignment=MainAxisAlignment.CENTER
                               ),

                        # aqui vai ficar o conteiner com as sessoes ativas
                    ])
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
                                                            IconButton(icon=icons.LIST_SHARP, icon_size=25),
                                                            Text('Detalhes', size=10)
                                                        ],
                                                        spacing=1,
                                                        alignment=MainAxisAlignment.CENTER,
                                                        key=str(cliente.id_consulta)
                                                    ),
                                                    Column(
                                                        controls=[
                                                            IconButton(icon=icons.DELETE_SHARP, icon_size=25),
                                                            Text('Del Cons', size=10)
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
                            )
                            ,

                        )
                    ])
                self.coluna_scroll.controls.append(linha)
        else:
            pass
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
            height=400,
            border_radius=15,
            padding=padding.only(right=20, left=20, bottom=10),
            content=self.elementos_pesquisa()

        )

        conteiner_autenticacao = Container(
            bgcolor=self.cor_conteiner,
            width=500,
            height=200,
            border_radius=15,
            padding=padding.only(top=80, right=20, left=20, bottom=20)
        )

        conteiner_titulo_cliente = Container(
            bgcolor=self.cor_conteiner,
            width=500,
            height=50,
            border_radius=15,
            padding=padding.only(top=5, right=80, left=80, bottom=5),
            content=self.elementos_titulo_cliente()
        )
        self.coluna_scroll = Column(
            scroll=ScrollMode.ALWAYS,
            auto_scroll=True,
            spacing=5,
            alignment=MainAxisAlignment.CENTER
        )

        self.conteiner_lista_clientes = Container(
            bgcolor=self.cor_conteiner,
            width=500,
            height=550,
            border_radius=15,
            padding=padding.only(top=20, right=20, left=20, bottom=20),
            content=self.coluna_scroll

        )
        return Row([
            Column([
                conteiner_pesquisa,
                conteiner_autenticacao
            ]),
            Column([
                conteiner_titulo_cliente,
                self.conteiner_lista_clientes
            ])

        ])
