import ast

from flet import *

from root_app.configuracoes.cliente.funcoes import *


class Cliente(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.dados_cliente = buscar_cliente()

    def eventosbar(self, e: ControlEvent):
        botao_string = str(e.control)[13:]
        botao_dicionario = ast.literal_eval(botao_string)
        if int(botao_dicionario['selectedindex']) == 0:
            self.page.go('/home')
        elif int(botao_dicionario['selectedindex']) == 1:
            pass

    def copia_dados(self, objeto: ControlEvent):
        print(objeto.__dict__)
        self.update()

    def elementos_dados_cliente(self):
        dados_cliente = Column([
            Container(
                key=str(self.dados_cliente.nome),
                content=Row([Text(value=f"Nome: {self.dados_cliente.nome}"),
                             IconButton(icon=icons.COPY, icon_size=20)]),
                on_click=self.copia_dados,
                width=320
            ),
            Container(
                key=str(self.dados_cliente.cpf),
                content=Row([Text(value=f"CPF: {self.dados_cliente.cpf}"),
                             IconButton(icon=icons.COPY, icon_size=20)]),
                on_click=self.copia_dados,
                width=320
            ),
            Container(
                key=str(self.dados_cliente.matricula),
                content=Row([Text(value=f"Matricula: {self.dados_cliente.matricula}"),
                             IconButton(icon=icons.COPY, icon_size=20)]),
                on_click=self.copia_dados,
                width=320
            ),
            Container(
                key=str(self.dados_cliente.convenio),
                content=Row([Text(value=f"Convenio: {self.dados_cliente.convenio}"),
                             IconButton(icon=icons.COPY,
                                        icon_size=20)]),
                on_click=self.copia_dados,
                width=320,
            ),
        ])

        dados_margens = Column([
            Container(
                key=str(self.dados_cliente.margem_emprestimo),
                content=Row([Text(value=f"Margem Emprestimo:    {self.dados_cliente.margem_emprestimo}"),
                             IconButton(icon=icons.COPY, icon_size=20)]),
                on_click=self.copia_dados,
                width=320
            ),
            Container(
                key=str(self.dados_cliente.margem_cartao),
                content=Row([Text(value=f"Margem Cartão:    {self.dados_cliente.margem_cartao}"),
                             IconButton(icon=icons.COPY, icon_size=20)]),
                on_click=self.copia_dados,
                width=320
            ),
            Container(
                key=str(self.dados_cliente.mes_referencia),
                content=Row([Text(value=f"Mês Referencia:    {self.dados_cliente.mes_referencia}"),
                             IconButton(icon=icons.COPY, icon_size=20)]),
                on_click=self.copia_dados,
                width=320
            ),
            Container(
                key=str(self.dados_cliente.data_consulta),
                content=Row([Text(value=f"Data Consulta:    {self.dados_cliente.data_consulta}"),
                             IconButton(icon=icons.COPY,
                                        icon_size=20)]),
                on_click=self.copia_dados,
                width=320,
            ),
        ])


        return Row([
            dados_cliente,
            dados_margens
        ],
        alignment=MainAxisAlignment.SPACE_AROUND)

    def build(self):
        navigation_bar = NavigationBar(
            height=80,
            destinations=[
                NavigationDestination(icon=icons.ARROW_BACK, label="Voltar"),
                NavigationDestination(icon=icons.FIND_IN_PAGE, label="Analise Automatica")
            ],
            on_change=self.eventosbar,
        )

        conteiner_dados = Container(
            bgcolor='#363636',
            width=800,
            height=200,
            border_radius=10,
            content=self.elementos_dados_cliente(),
            padding=padding.only(right=20, left=20, top=5)
        )

        conteiner_emprestimos = Container(
            bgcolor='#363636',
            width=800,
            height=400,
            border_radius=10
        )

        return Column(
            [
                navigation_bar,
                conteiner_dados,
                Container(
                    bgcolor='#363636',
                    width=800,
                    height=30,
                    border_radius=10
                ),
                conteiner_emprestimos,
            ]
        )
