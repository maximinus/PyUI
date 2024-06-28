import unittest
from unittest.mock import patch

from pyui.base import Size, Position, Color
from pyui.events.loop import PyUIApp
from pyui.widgets import Frame, ColorRect


class TestPyUiApp(unittest.TestCase):
    def setUp(self):
        self.app = PyUIApp(window_size=Size(100, 100))

    def test_no_frames(self):
        self.assertEqual(len(self.app.frame_events), 0)

    def test_no_dirty_rects(self):
        self.assertEqual(len(self.app.dirty_widgets), 0)

    def test_frame_added_and_removed(self):
        test_frame = Frame(Position(0, 0), Size(100, 100))
        self.app.push_frame(test_frame)
        self.assertEqual(len(self.app.frame_events), 1)
        self.app.pop_frame()
        self.assertEqual(len(self.app.frame_events), 0)

    def test_frame_order_reversed(self):
        # the first frame in the list should be the last added
        frame1 = Frame(Position(0, 0), Size(100, 100))
        frame2 = Frame(Position(0, 0), Size(100, 100))
        self.app.push_frame(frame1)
        self.app.push_frame(frame2)
        self.assertEqual(self.app.frame_events[0].frame, frame2)
        self.app.pop_frame()
        self.assertEqual(self.app.frame_events[0].frame, frame1)
        self.app.pop_frame()
        self.assertEqual(len(self.app.frame_events), 0)

    @patch.object(ColorRect, 'update')
    def test_dirty_rect_updated(self, mock_update):
        # create a frame and a widget, and make the widget dirty
        color_rect = ColorRect(Size(10, 10), Color.RED)
        frame = Frame(Position(10, 10), widget=color_rect)
        self.app.push_frame(frame)
        self.app.set_dirty(color_rect)
        self.app.update_dirty_widgets()
        self.assertTrue(mock_update.called)
        self.app.pop_frame()

    @patch.object(ColorRect, 'update')
    def test_non_attached_dirty_not_updated(self, mock_update):
        # have a color rect not attached to a frame - it shouldn't be updated
        color_rect = ColorRect(Size(10, 10), Color.RED)
        frame = Frame(Position(10, 10))
        self.app.push_frame(frame)
        self.app.set_dirty(color_rect)
        self.app.update_dirty_widgets()
        self.assertFalse(mock_update.called)
        self.app.pop_frame()
