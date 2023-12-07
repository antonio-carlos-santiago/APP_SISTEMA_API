import ast

from flet import *


class Cliente(UserControl):

    def __init__(self, page):
        super().__init__()
        self.page = page

    def eventosbar(self, e: ControlEvent):
        botao_string = str(e.control)[13:]
        botao_dicionario = ast.literal_eval(botao_string)
        if int(botao_dicionario['selectedindex']) == 0:
            self.page.go('/home')

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
            border_radius=10
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
