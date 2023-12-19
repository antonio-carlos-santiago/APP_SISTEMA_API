from datetime import datetime

from flet import *

from root_app.configuracoes.contracheques.funcoes import consulta
from root_app.pages import dados_de_acesso_autorizado


def checkout():
    try:
        return datetime.strptime(dados_de_acesso_autorizado['data_atual'], "%Y-%m-%d")
    finally:
        return datetime.now()


class ContraCheque(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.data_atual = checkout()
        self.formulario_cpf = TextField(
            hint_text='Insira o CPF',
            prefix_icon=icons.NUMBERS,
            border_color='white',
            input_filter=NumbersOnlyInputFilter(),
            cursor_color='black',
            max_length=11,
            width=300,
            height=80,
            text_size=20,
            text_align=TextAlign.CENTER,
            autofocus=True,
            counter_style=TextStyle(color='black'),
            border_radius=10,
            filled=True,
            on_change=self.limpa_avisos
        )
        self.formulario_mes = Dropdown(
            prefix_icon=icons.CALENDAR_MONTH,
            height=50,
            width=145,
            value=f"{self.data_atual.month}",
            alignment=alignment.center,
            filled=True,
            border_color='white',
            border_radius=10,
            options=[dropdown.Option(f'{mes}') for mes in range(1, 13)],
            text_size=15,
            hint_text='Mes',
            label="Mes",
            on_change=self.limpa_avisos
        )
        self.formulario_ano = Dropdown(
            prefix_icon=icons.CALENDAR_MONTH,
            width=145,
            height=50,
            value=f"{self.data_atual.year}",
            alignment=alignment.center,
            filled=True,
            border_color='white',
            border_radius=10,
            text_size=15,
            hint_text='Ano',
            options=[dropdown.Option(f'202{ano}') for ano in range(2, 6)],
            label="Ano",
            on_change=self.limpa_avisos

        )
        self.notificacoes = Text()

        self.botao_solicita_emissao = ElevatedButton(
            text="Emitir Contra-cheque",
            height=40,
        )

    def emitir_cc(self, e):
        self.botao_solicita_emissao.disabled = True
        self.update()
        while len(self.formulario_cpf.value) != 11:
            self.formulario_cpf.value = f'0{self.formulario_cpf.value}'
        status = consulta(
            self.formulario_cpf.value,
            self.formulario_mes.value,
            self.formulario_ano.value
        )
        if not status:
            self.notificacoes.value = 'Verifique o CPF, algo deu errado'
        self.botao_solicita_emissao.disabled = False
        self.update()

    def limpa_avisos(self, e):
        self.notificacoes.value = ''
        self.update()

    def build(self):
        self.botao_solicita_emissao.on_click = self.emitir_cc
        return Container(
            on_hover=self.limpa_avisos,
            width=460,
            height=230,
            padding=padding.only(top=10, left=10, right=10),
            content=Column(
                controls=[
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.formulario_cpf
                        ]
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.formulario_mes,
                            self.formulario_ano
                        ]
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.notificacoes
                        ]
                    ),
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.botao_solicita_emissao
                        ]
                    ),
                ]
            )
        )
