from pyui.base import NinePatch, Margin
from pyui.theme import THEME
from pyui.widget_base import Widget
from pyui.widgets import TextLabel


class Button(Widget):
    def __init__(self, text, patch_name='button', **kwargs):
        self.patch = NinePatch(patch_name)
        super().__init__(**kwargs)
        self.text = TextLabel(text=text, style=THEME.text['button_text'])
        self.text_margin = Margin(20, 20, 10, 10)

    @property
    def min_size(self):
        return self.text.min_size.add_margin(self.text_margin).add_margin(self.margin)

    def draw(self, new_size):
        text_size = self.text.min_size
        size = self.min_size
        self.text.draw(text_size)

        self.texture = self.get_texture(new_size)
        if self.background is not None:
            self.texture.fill(self.background)

        offset = self.get_align_offset(size, new_size)
        offset.x += self.margin.left
        offset.y += self.margin.top
        self.texture.blit(self.patch.draw(size), (offset.x, offset.y))
        offset.x += (size.width - text_size.width) // 2
        offset.y += (size.height - text_size.height) // 2
        self.texture.blit(self.text.texture, (offset.x, offset.y))
