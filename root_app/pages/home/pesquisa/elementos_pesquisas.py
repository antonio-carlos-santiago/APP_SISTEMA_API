from datetime import datetime

from flet import *

from root_app.configuracoes.home.funcoes import valida_cpf, consultar_margem, salvar_dados_retornados
from root_app.pages import dados_de_acesso_autorizado


class Pesquisas(UserControl):
    def __init__(self, page):
        super().__init__()
        self.acesso_autorizado = dados_de_acesso_autorizado
        self.cor_conteiner = '#696969'
        self.cor_do_botao = '#800000'
        self.page = page
        self.formulario_cpf = TextField(
            hint_text='Insira o CPF',
            prefix_icon=icons.NUMBERS,
            border_color='white',
            input_filter=NumbersOnlyInputFilter(),
            cursor_color='black',
            max_length=11,
            width=300,
            text_size=20,
            text_align=TextAlign.CENTER,
            autofocus=True,
            counter_style=TextStyle(color='black'),
            border_radius=10,
            filled=True
        )

        self.lista_convenio = Dropdown(
            prefix_icon=icons.LIST,
            width=300,
            value='Selecione o Convenio',
            alignment=alignment.center,
            filled=True,
            border_color='white',
            border_radius=10,
            options=[
                dropdown.Option('Selecione o Convenio'),
                dropdown.Option('AMAZONPREV'),
                dropdown.Option('MANAUS'),
                dropdown.Option('PREFEITURA')
            ],

        )

        self.botao_busca = ElevatedButton(
            icon=icons.FIND_IN_PAGE,
            text='BUSCAR',
            width=200,
            height=40,
            elevation=10,
            bgcolor=self.cor_do_botao,
            color='white',

        )

        self.barra_de_carregamento = Row(
            visible=False,
            controls=[
                Icon(
                    name=icons.FIND_IN_PAGE
                ),
                ProgressBar(
                    color="#8B0000",
                    bgcolor="#778899",
                    width=420,
                    height=20
                )
            ],
        )

        self.avisos_adicionais = Text(
            value='Consulta Realizada com Sucesso!!',
            visible=False,
            text_align=TextAlign.CENTER,
            width=460,
            size=15,
            color='white'
        )

    def trata_erros(self, e):
        self.avisos_adicionais.visible = False
        self.formulario_cpf.error_text = None
        self.lista_convenio.error_text = None
        self.update()

    def buscar_margem(self, e):
        data_vencimento = datetime.strptime(self.acesso_autorizado['vencimento'], "%Y-%m-%d")
        data_servidor = datetime.strptime(self.acesso_autorizado['data_atual'], "%Y-%m-%d")
        if data_vencimento >= data_servidor:
            cpf = valida_cpf(self.formulario_cpf.value)
            if self.lista_convenio.value == 'Selecione o Convenio':
                self.lista_convenio.error_text = 'Verifique o convenio'
                self.update()
            elif not cpf:
                self.formulario_cpf.error_text = 'Verifique o CPF'
                self.update()
            else:

                self.barra_de_carregamento.visible = True
                self.botao_busca.visible = False
                self.update()
                resultado = consultar_margem(cpf, self.lista_convenio.value)
                if 'status' in resultado:
                    if not resultado['status']:
                        self.avisos_adicionais.value = resultado['info']
                        self.barra_de_carregamento.visible = False
                        self.avisos_adicionais.visible = True
                        self.botao_busca.visible = True
                        self.update()
                else:
                    salvar_dados_retornados(resultado)
                    self.avisos_adicionais.value = 'Cliente consultado'
                    self.barra_de_carregamento.visible = False
                    self.avisos_adicionais.visible = True
                    self.botao_busca.visible = True
                    self.update()
        else:
            self.avisos_adicionais.value = "Usuario com pendencias"
            self.avisos_adicionais.visible = True
            self.update()

    def build(self):
        self.botao_busca.on_click = self.buscar_margem
        self.formulario_cpf.on_change = self.trata_erros
        self.lista_convenio.on_change = self.trata_erros
        return Column(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        self.formulario_cpf,
                    ],
                ),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        self.lista_convenio,
                    ],
                ),
                Container(
                    alignment=alignment.center,
                    width=20,
                    height=30,
                    content=Column(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Row(
                                controls=[
                                    self.avisos_adicionais
                                ]
                            ),
                            Row(
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    self.barra_de_carregamento
                                ]
                            ),
                        ],
                    ),
                ),
                Column(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Row(
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                self.botao_busca
                            ]
                        )
                    ]
                )
            ]
        )
