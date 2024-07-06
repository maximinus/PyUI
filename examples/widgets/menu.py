import pygame
from pyui.setup import init, await_keypress
from pyui.base import Size, Color, Margin, Position, get_asset
from pyui.widgets import Menu, MenuItem, HBox, ColorRect, TextLabel, Border, Image, VBox, Frame

BACKGROUND_COLOR = (140, 140, 140)

# we will set up functions to display color widgets


def screen1():
    box = HBox(widgets=[ColorRect(Size(50, 50), Color.BLUE), TextLabel('Hello, World')])
    return Frame(Position(100, 100), widget=box)


def screen2():
    # same as above, just in a Border with some better margins
    box = HBox(widgets=[ColorRect(Size(50, 50), Color.BLUE),
                        TextLabel('Hello, World', margin=Margin(2, 0, 0, 0))],
               margin=Margin(4, 4, 4, 4))
    return Border(None, Position(100, 100), widget=box)


def screen3():
    # now replace the colorrect with an image
    box = HBox(widgets=[Image(get_asset('icons/open.png')),
                        TextLabel('Hello, World', margin=Margin(4, 0, 0, 0))],
               margin=Margin(4, 4, 4, 4))
    return Border(None, Position(100, 100), widget=box)


def screen4():
    # menu items in a VBox, very similar to our menu
    r1 = HBox(widgets=[Image(get_asset('icons/open.png')), TextLabel('Hello, World', margin=Margin(4, 0, 0, 0))])
    r2 = HBox(widgets=[Image(get_asset('icons/open.png')), TextLabel('Another one', margin=Margin(4, 0, 0, 0))])
    r3 = HBox(widgets=[Image(get_asset('icons/open.png')), TextLabel('This to end!', margin=Margin(4, 0, 0, 0))])
    box = VBox(widgets=[r1, r2, r3])
    return Frame(Position(100, 100), widget=box)


def screen5():
    # get some menu items
    menu1 = MenuItem('Open File', 'open')
    menu2 = MenuItem('Close File')
    menu3 = MenuItem('Exit IDE')
    return Menu(Position(100, 100), items=[menu1, menu2, menu3])


if __name__ == '__main__':
    display = init()
    screens = [screen1(), screen2(), screen3(), screen4(), screen5()]
    for single_screen in screens:
        display.fill(BACKGROUND_COLOR)
        single_screen.render(display, Position(0, 0), Position(0, 0), None)
        pygame.display.flip()
        await_keypress()
    pygame.quit()
