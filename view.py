from flet import *

from root_app.pages.detalhes import Detalhes
from root_app.pages.home import Home
from root_app.pages.login import Login
from root_app.pages.cliente import Cliente


def views_handler(page):
    return {
        '/home': View(
            route='/home',
            controls=[
                Home(page)
            ]
        ),
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
    }
