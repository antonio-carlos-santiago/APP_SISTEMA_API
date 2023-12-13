from flet import *

from root_app.configuracoes.login.funcoes import ler_imagem, efetua_login
from root_app.pages import dados_de_acesso_autorizado


class Login(UserControl):

    def __init__(self, page):
        super().__init__()
        self.imagem_svc_login = ler_imagem(r'root_app\imagens\imagem_login')
        self.botao_login = None
        self.formulario_senha = None
        self.formulario_login = None
        self.page = page

    def solicitacao_login(self, e):
        retorno = efetua_login(self.formulario_login.value, self.formulario_senha.value)
        if retorno['status']:
            dados_de_acesso_autorizado['vencimento'] = retorno['vencimento']
            dados_de_acesso_autorizado['nome'] = retorno['nome']
            dados_de_acesso_autorizado['nome_escritorio'] = retorno['nome_escritorio']
            dados_de_acesso_autorizado['cpfoucnpf'] = retorno['cpfoucnpf']
            dados_de_acesso_autorizado['telefone'] = retorno['telefone']
            dados_de_acesso_autorizado['email'] = retorno['email']
            dados_de_acesso_autorizado['data_atual'] = retorno['data_atual']
            dados_de_acesso_autorizado['link_foto_perfil'] = retorno['link_foto_perfil']
            self.page.go('/new_home')
        else:
            self.formulario_senha.error_text = retorno['info']
            self.update()

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
            can_reveal_password=True,
            error_style=TextStyle(color='black')
        )

        self.botao_login = ElevatedButton(
            icon=icons.LOGIN,
            text='LOGIN',
            bgcolor='#FF7F50',
            width=200,
            height=50,
            elevation=10,
            on_click=self.solicitacao_login
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

        conteiner_imagem = Container(
            width=480,
            height=480,
            content=Image(src=self.imagem_svc_login),
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
