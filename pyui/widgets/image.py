from pyui.base import Expand, Size, Align
from pyui.widget_base import Widget


class Image(Widget):
    def __init__(self, image, margin=None, expand=None, fill=Expand.NONE, align=Align.CENTER):
        # the image is an already loaded surface
        super().__init__(expand, margin, align)
        self.image = image
        self.size = Size(image.get_width(), image.get_height())
        self.fill = fill

    def render(self, surface, x, y, available_size=None):
        surface.blit(self.image, (x + self.margin.left, y + self.margin.top))
