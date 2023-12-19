from datetime import datetime

from flet import *

from root_app.pages import dados_de_acesso_autorizado


class Perfil(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.dados_autenticados = dados_de_acesso_autorizado
        self.nome = Text()
        self.foto_perfil = CircleAvatar(
            width=50,
            height=50
        )
        self.empresa = Text()
        self.validade = Text()
        self.vencimento = Text()
        self.email = Text()
        self.telefone = Text()

    def build(self):
        if self.dados_autenticados:
            data_vencimento = datetime.strptime(self.dados_autenticados["vencimento"], "%Y-%m-%d")
            data_atual = datetime.strptime(self.dados_autenticados["data_atual"], "%Y-%m-%d")
            vencimento = data_vencimento - data_atual
            self.nome.value = f'Nome: {self.dados_autenticados["nome"]}'
            self.foto_perfil.foreground_image_url = self.dados_autenticados["link_foto_perfil"],
            self.empresa.value = f"Empresa: {self.dados_autenticados['nome_escritorio']}"
            self.email.value = f"Email: {self.dados_autenticados['email']}"
            self.telefone.value = f"Telefone: {self.dados_autenticados['telefone']}"
            self.validade.value = f"Valído até: {data_vencimento.strftime('%d/%m/%Y')}"
            self.vencimento.value = f"Dias Restante: {vencimento.days} dias"

        return Column(
            controls=[
                Container(
                    height=10,
                    width=10
                ),
                Row(
                    controls=[
                        self.foto_perfil,
                        Column(
                            controls=[
                                self.nome,
                                self.empresa
                            ]
                        ),
                    ]
                ),
                Divider(),
                self.validade,
                self.vencimento,
                self.email,
                self.telefone
            ]
        )


