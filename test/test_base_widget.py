import unittest

from pyui.base import Color, Size, Position
from pyui.widget_base import Widget
from pyui.widgets import ColorRect, HBox, Frame


class TestBaseWidget(unittest.TestCase):
    def test_start_with_no_render_rect(self):
        widget = Widget()
        self.assertIsNone(widget.render_rect)

    def test_start_needing_redraw(self):
        widget = Widget()
        self.assertTrue(widget.redraw)

    def test_parent_is_none(self):
        widget = Widget()
        self.assertIsNone(widget.parent)

    def test_complex_parent(self):
        color_rect = ColorRect(Size(10, 10), Color.RED)
        box = HBox(widgets=[color_rect])
        root = Frame(Position(0, 0), widget=box)
        root_widget = root.get_root()
        self.assertEqual(root, root_widget)

    def test_min_size_zero(self):
        widget = Widget()
        size = widget.min_size
        self.assertEqual(size.width, 0)
        self.assertEqual(size.height, 0)
