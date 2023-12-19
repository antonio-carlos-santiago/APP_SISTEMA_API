from flet import *

from root_app.pages.home.abas.autenticacao import Autenticacao
from root_app.pages.home.abas.contracheque import ContraCheque
from root_app.pages.home.abas.indefinido import Indefinido
from root_app.pages.home.abas.perfil import Perfil


class AbaFather(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.aba_autenticacao = Autenticacao(page)
        self.aba_contracheque = ContraCheque(page)
        self.aba_higienizar = Indefinido(page)
        self.aba_perfil = Perfil(page)
        self.aba_pagamentos = Indefinido(page)
        self.cor_do_botao = '#800000'
        self.tabs = Tabs(
            selected_index=0,
            animation_duration=300,
            width=500,
            height=600,
            label_color=self.cor_do_botao,
            indicator_border_radius=10
        )

    def build(self):
        self.tabs.tabs = [
            Tab(
                text="Autenticação",
                content=self.aba_autenticacao),
            Tab(
                text='Emitir CC',
                content=self.aba_contracheque
            ),
            Tab(
                text="Higielizar",
                content=self.aba_higienizar
            ),
            Tab(
                text='Perfil',
                content=self.aba_perfil
            ),
            Tab(
                text='Pagamentos',
                content=self.aba_pagamentos
            )
        ]

        return self.tabs

