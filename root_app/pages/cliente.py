import ast

from flet import *

from root_app.configuracoes.cliente.funcoes import *


class Cliente(UserControl):
    def __init__(self, page):
        super().__init__()
        self.radio = None
        self.conteiner_emprestimos = None
        self.page = page
        self.dados_cliente = buscar_cliente()

    def eventosbar(self, e: ControlEvent):
        botao_string = str(e.control)[13:]
        botao_dicionario = ast.literal_eval(botao_string)
        if int(botao_dicionario['selectedindex']) == 0:
            self.page.go('/new_home')
        elif int(botao_dicionario['selectedindex']) == 1:
            self.page.go('/detalhes')

    def copia_dados(self, objeto: ControlEvent):
        print(objeto.__dict__)
        self.update()

    def elementos_dados_cliente(self):
        self.radio = RadioGroup(
            on_change=self.elementos_linhas_emprestimo,
            content=Row([
                Radio(value='Emprestimo', label="Emprestimo"),
                Radio(value="Cartao", label='Cartao')
            ])
        )

        dados_cliente = Column([
            Container(
                key=str(self.dados_cliente.nome),
                content=Row([Text(value=f"Nome:    {self.dados_cliente.nome}"),
                             IconButton(icon=icons.COPY, icon_size=20)]),
                on_click=self.copia_dados,
                width=320
            ),
            Container(
                key=str(self.dados_cliente.cpf),
                content=Row([Text(value=f"CPF:    {self.dados_cliente.cpf}"),
                             IconButton(icon=icons.COPY, icon_size=20)]),
                on_click=self.copia_dados,
                width=320
            ),
            Container(
                key=str(self.dados_cliente.matricula),
                content=Row([Text(value=f"Matricula:    {self.dados_cliente.matricula}"),
                             IconButton(icon=icons.COPY, icon_size=20)]),
                on_click=self.copia_dados,
                width=320
            ),
            Container(
                key=str(self.dados_cliente.convenio),
                content=Row([Text(value=f"Convenio:    {self.dados_cliente.convenio}"),
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
                content=Row([Text('Exibir contratos: '), self.radio]),
                width=320,
            ),
        ])
        return Row([
            dados_cliente,
            dados_margens
        ],
            alignment=MainAxisAlignment.SPACE_AROUND
        )

    def elementos_linhas_emprestimo(self, e):
        if self.radio.value == "Emprestimo":
            busca = self.dados_cliente.emprestimos
        else:
            busca = self.dados_cliente.cartoes

        scrool = Column(
            height=500,
            width=1050,
            scroll=ScrollMode.ALWAYS,
        )

        linhas_de_emprestimos = []

        for emprestimo in busca:
            linhas_de_emprestimos.append(
                DataRow(
                    cells=[DataCell(Text(value=f'{emprestimo["ade"]}')),
                           DataCell(Text(value=f'{emprestimo["data_deferimento"]}')),
                           DataCell(Text(value=f'{emprestimo["servicos"]}')),
                           DataCell(Text(value=f'{emprestimo["consignataria"]}')),
                           DataCell(Text(value=f'{emprestimo["parcela_atual"]}')),
                           DataCell(Text(value=f'{emprestimo["parcela_total"]}')),
                           DataCell(Text(value=f'{emprestimo["valor"]}')),
                           DataCell(Text(value=f'{emprestimo["status"]}'))]
                )
            )

        lista_de_emprestimos = DataTable(
            columns=[
                DataColumn(Text('ADE')),
                DataColumn(Text('DEFERIMENTO')),
                DataColumn(Text('SERVIÇO')),
                DataColumn(Text('CONSIGNATARIA')),
                DataColumn(Text('ATUAL')),
                DataColumn(Text('TOTAL')),
                DataColumn(Text('VALOR')),
                DataColumn(Text('STATUS')),
            ],
            rows=linhas_de_emprestimos

        )
        scrool.controls.append(lista_de_emprestimos)
        self.conteiner_emprestimos.content = scrool
        self.update()

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
            width=1050,
            height=200,
            border_radius=10,
            content=self.elementos_dados_cliente(),
            padding=padding.only(right=20, left=20, top=5)
        )

        self.conteiner_emprestimos = Container(
            bgcolor='#363636',
            width=1050,
            height=400,
            border_radius=10,
            padding=padding.only(bottom=20),
            content=Row([Text('Selecione uma das opçoes acima para exibir os contratos', size=30)],
                        alignment=MainAxisAlignment.CENTER)
        )

        return Column(
            [
                navigation_bar,
                conteiner_dados,
                self.conteiner_emprestimos
            ]
        )
