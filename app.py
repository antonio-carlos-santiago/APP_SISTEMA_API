from flet import *

from view import views_handler


def main(page: Page):
    page.window_resizable = False
    page.window_maximizable = False
    page.update()

    def router_change(route):
        page.views.clear()
        page.views.append(
            views_handler(page)[page.route]
        )
        if page.route == '/login':
            page.title = 'Login'
            page.window_width = 1005
            page.window_height = 560

        # elif page.route == '/home':
        #     page.window_width = 1045
        #     page.window_height = 670
        #     page.title = 'Home'
        #     page.theme_mode = ThemeMode.DARK
        #     page.update()
        #
        # elif page.route == '/cliente':
        #     page.window_width = 1020
        #     page.window_height = 760
        #     page.theme_mode = ThemeMode.DARK
        #     page.title = 'Cliente'
        #     page.update()
        #
        # elif page.route == '/detalhes':
        #     page.window_width = 1050
        #     page.window_height = 760
        #     page.theme_mode = ThemeMode.DARK
        #     page.title = 'Detalhes'

    page.on_route_change = router_change
    page.go('/login')


app(target=main)
