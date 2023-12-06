from flet import *


class Cliente(UserControl):

    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def teste(e):
            if text.value == 'confia':
                self.page.go('/home')
            else:
                text.error_text = 'Tente outra vez'
                self.update()

        text = TextField(
            hint_text='Insira o CPF',
            width=200,
            height=50,
        )

        botao = ElevatedButton(
            text='teste', on_click=teste
        )
        return Container(
            bgcolor='blue',
            width=500,
            height=500,
            content=Row([
                text,
                botao
            ]
            )
        )
