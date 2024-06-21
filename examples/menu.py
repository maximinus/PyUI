import pygame
from pyui.setup import init, await_keypress, DEFAULT_SIZE
from pyui.widgets import Menu, MenuItem

BACKGROUND_COLOR = (80, 80, 80)

# we will set up functions to display color widgets


def screen1():
    # get some menu items
    menu1 = MenuItem('Open File', 'open')
    menu2 = MenuItem('Close File')
    menu3 = MenuItem('Exit IDE')
    return Menu(items=[menu1, menu2, menu3])


if __name__ == '__main__':
    display = init()
    screens = [screen1()]
    for single_screen in screens:
        display.fill(BACKGROUND_COLOR)
        single_screen.render(display, 100, 100)
        pygame.display.flip()
        await_keypress()
    pygame.quit()
