import unittest

from pyui.widget import Widget
from pyui.helpers import Size, Margin, Position, Align


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
        widget = Widget(margin=Margin(20, 20, 20, 20), align=Align(Align.LEFT, Align.CENTER))
        position = widget.get_position(Size(100, 100))
        self.assertEqual(position, Position(0, 30))
    
    def test_position_right_with_space(self):
        widget = Widget(margin=Margin(20, 20, 20, 20), align=Align(Align.RIGHT, Align.CENTER))
        position = widget.get_position(Size(100, 100))
        self.assertEqual(position, Position(60, 30))

    def test_position_top_with_space(self):
        widget = Widget(margin=Margin(20, 20, 20, 20), align=Align(Align.CENTER, Align.TOP))
        position = widget.get_position(Size(100, 100))
        self.assertEqual(position, Position(30, 0))
    
    def test_position_bottom_with_space(self):
        widget = Widget(margin=Margin(20, 20, 20, 20), align=Align(Align.CENTER, Align.BOTTOM))
        position = widget.get_position(Size(100, 100))
        self.assertEqual(position, Position(30, 60))
