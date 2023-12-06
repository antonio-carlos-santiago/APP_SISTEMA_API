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
        if page.route == '/home':
            page.title = 'Home'
            page.window_width = 1045
            page.window_height = 670
            page.theme_mode = ThemeMode.DARK


        elif page.route == '/login':
            page.window_width = 300
            page.title = 'Login'
            page.update()

        elif page.route == '/cliente':
            page.window_width = 400
            page.title = 'Cliente'
            page.update()

    page.on_route_change = router_change
    page.go('/home')


app(target=main)
