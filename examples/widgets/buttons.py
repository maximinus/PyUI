import pygame.display

from pyui.base import Size, Color, Align, Expand, Margin
from pyui.setup import init, await_keypress
from pyui.widgets import Button, HBox, Frame


def get_layout():
    button1 = Button('Hello', expand=Expand.HORIZONTAL)
    button2 = Button('World', expand=Expand.HORIZONTAL)
    button3 = Button('Again', expand=Expand.HORIZONTAL)
    box = HBox(align=Align.CENTER, widgets=[button1, button2, button3], background=Color.BLUE)
    frame = Frame(size=Size(800, 600), widget=box, margin=Margin(50, 50, 50, 50), background=Color.GREEN)
    return frame


if __name__ == '__main__':
    display = init()
    box = get_layout()
    box.render(Size(800, 600))
    display.blit(box.texture, (0, 0))
    pygame.display.flip()
    await_keypress()
