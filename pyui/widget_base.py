from pyui.base import Expand, Margin, Align, Size


class Widget:
    def __init__(self, expand=None, margin=None, align=None):
        self.expand = expand if expand is not None else Expand.NONE
        self.margin = margin if margin is not None else Margin()
        self.align = Align(align) if align is not None else Align(Align.TOP|Align.LEFT)
        self.size = Size(0, 0)

    @property
    def min_size(self):
        return self.size.add_margin(self.margin)

    def render(self, surface, x, y, available_size=None):
        # if the available size is None, then the default is to render at the minimum size
        pass
