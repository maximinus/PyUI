from test.sdl_test import SDLTest

from pyui.base import Size, Position, Color, Margin
from pyui.widgets import Frame, Border, ColorRect, HBox


class TestBasicFrameOffset(SDLTest):
    def test_simple_frame(self):
        frame = Frame(Size(50, 50), pos=Position(0, 0))
        self.assertEqual(frame.frame_offset, Position(0, 0))

    def test_simple_border(self):
        border = Border(Size(50, 50), pos=Position(0, 0))
        self.assertEqual(border.frame_offset, Position(0, 0))

    def test_frame_with_margin(self):
        crect = ColorRect(Size(50, 50), Color.RED)
        frame = Frame(Size(100, 100), pos=Position(0, 0), widget=crect, margin=Margin(10, 10, 10, 10))
        frame.draw(frame.current_size)
        self.assertEqual(crect.frame_offset, Position(10, 10))

    def test_hbox_and_frame_with_margin(self):
        crect = ColorRect(Size(50, 50), Color.RED)
        box = HBox(widgets=[crect], margin=Margin(10, 10, 10, 10))
        frame = Frame(Size(100, 100), pos=Position(0, 0), widget=box, margin=Margin(10, 10, 10, 10))
        frame.draw(frame.current_size)
        self.assertEqual(frame.frame_offset, Position(0, 0))
        self.assertEqual(box.frame_offset, Position(10, 10))
        # crect is centered in thr widget, thus the offset
        self.assertEqual(crect.frame_offset, Position(25, 25))
