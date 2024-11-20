import pygame.display

from pyui.base import Size, Color, Align, Expand
from pyui.setup import init, await_keypress
from pyui.widgets import Button, HBox, Frame


def get_layout():
    button1 = Button('Hello', Size(120, 60), expand=Expand.HORIZONTAL, align=Align.CENTER)
    button2 = Button('World', Size(120, 60), expand=Expand.HORIZONTAL, align=Align.CENTER)
    button3 = Button('Again', Size(120, 60), expand=Expand.HORIZONTAL, align=Align.CENTER)
    box = HBox(align=Align.CENTER, widgets=[button1, button2, button3], background=Color.BLUE)
    frame = Frame(size=Size(800, 600), widget=box, background=Color.RED)
    return frame


if __name__ == '__main__':
    display = init()
    window = get_layout()
    window.render(Size(800, 600))
    display.blit(window.texture, (0, 0))
    pygame.display.flip()
    await_keypress()
