from flet import *

from root_app import Selecionado, Consulta
from root_app.shared.database import SessionLocal

cor_conteiner = '#696969'
cor_do_botao = '#800000'
sessao = SessionLocal()


def buscar_cliente_cc():
    cliente_id = sessao.query(Selecionado).first()
    if cliente_id:
        dados_consula = sessao.query(Consulta).filter_by(id_consulta=cliente_id.id_selecionado_cliente).first()
        return dados_consula


def titulo_contracheque(pagina):
    cliente = buscar_cliente_cc()
    return Container(
        padding=padding.only(left=50, right=50),
        bgcolor=cor_conteiner,
        width=800,
        height=60,
        border_radius=10,
        content=Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                IconButton(
                    icon=icons.KEYBOARD_RETURN_SHARP,
                    icon_size=30,
                    on_click=lambda _: pagina.go('/new_home'),
                    bgcolor=cor_do_botao
                ),
                Text(
                    value=f'{cliente.nome}',
                    size=20
                ),
                Text(
                    value=f'{cliente.mes_referencia}',
                    size=20
                ),
                IconButton(
                    icon=icons.DOWNLOAD,
                    icon_size=30,
                    bgcolor=cor_do_botao,
                )
            ]
        )
    )


def corpo_contracheque():
    pass
