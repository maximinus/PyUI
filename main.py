import pygame

from pyui.setup import init, await_keypress, DEFAULT_SIZE
from pyui.base import Color, Size
from pyui.widgets import ColorRect, HBox

BACKGROUND_COLOR = (30, 30, 30)


def main():
    screen = init()

    # Create widgets and containers
    rect1 = ColorRect(Size(100, 50), Color.RED)
    rect2 = ColorRect(Size(100, 50), Color.GREEN)
    rect3 = ColorRect(Size(100, 50), Color.BLUE)

    row = HBox()
    row.add_widget(rect1)
    row.add_widget(rect2)
    row.add_widget(rect3)

    screen.fill(BACKGROUND_COLOR)
    row.render(screen, 0, 0, DEFAULT_SIZE)
    pygame.display.flip()

    await_keypress()


if __name__ == "__main__":
    main()
    pygame.quit()
