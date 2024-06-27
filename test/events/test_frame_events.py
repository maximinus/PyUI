import unittest

from pyui.events.loop import FrameEvents, Callback
from pyui.events.events import MouseLeftClickDown, Event


class TestFrameEvents(unittest.TestCase):
    def test_empty_callbacks_with_none(self):
        frame = FrameEvents(1)
        self.assertEqual(len(frame.callbacks), 0)

    def test_frame_matches_event(self):
        frame = FrameEvents(1)
        frame.callbacks.append(Callback(1, Event.MouseLeftClickDown))
        handlers = frame.get_handlers(MouseLeftClickDown.type)
        self.assertEqual(len(handlers), 1)
