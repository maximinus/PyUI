import unittest

from pyui.base import Color, Size, Position
from pyui.widget_base import Widget
from pyui.widgets import ColorRect, HBox, Frame


class TestBaseWidget(unittest.TestCase):
    def test_not_a_container(self):
        w = Widget()
        self.assertFalse(w.container)

    def test_starts_with_no_texture(self):
        w = Widget()
        self.assertIsNone(w.texture)

    def test_current_size_invalid(self):
        w = Widget()
        self.assertEqual(w.current_size, Size(-1, -1))

    def test_parent_is_none(self):
        widget = Widget()
        self.assertIsNone(widget.parent)

    def test_complex_parent(self):
        color_rect = ColorRect(Size(10, 10), Color.RED)
        box = HBox(widgets=[color_rect])
        root = Frame(None, pos=Position(0, 0), widget=box)
        root_widget = root.get_root()
        self.assertEqual(root, root_widget)

    def test_min_size_zero(self):
        widget = Widget()
        size = widget.min_size
        self.assertEqual(size.width, 0)
        self.assertEqual(size.height, 0)


class TestBaseWidgetSpec(unittest):
    def test_simple_render(self):
        # When a widget is rendered to a size N, it will create a texture of that size, although it may not use all of it
        w = Widget()
        w.render(Size(20, 20), Position(0, 0))
        self.assertEqual(w.current_size.width, 20)
        self.assertEqual(w.current_size.height, 20)
        self.assertIsNotNone(self.texture)

    def test_no_render_no_texture(self):
        # A widgets texture is always None until it is rendered.
        w = Widget()
        self.assertIsNone(w.texture)
