from pyui.widget_base import Widget


class Spacer(Widget):
    def __init__(self, size, expand=None):
        # a spacer is a simple widget whose only job is to consume space
        # it has no margin
        super().__init__(expand=expand)
        self.size = size

    def render(self, surface, x, y, available_size=None):
        pass
