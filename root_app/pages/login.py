from flet import *


class Login(UserControl):

    def __init__(self, page):
        super().__init__()

        self.page = page

    def build(self):


        return Container(
            bgcolor='red',
            width=500,
            height=500,
            on_click=lambda _: self.page.go('/home')
        )
