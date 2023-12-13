from datetime import datetime

import flet as ft
from flet import *


from root_app.configuracoes.login.funcoes import ler_imagem
dados_teste = {'vencimento': '2023-12-31', 'nome': 'antonio carlos santiago', 'nome_escritorio': 'iconnect', 'cpfoucnpf': 5303617360, 'telefone': '92984404584', 'email': 'carlos.santiago013@gmail.com', 'data_atual': '2023-12-13', 'link_foto_perfil': 'https://media-gru1-1.cdn.whatsapp.net/v/t61.24694-24/408285891_1733168760517763_5499078028534220565_n.jpg?ccb=11-4&oh=01_AdToDGA8UlT7OLf25ILvC-G1-JPBffJQNu3DIQpteZlqAQ&oe=6586D497&_nc_sid=e6ed6c&_nc_cat=109'}


def main(page: Page):
    data_vencimento = datetime.strptime(dados_teste["vencimento"], "%Y-%m-%d")
    data_atual = datetime.strptime(dados_teste["data_atual"], "%Y-%m-%d")
    vencimento = data_vencimento - data_atual
    teste = Container(
        width=500,
        height=250,
        border_radius=10,
        bgcolor='red',
        padding=padding.only(top=20, left=20, right=20),
        content=Column(
            controls=[
                Row(
                    # alignment=MainAxisAlignment.START,
                    controls=[
                        CircleAvatar(foreground_image_url=dados_teste['link_foto_perfil'], width=50, height=50),
                        Column(
                            controls=[
                                Text(value=f'Nome: {dados_teste["nome"].title()}'),
                                Text(value=f"Empresa: {dados_teste['nome_escritorio'].title()}")
                            ]
                        ),
                    ]
                ),
                Divider(),
                Text(value=f"Valído até: {data_vencimento.strftime('%d/%m/%Y')}"),
                Text(value=f"Dias Restante: {vencimento.days} dias"),
                Text(value=f"Email: {dados_teste['email']}"),
                Text(value=f"Telefone: {dados_teste['telefone']}")

            ]
        )
    )




    page.add(
        teste
    )


ft.app(target=main)
