import unittest

from pyui.widget import Widget
from pyui.helpers import Size, Margin, Position, Alignment


class TestWidget(unittest.TestCase):
    def test_default_size(self):
        widget = Widget()
        self.assertEqual(widget.min_size, Size(0, 0))
    
    def test_with_margin(self):
        widget = Widget(margin=Margin(10, 20, 30, 40))
        self.assertEqual(widget.min_size, Size(10 + 20, 30 + 40))

    def test_after_margin_update(self):
        widget = Widget(margin=Margin(10, 20, 30, 40))
        widget.margin = Margin(5, 5, 5, 5)
        self.assertEqual(widget.min_size, Size(5 + 5, 5 + 5))


class TestWidgetAlignHorizontal(unittest.TestCase):
    def test_horizontal_align(self):
        widget = Widget(align=Alignment.LEFT)
        self.assertEqual(widget.horizontal_align, Alignment.LEFT)

    def test_horizontal_align_center(self):
        widget = Widget(align=Alignment.CENTER)
        self.assertEqual(widget.horizontal_align, Alignment.CENTER)

    def test_horizontal_align_right(self):
        widget = Widget(align=Alignment.RIGHT)
        self.assertEqual(widget.horizontal_align, Alignment.RIGHT)

    def test_horizontal_align_top_left(self):
        widget = Widget(align=Alignment.TOP_LEFT)
        self.assertEqual(widget.horizontal_align, Alignment.LEFT)

    def test_horizontal_align_top_right(self):
        widget = Widget(align=Alignment.TOP_RIGHT)
        self.assertEqual(widget.horizontal_align, Alignment.RIGHT)

    def test_horizontal_align_bottom_left(self):
        widget = Widget(align=Alignment.BOTTOM_LEFT)
        self.assertEqual(widget.horizontal_align, Alignment.LEFT)

    def test_horizontal_align_bottom_right(self):
        widget = Widget(align=Alignment.BOTTOM_RIGHT)
        self.assertEqual(widget.horizontal_align, Alignment.RIGHT)


class TestWidgetAlignVertical(unittest.TestCase):
    def test_vertical_align(self):
        widget = Widget(align=Alignment.TOP)
        self.assertEqual(widget.vertical_align, Alignment.TOP)

    def test_vertical_align_center(self):
        widget = Widget(align=Alignment.CENTER)
        self.assertEqual(widget.vertical_align, Alignment.CENTER)

    def test_vertical_align_bottom(self):
        widget = Widget(align=Alignment.BOTTOM)
        self.assertEqual(widget.vertical_align, Alignment.BOTTOM)

    def test_vertical_align_top_left(self):
        widget = Widget(align=Alignment.TOP_LEFT)
        self.assertEqual(widget.vertical_align, Alignment.TOP)

    def test_vertical_align_top_right(self):
        widget = Widget(align=Alignment.TOP_RIGHT)
        self.assertEqual(widget.vertical_align, Alignment.TOP)

    def test_vertical_align_bottom_left(self):
        widget = Widget(align=Alignment.BOTTOM_LEFT)
        self.assertEqual(widget.vertical_align, Alignment.BOTTOM)

    def test_vertical_align_bottom_right(self):
        widget = Widget(align=Alignment.BOTTOM_RIGHT)
        self.assertEqual(widget.vertical_align, Alignment.BOTTOM)


class TestWidgetPosition(unittest.TestCase):
    def test_position(self):
        widget = Widget(margin=Margin(20, 20, 20, 20))
        position = widget.get_position(Size(40, 40))
        self.assertEqual(position, Position(0, 0))

    def test_position_centre_with_space(self):
        widget = Widget(margin=Margin(20, 20, 20, 20))
        position = widget.get_position(Size(100, 100))
        self.assertEqual(position, Position(30, 30))

    def test_position_left_with_space(self):
        widget = Widget(margin=Margin(20, 20, 20, 20), align=Alignment.LEFT)
        position = widget.get_position(Size(100, 100))
        self.assertEqual(position, Position(0, 30))
    
    def test_position_right_with_space(self):
        widget = Widget(margin=Margin(20, 20, 20, 20), align=Alignment.RIGHT)
        position = widget.get_position(Size(100, 100))
        self.assertEqual(position, Position(60, 30))

    def test_position_top_with_space(self):
        widget = Widget(margin=Margin(20, 20, 20, 20), align=Alignment.TOP)
        position = widget.get_position(Size(100, 100))
        self.assertEqual(position, Position(30, 0))
    
    def test_position_bottom_with_space(self):
        widget = Widget(margin=Margin(20, 20, 20, 20), align=Alignment.BOTTOM)
        position = widget.get_position(Size(100, 100))
        self.assertEqual(position, Position(30, 60))
