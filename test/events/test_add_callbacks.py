import unittest

from pyui.events.events import Event
from pyui.events.loop import get_ordered_callbacks
from pyui.base import Position, Size, Color
from pyui.widgets import Frame, Menu, ColorRect, HBox


class TestCallbacksAdded(unittest.TestCase):
    def test_menu_has_callback(self):
        test_menu = Menu(Position(0, 0), items=[])
        self.assertEqual(len(test_menu.callbacks), 1)

    def test_menu_callback_exists(self):
        # add a menu to a frame; this has a callback
        test_menu = Menu(Position(0, 0), items=[])
        test_frame = Frame(Position(0, 0), widget=test_menu)
        # there is a callback by default in the menu, check we find it
        callbacks = get_ordered_callbacks(test_frame)
        self.assertEqual(len(callbacks), 1)

    def test_has_added_callback(self):
        color = ColorRect(Size(50, 50), Color.RED)
        color.connect(Event.MouseMove, self.test_menu_has_callback)
        self.assertEqual(len(color.callbacks), 1)

    def test_added_callback_exists(self):
        color = ColorRect(Size(50, 50), Color.RED)
        color.connect(Event.MouseMove, self.test_menu_has_callback)
        test_frame = Frame(Position(0, 0), widget=color)
        callbacks = get_ordered_callbacks(test_frame)
        self.assertEqual(len(callbacks), 1)


class TestCallbackOrder(unittest.TestCase):
    def callback(self):
        pass

    def test_callbacks_in_correct_order(self):
        color = ColorRect(Size(50, 50), Color.RED)
        color.connect(Event.MouseMove, self.callback)
        box = HBox(widgets=[color])
        box.connect(Event.MouseLeftClickDown, self.callback)
        test_frame = Frame(Position(0, 0), widget=box)
        callbacks = get_ordered_callbacks(test_frame)
        self.assertEqual(len(callbacks), 2)
        self.assertEqual(callbacks[0].event_type, Event.MouseMove)
        self.assertEqual(callbacks[1].event_type, Event.MouseLeftClickDown)
