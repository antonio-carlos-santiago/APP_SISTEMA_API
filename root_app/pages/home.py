from root_app.configuracoes.home.funcoes import *
from flet import *
import ast

convenios = listar_convenios()
lista_de_funcoes = verifica_sessoes(convenios)
elementos = Column(lista_de_funcoes, alignment=MainAxisAlignment.CENTER)


class Home(UserControl):

    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def buscar_margem(e):
            cpf = valida_cpf(campo_de_texto.value)
            if not lista_de_convenios.value in convenios:
                lista_de_convenios.error_text = 'Verifique o convenio'
                self.update()
            elif not cpf:
                campo_de_texto.error_text = 'Verifique o CPF'
                self.update()
            else:
                resultado = consultar_margem(cpf, lista_de_convenios.value)
                if 'status' in resultado:
                    if not resultado['status']:
                        mensagens_de_avisos.value = resultado['info']
                        self.update()
                else:
                    salvar_dados_retornados(resultado)
                    mensagens_de_avisos.value = 'Cliente consultado'
                    self.update()

        def trata_erros(e):
            lista_de_convenios.error_text = None
            campo_de_texto.error_text = None
            mensagens_de_avisos.value = None
            self.update()

        def atualiza_lista_sessoes_pricipal(e):
            elementos.controls = verifica_sessoes(convenios)
            self.update()

        campo_de_texto = TextField(hint_text='Insira o CPF',
                                   max_length=11,
                                   text_align=TextAlign.CENTER,
                                   text_size=50,
                                   text_style=TextStyle(color='#7FFFD4'),
                                   hint_style=TextStyle(color='#00CED1'),
                                   border_color='#5F9EA0',
                                   input_filter=NumbersOnlyInputFilter(),
                                   autofocus=True,
                                   bgcolor='#2F4F4F',
                                   counter_style=TextStyle(color='#7FFFD4'),
                                   border_radius=15,
                                   on_submit=buscar_margem,
                                   on_change=trata_erros
                                   )
        todos_os_convenios = [dropdown.Option(convenio) for convenio in convenios]
        todos_os_convenios.insert(0, dropdown.Option('Selecione o Convenio'))

        lista_de_convenios = Dropdown(
            width=250, border_radius=15, value='Selecione o Convenio', options=todos_os_convenios,
            border_color='#5F9EA0', text_style=TextStyle(color='#7FFFD4'), alignment=Alignment(0, 0),
            on_change=trata_erros
        )

        btn_busca_dados = ElevatedButton(
            text="Buscar", width=150, height=50, icon=icons.FIND_IN_PAGE, on_click=buscar_margem
        )

        mensagens_de_avisos = Text(size=20)

        conteine_painel = Container(
            bgcolor='#363636',
            width=500,
            height=350,
            border_radius=10,
            content=Column(
                [
                    campo_de_texto,
                    Row([
                        lista_de_convenios,
                        btn_busca_dados
                    ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    Row([]),
                    Row(
                        [
                            mensagens_de_avisos
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=15
            ),
            padding=padding.only(top=50, right=30, left=30),
            on_click=trata_erros
        )

        conteine_de_autenticacao = Container(
            bgcolor='#363636',
            width=245,
            height=250,
            border_radius=10,
            content=Column([
                Row([
                    Text(' AUTENTICAÇÕES', color='green', font_family='bold'),
                    IconButton(icon=icons.REFRESH, icon_size=30, animate_rotation=True,
                               on_click=atualiza_lista_sessoes_pricipal)
                ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                ),
                elementos
            ]),
            padding=padding.only(top=15, right=15, left=15, bottom=15)
        )

        conteine_de_informacoes = Container(
            bgcolor='#363636',
            width=245,
            height=250,
            border_radius=10,
        )

        coluna_de_pesquisados = Column(
            spacing=10,
            height=200,
            width=float("inf"),
            scroll=ScrollMode.ALWAYS,
            alignment=MainAxisAlignment.CENTER,
            auto_scroll=True

        )

        def botao_selecionado(botao: ControlEvent):
            botao_string = str(botao.control)[9:]
            botao_dicionario = ast.literal_eval(botao_string)
            buscar_selecionado(botao_dicionario['key'])
            self.page.go('/cliente')



        def lista_de_consulta(e):
            coluna_de_pesquisados.controls.clear()
            todas_as_consultas = consultas_diarias_realizadas()
            if todas_as_consultas:
                for emprestimo in todas_as_consultas:
                    if emprestimo.data_consulta == datetime.utcnow().date():
                        matricula = emprestimo.matricula
                        cliente = Container(bgcolor='red', width=460, key=str(emprestimo.id_consulta), content=
                        Text(value=f'Cliente: {emprestimo.nome[:15]} Matricula: {matricula} CPF: {emprestimo.cpf}'),
                                            on_click=lambda matricula=matricula: botao_selecionado(matricula))
                        coluna_de_pesquisados.controls.append(cliente)
            self.update()

        container_de_titulo = Container(
            bgcolor='#363636',
            width=500,
            height=80,
            border_radius=10,
            content=Column(
                [
                    Row([Text(value="Consultas do dia", size=30)], alignment=MainAxisAlignment.CENTER)
                ],
            ),
            padding=padding.only(top=20, left=10, right=10,
                                 bottom=20),

        )

        container_de_dados = Container(
            bgcolor='#363636',
            width=500,
            height=520,
            border_radius=10,
            padding=padding.only(top=20, left=10,
                                 bottom=20),
            content=coluna_de_pesquisados,
            on_hover=lista_de_consulta,

        )

        return Column(
            [
                Row([
                    Column([
                        conteine_painel,
                        Row([
                            conteine_de_autenticacao, conteine_de_informacoes
                        ])
                    ]),
                    Column([
                        container_de_titulo, container_de_dados
                    ])
                ])
            ]
        )
