from pyui.base import get_asset, Size, NinePatch
from pyui.widget_base import Widget
from pyui.widgets import TextLabel


class Button(Widget):
    def __init__(self, text, patch_name='button', **kwargs):
        self.patch = NinePatch(patch_name)
        super().__init__(**kwargs)
        self.size = Size(100, 100)
        self.text = TextLabel(text=text, )

    @property
    def min_size(self):
        return self.size

    def draw(self, new_size):
        self.texture = self.get_texture(new_size)
        if self.background is not None:
            self.texture.fill(self.background)

        offset = self.get_align_offset(self.size, new_size)
        self.texture.blit(self.patch.draw(self.size), (offset.x, offset.y))
