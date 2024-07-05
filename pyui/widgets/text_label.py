import pygame

from pyui.base import Size, Align, Position
from pyui.widget_base import Widget
from pyui.theme import THEME


class TextLabel(Widget):
    def __init__(self, text, style=None, background=None, expand=None, margin=None, align=None, fill=None):
        super().__init__(expand, margin, align, fill)
        self.text = text
        self.style = style
        self.background = background
        if style is None:
            self.style = THEME.text['menu']
        self.font = pygame.font.Font(self.style.font, self.style.size)
        self.image = self.font.render(text, True, self.style.color)
        self.text_size = Size(self.image.get_width(), self.image.get_height())

    @property
    def min_size(self):
        return self.text_size.add_margin(self.margin)

    def draw(self, new_size):
        self.texture = self.get_texture(new_size)

        # text labels ignore "fill" as they cannot naturally expand
        if self.background is not None:
            self.texture.fill(self.background)
        x = self.margin.left
        y = self.margin.top

        horiz_align = self.align.horizontal()
        full_size = self.min_size
        if horiz_align == Align.CENTER:
            x += (new_size.width - full_size.width) // 2
        elif horiz_align == Align.RIGHT:
            x += (new_size.width - full_size.width)

        vert_align = self.align.vertical()
        if vert_align == Align.CENTER:
            y += (new_size.height - full_size.height) // 2
        elif vert_align == Align.BOTTOM:
            y += (new_size.height - full_size.height)

        self.texture.blit(self.image, (x, y))
        self.current_size = new_size
