from pygame import Surface

from pyui.helpers import Size, Margin, Alignment, Position, Expand


class Widget:
    def __init__(self, margin=None, align=None, expand=None, background=None):
        if margin is None:
            margin = Margin()
        if align is None:
            align = Alignment.CENTER
        if expand is None:
            expand = Expand.NONE
        self.align = align
        self.margin = margin
        self.expand = expand
        self.background = background
        self.parent = None
        # if a widget is expanding, it means it will draw to the extra
        # apce allocated to it
        self.expanding = False

    @property
    def min_size(self) -> Size:
        return self.margin.size

    def get_position(self, area: Size) -> Position:
        render_position = Position(0, 0)
        space_x = area.width - self.min_size.width
        space_y = area.height - self.min_size.height
        # not enough space, render at 0,0
        if space_x < 0 or space_y < 0:
            return render_position
        # calculate position based on alignment
        # don't offset if wanting to expand AND self-expanding
        if space_x > 0 and not (self.expand.horizontal and self.expanding):
            match self.align.horizontal:
                case Alignment.LEFT:
                    render_position.x = 0
                case Alignment.RIGHT:
                    render_position.x = space_x
                case _:
                    render_position.x = space_x // 2
        if space_y > 0 and not (self.expand.vertical and self.expanding):
            match self.align.vertical:
                case Alignment.TOP:
                    render_position.y = 0
                case Alignment.BOTTOM:
                    render_position.y = space_y
                case _:
                    render_position.y = space_y // 2
        return render_position

    def render(self, destination: Surface, pos: Position, size: Size):
        pass
