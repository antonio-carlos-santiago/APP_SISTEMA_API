from flet import *

from root_app.configuracoes.contracheques.elementos import titulo_contracheque


class ContraCheque(UserControl):

    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        return titulo_contracheque(self.page)
