from flet import *

from root_app.pages.detalhes import Detalhes
from root_app.pages.login import Login
from root_app.pages.cliente import Cliente
from root_app.pages.new_home import NewHome
from root_app.pages.contracheque import ContraCheque


def views_handler(page):
    return {
        '/login': View(
            route='/login',
            controls=[
                Login(page)
            ]
        ),
        '/cliente': View(
            route='/cliente',
            controls=[
                Cliente(page)
            ]
        ),
        '/detalhes': View(
          route='/detalhes',
            controls=[
                Detalhes(page)
            ]
        ),
        '/new_home': View(
            route='/new_home',
            controls=[
                NewHome(page)
            ]
        ),
        '/contracheque': View(
            route='/contracheque',
            controls=[
                ContraCheque(page)
            ]
        )
    }
