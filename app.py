from flet import *

from view import views_handler


def main(page: Page):
    page.window_resizable = False
    page.window_maximizable = False

    page.update()

    def router_change(e):
        page.views.clear()
        page.views.append(
            views_handler(page)[page.route]
        )
        if page.route == '/login':
            page.title = 'Login'
            page.window_width = 1005
            page.window_height = 560

        elif page.route == '/new_home':
            page.window_width = 1045
            page.window_height = 670
            page.title = 'New Home'
            page.theme_mode = ThemeMode.DARK

        elif page.route == '/cliente':
            page.window_width = 1020
            page.window_height = 760
            page.theme_mode = ThemeMode.DARK
            page.title = 'Cliente'

        elif page.route == '/detalhes':
            page.window_width = 1050
            page.window_height = 760
            page.theme_mode = ThemeMode.DARK
            page.title = 'Detalhes'

    page.on_route_change = router_change
    page.go('/new_home')


app(target=main, assets_dir='assets')
