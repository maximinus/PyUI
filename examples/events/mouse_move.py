import pygame
from pyui.setup import init
from pyui.base import Size, Position
from pyui.widgets import Menu, MenuItem
from pyui.events.loop import PyUIApp

BACKGROUND_COLOR = (140, 140, 140)


def get_menu():
    # get some menu items
    menu1 = MenuItem('Open File', 'open')
    menu2 = MenuItem('Close File')
    menu3 = MenuItem('Exit IDE')
    return Menu(items=[menu1, menu2, menu3])


if __name__ == '__main__':
    display = init()
    menu = get_menu()
    display.fill(BACKGROUND_COLOR)
    menu.render(display, Position(100, 100), Size(250, 200))
    pygame.display.flip()

    app = PyUIApp(frame=menu)
    app.event_loop()
