import base64
from datetime import datetime

from flet import *

from root_app import Selecionado, Consulta, Contracheque
from root_app.configuracoes.contracheques.funcoes import consulta
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
    contra_cheques_salvos = sessao.query(Contracheque).filter_by(cpf=cliente.cpf).all()
    if cliente.convenio == "AMAZONPREV":
        conteudo = Container(
            bgcolor='red',
            content=Text(
                value="Esse cliente não possui função de contracheque ainda",
            )
        )
    else:
        data_referencia_formatada = datetime.strptime(cliente.mes_referencia, "%m/%Y")
        if contra_cheques_salvos:
            for item in contra_cheques_salvos:
                print(type(item.imagem_contracheque))
                imagem = item.imagem_contracheque
                conteudo = Image(
                    src_base64=imagem,
                    width=500,
                    height=500
                )

        else:
            consulta(cliente.cpf, data_referencia_formatada.month, data_referencia_formatada.year)
            conteudo = Text(value='Vai tomar no cu caralho, vai emitir contrachque no inferno')

    data_referencia = Text(value=f'{cliente.mes_referencia}', size=20)
    return Column(
        controls=[
            Container(
                padding=padding.only(left=50, right=50),
                bgcolor=cor_conteiner,
                width=800,
                height=60,
                border_radius=10,
                content=Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        IconButton(
                            icon=icons.ARROW_BACK,
                            icon_size=30,
                            on_click=lambda _: pagina.go('/new_home'),
                            bgcolor=cor_do_botao,

                        ),
                        Text(
                            value=f'{cliente.nome[:20]}',
                            size=20
                        ),
                        Container(
                            content=Row(
                                controls=[
                                    IconButton(
                                        icon=icons.ARROW_LEFT,
                                        icon_size=30,
                                        bgcolor=cor_do_botao
                                    ),
                                    Container(
                                        bgcolor=cor_do_botao,
                                        width=100,
                                        height=45,
                                        border_radius=10,
                                        content=Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                data_referencia,
                                            ]
                                        )
                                    ),
                                    IconButton(
                                        icon=icons.ARROW_RIGHT,
                                        icon_size=30,
                                        bgcolor=cor_do_botao
                                    ),

                                ]
                            )
                        ),
                        IconButton(
                            icon=icons.DOWNLOAD,
                            icon_size=30,
                            bgcolor=cor_do_botao,
                        ),

                    ]
                )
            ),
            corpo_contracheque(conteudo)
        ]
    )


def corpo_contracheque(contra_cheques):
    coluna_scroll = Column(
        scroll=ScrollMode.ALWAYS,
        height=610,
        width=780,
        controls=[
            contra_cheques
        ]
    )
    return Container(
        padding=padding.only(left=10, right=10, top=10, bottom=10),
        bgcolor=cor_conteiner,
        width=800,
        height=630,
        border_radius=10,
        content=coluna_scroll
    )


"""
Rascunho patra me nao esquecer, a tabela de contracheque ja foi criada, agora qu tenho que fazer a logica
 de visualização
"""
