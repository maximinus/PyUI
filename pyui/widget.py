from pygame import Surface

from pyui.helpers import Size, Margin, Align, Position, Expand


class Widget:
    def __init__(self, margin=None, align=None, expand=None, background=None):
        if margin is None:
            margin = Margin()
        if align is None:
            align = Align(Align.CENTER, Align.CENTER)
        if expand is None:
            expand = Expand.NONE
        self.align = align
        self.margin = margin
        self.expand = expand
        self.background = background
        self.parent = None

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
        if space_x > 0:
            match self.align.horizontal:
                case Align.LEFT:
                    render_position.x = 0
                case Align.RIGHT:
                    render_position.x = space_x
                case Align.FILL:
                    render_position.x = 0
                case _:
                    render_position.x = space_x // 2
        if space_y > 0:
            match self.align.vertical:
                case Align.TOP:
                    render_position.y = 0
                case Align.BOTTOM:
                    render_position.y = space_y
                case Align.FILL:
                    render_position.y = 0
                case _:
                    render_position.y = space_y // 2
        return render_position

    def render(self, destination: Surface, pos: Position, size: Size):
        pass
