import unittest

from pyui.base import Size, Position
from pyui.events.loop import PyUIApp
from pyui.widgets import Frame


class TestPyUiApp(unittest.TestCase):
    def setUp(self):
        self.app = PyUIApp(window_size=Size(100, 100))

    def test_no_frames(self):
        self.assertEqual(len(self.app.window_data), 0)

    def test_no_dirty_rects(self):
        self.assertEqual(len(self.app.dirty_widgets), 0)

    def test_frame_added_and_removed(self):
        test_frame = Frame(Position(0, 0), Size(100, 100))
        self.app.push_frame(test_frame)
        self.assertEqual(len(self.app.window_data), 1)
        self.app.pop_frame()
        self.assertEqual(len(self.app.window_data), 0)

    def test_frame_order_reversed(self):
        # the first frame in the list should be the last added
        frame1 = Frame(Position(0, 0), Size(100, 100))
        frame2 = Frame(Position(0, 0), Size(100, 100))
        self.app.push_frame(frame1)
        self.app.push_frame(frame2)
        self.assertEqual(self.app.window_data[0].frame, frame2)
        self.app.pop_frame()
        self.assertEqual(self.app.window_data[0].frame, frame1)
        self.app.pop_frame()
        self.assertEqual(len(self.app.window_data), 0)

