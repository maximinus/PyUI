from pyui.base import Position
from pyui.widgets import Menu, MenuItem
from pyui.events.loop import app

BACKGROUND_COLOR = (140, 140, 140)


def get_menu():
    # get some menu items
    menu1 = MenuItem('Open File', 'open')
    menu2 = MenuItem('Close File')
    menu3 = MenuItem('Exit IDE')
    return Menu(Position(200, 150), items=[menu1, menu2, menu3])


if __name__ == '__main__':
    menu = get_menu()
    app.push_frame(menu)
    app.event_loop()
