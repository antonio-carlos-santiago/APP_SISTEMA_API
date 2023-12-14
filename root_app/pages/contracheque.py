from flet import *

from root_app.pages import cliente_contra_cheque_selecionado


class ContraCheque(UserControl):

    def __init__(self, page):
        super().__init__()

        self.page = page

    def build(self):
        self.page.window_height = 2000
        self.page.window_width = 200
        return Container(
            bgcolor='red',
            width=200,
            height=200,
            content=Row([
                Text(
                    value=f'{cliente_contra_cheque_selecionado["cliente"].nome}'
                )
            ])
        )

