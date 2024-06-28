from pyui.base import Position
from pyui.widgets import MenuBar, Frame
from pyui.events.loop import app, DEFAULT_SIZE


# create a simple menubar and display it maxed in a window
# a window is a frame at maximum size


def get_menubar():
    menubar = MenuBar()
    menubar.add_menu('File', None)
    menubar.add_menu('Edit', None)
    menubar.add_menu('Help', None)
    return menubar


if __name__ == '__main__':
    menu = get_menubar()
    window = Frame(Position(0, 0), size=DEFAULT_SIZE, widget=menu)
    app.push_frame(window)
    app.event_loop()
