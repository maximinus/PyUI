from pyui.base import Position, Align
from pyui.widgets import MenuBar, Frame, MenuItem, Menu
from pyui.events.loop import app, DEFAULT_SIZE


# create a simple menubar and display it in a window

def menu1():
    m1 = MenuItem('Open File', 'open')
    m2 = MenuItem('Close File')
    m3 = MenuItem('Exit IDE')
    return Menu(items=[m1, m2, m3])


def menu2():
    m1 = MenuItem('Cut Text')
    m2 = MenuItem('Copy Text')
    m3 = MenuItem('Paste Text')
    return Menu(items=[m1, m2, m3])


def menu3():
    # get some menu items
    m1 = MenuItem('Help')
    m2 = MenuItem('About')
    return Menu(items=[m1, m2])


def get_menubar():
    menubar = MenuBar()
    menubar.add_menu('File', menu1())
    menubar.add_menu('Edit', menu2())
    menubar.add_menu('Help', menu3())
    return menubar


if __name__ == '__main__':
    menu = get_menubar()
    window = Frame(size=DEFAULT_SIZE, widget=menu)
    app.push_frame(window)
    app.event_loop()
