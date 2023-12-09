from flet import *


class NewHome(UserControl):

    def __init__(self, page):
        super().__init__()
        self.barra_de_carregamento = None
        self.avisos_adicionais = None
        self.lista_convenio = None
        self.botao_busca = None
        self.formulario_cpf = None
        self.page = page

    def elementos_pesquisa(self):
        self.formulario_cpf = TextField(
            hint_text='Insira o CPF',
            prefix_icon=icons.FIND_IN_PAGE,
            bgcolor='#FA8072',
            border_color='black',
            input_filter=NumbersOnlyInputFilter(),
            cursor_color='black',
            max_length=11,
            width=300,
            text_size=20,
            text_align=TextAlign.CENTER,
            autofocus=True,
            counter_style=TextStyle(color='black'),
            border_radius=10
        )
        self.lista_convenio = Dropdown(
            options=[dropdown.Option('Selecione o Convenio'), dropdown.Option('AMAZONPREV')],
            prefix_icon=icons.LIST,
            bgcolor='#FA8072',
            width=300,
            value='Selecione o Convenio',
            alignment=alignment.center,
            filled=True,
            border_color='black',
            border_radius=10
        )
        self.botao_busca = ElevatedButton(
            icon=icons.CHECK,
            text='BUSCAR',
            bgcolor='#FF7F50',
            width=200,
            height=50,
            elevation=10,
            color='black',
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
                        Column([ElevatedButton(text='Checar Sessoes Ativas')],
                               alignment=MainAxisAlignment.CENTER
                               ),

                        # aqui vai ficar o conteiner com as sessoes ativas
                    ])
                ],
                    alignment=MainAxisAlignment.CENTER)

            ], alignment=MainAxisAlignment.CENTER
        )
        return elementos

    def build(self):
        conteiner_pesquisa = Container(
            bgcolor='#A52A2A',
            width=500,
            height=400,
            border_radius=15,
            padding=padding.only(top=40, right=20, left=20, bottom=20),
            content=self.elementos_pesquisa()

        )

        conteiner_autenticacao = Container(
            bgcolor='#A52A2A',
            width=500,
            height=200,
            border_radius=15,
            padding=padding.only(top=80, right=20, left=20, bottom=20)
        )

        conteiner_lista_clientes = Container(
            bgcolor='#A52A2A',
            width=500,
            height=610,
            border_radius=15,
            padding=padding.only(top=20, right=20, left=20, bottom=20),

        )
        return Row([
            Column([
                conteiner_pesquisa,
                conteiner_autenticacao
            ]),
            conteiner_lista_clientes
        ])
