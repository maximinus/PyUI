import unittest

from pyui.events.events import Event, MouseLeftClickDown
from pyui.events.loop import get_ordered_callbacks, app
from pyui.base import Position, Size, Color
from pyui.widgets import Frame, Menu, ColorRect, HBox, MenuBar, MenuItem

from pyui.events.queue import ev_queue


class TestCallbacksAdded(unittest.TestCase):
    def test_menu_has_callback(self):
        test_menu = Menu(Position(0, 0), items=[])
        # 2 events should be being listened out for
        self.assertEqual(len(ev_queue.event_listeners), 2)

    def test_menu_callback_exists(self):
        test_menu = Menu(Position(0, 0), items=[])
        # we should find these events
        self.assertTrue(Event.MouseIn, ev_queue.event_listeners)
        self.assertTrue(Event.MouseOut, ev_queue.event_listeners)

    def test_has_added_callback(self):
        color = ColorRect(Size(50, 50), Color.RED)
        color.connect(Event.MouseMove, self.test_menu_has_callback)
        self.assertEqual(len(color.callbacks), 1)

    def test_added_callback_exists(self):
        color = ColorRect(Size(50, 50), Color.RED)
        color.connect(Event.MouseMove, self.test_menu_has_callback)
        test_frame = Frame(Position(0, 0), widget=color)
        ev_queue.get_frame_callbacks(test_frame)
        self.assertEqual(len(ev_queue.event_listeners), 1)

    def test_menu_bar(self):
        menubar = MenuBar()
        menubar.add_menu('File', Menu(items=[MenuItem('Help')]))
        window = Frame(size=Size(800, 600), widget=menubar)
        ev_queue.get_frame_callbacks(window)
        callbacks = app.window_data[0].get_filtered_callbacks([Event.MouseLeftClickDown])
        self.assertEqual(len(ev_queue.event_listeners), 3)


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
