from pyui.widget import Widget

from pyui.helpers import Position, Align, Expand


class Absolute(Widget):
    """A widget that allows absolute positioning of it's child widget"""
    def __init__(self, child, pos: Position, *args, **kwargs):
        assert "expand" not in kwargs, "Absolute layout does not support expand"
        assert "align" not in kwargs, "Absolute layout does not support align"
        assert "background" not in kwargs, "Absolute layout does not support background"
        assert "margin" not in kwargs, "Absolute layout does not support margin"
        super().__init__(*args, align=Align(Align.LEFT, Align.TOP),
                         expand=Expand.NONE)
        self.offset = pos
        self.child = child
    
    def add_child(self, child: Widget):
        assert False, "Absolute layout can only have one child"
    
    def render(self, mouse, destination, position, size):
        """Render the absolute layout and its children."""
        self.child.render(mouse, destination, position + self.offset, size)

    def set_active(self, is_active):
        self.active = is_active
        self.child.set_active(is_active)
