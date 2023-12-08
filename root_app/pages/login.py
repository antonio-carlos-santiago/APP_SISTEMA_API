from flet import *

from root_app.configuracoes.login.funcoes import ler_imagem


class Login(UserControl):

    def __init__(self, page):
        super().__init__()
        self.botao_login = None
        self.formulario_senha = None
        self.formulario_login = None
        self.page = page

    def elementos_login(self):
        self.formulario_login = TextField(
            border=InputBorder.NONE,
            hint_text='Insira seu E-mail',
            prefix_icon=icons.EMAIL,
            bgcolor='#FA8072',
            border_color='#FF6347',
            capitalization=TextCapitalization.CHARACTERS,
            cursor_color='black'
        )

        self.formulario_senha = TextField(
            border=InputBorder.NONE,
            hint_text='Insira sua senha',
            prefix_icon=icons.PASSWORD,
            bgcolor='#FA8072',
            border_color='#FF6347',
            cursor_color='black',
            password=True,
            can_reveal_password=True
        )

        self.botao_login = ElevatedButton(
            icon=icons.LOGIN,
            text='LOGIN',
            bgcolor='#FF7F50',
            width=200,
            height=50,
            elevation=10,
            on_click=lambda _: self.page.go('/home')
        )
        elementos = Column(
            [
                Text(
                    value='Login',
                    size=30,
                    color='white',
                    style=TextThemeStyle.TITLE_LARGE,
                    font_family="Kanit"
                ),
                Container(
                    height=60
                ),
                self.formulario_login,
                self.formulario_senha,
                Column([
                    Container(height=20, width=20),
                    Row([
                        self.botao_login
                    ],
                        alignment=MainAxisAlignment.CENTER)

                ],
                    alignment=MainAxisAlignment.CENTER)

            ]
        )
        return elementos

    def build(self):
        imagem_svc = ler_imagem(r'root_app\imagens\imagem_login'),
        conteiner_imagem = Container(
            width=480,
            height=480,
            content=Image(src=imagem_svc),
        )

        conteiner_formulario = Container(
            bgcolor='#8B0000',
            width=480,
            height=500,
            border_radius=10,
            padding=padding.only(top=80, right=60, left=60, bottom=30),
            content=self.elementos_login()
        )
        return Row([
            conteiner_imagem,
            conteiner_formulario
        ])
