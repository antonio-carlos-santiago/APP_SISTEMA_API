from flet import *


class Detalhes(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        return Container(
            bgcolor='green',
            width=200,
            height=200
        )
