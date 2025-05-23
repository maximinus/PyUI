from pygame import Surface

from src.helpers import Size, Margin, Alignment, Position


class Widget:
    def __init__(self, margin=None, align=None):
        if margin is None:
            margin = Margin.none()
        if align is None:
            align = Alignment.CENTER
        self.align = align
        self.margin = margin

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
        if space_x > 0:
            match self.horizontal_align:
                case Alignment.LEFT:
                    render_position.x = 0
                case Alignment.RIGHT:
                    render_position.x = space_x
                case _:
                    render_position.x = space_x // 2
        if space_y > 0:
            match self.vertical_align:
                case Alignment.TOP:
                    render_position.y = 0
                case Alignment.BOTTOM:
                    render_position.y = space_y
                case _:
                    render_position.y = space_y // 2
        return render_position

    @property
    def horizontal_align(self):
        if self.align in [Alignment.LEFT, Alignment.CENTER_LEFT, Alignment.TOP_LEFT, Alignment.BOTTOM_LEFT]:
            return Alignment.LEFT
        elif self.align in [Alignment.RIGHT, Alignment.CENTER_RIGHT, Alignment.TOP_RIGHT, Alignment.BOTTOM_RIGHT]:
            return Alignment.RIGHT
        return Alignment.CENTER

    @property
    def vertical_align(self):
        if self.align in [Alignment.TOP, Alignment.CENTER_TOP, Alignment.TOP_LEFT, Alignment.TOP_RIGHT]:
            return Alignment.TOP
        elif self.align in [Alignment.BOTTOM, Alignment.CENTER_BOTTOM, Alignment.BOTTOM_LEFT, Alignment.BOTTOM_RIGHT]:
            return Alignment.BOTTOM
        return Alignment.CENTER

    def render(self, destination: Surface, pos: Position, size: Size):
        pass
