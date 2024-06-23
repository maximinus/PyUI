from pyui.base import Expand, Margin, Align, Size


# let's define the base widget
# a widget has a size, and a min_size
# the size is the rendered content of the widget
# the min_size is the size of the widget + margin
# this is bad naming, as min_size > size!!
# "min_size" is asking, what is the smallest size? The name is fine
# "widget_size" means "how big is this widget if I had to draw it?
#    * Some widgets require a size: ColorRect
#    * Some widgets acquire a size (Image, Icon)
# Right now, we render to screen, but this will surely need to stop, if only to avoid over-writing on screeen
# When we blit to another image, we will need the minimum size of the area required to draw to
# This will include the border!
# However, the border is a special case since it's always the parent


class Widget:
    def __init__(self, expand=None, margin=None, align=None):
        self.expand = expand if expand is not None else Expand.NONE
        self.margin = margin if margin is not None else Margin()
        self.align = Align(align) if align is not None else Align(Align.CENTER)
        self.size = Size(0, 0)

    @property
    def min_size(self):
        return self.size.add_margin(self.margin)

    def render(self, surface, x, y, available_size=None):
        # if the available size is None, then the default is to render at the minimum size
        pass
