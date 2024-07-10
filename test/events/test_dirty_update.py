from unittest.mock import patch

import pygame

from pyui.base import Size, Align, Position, Margin
from pyui.events.loop import app
from pyui.widgets import Frame, TextLabel, Button, VBox
from test.sdl_test import SDLTest


class TestSimpleDirty(SDLTest):
    def test_is_dirty(self):
        label = TextLabel('Hello', align=Align.CENTER)
        frame = Frame(size=Size(800, 600), pos=Position(0, 0), widget=label)
        app.push_frame(frame)
        label.update_text('World')
        app.set_dirty(label)
        self.assertEqual(len(app.dirty_widgets), 1)
        app.reset()

    @patch.object(Frame, 'update_dirty_widget')
    def test_dirty_discovered(self, mock):
        label = TextLabel('Hello', align=Align.CENTER)
        frame = Frame(size=Size(800, 600), pos=Position(0, 0), widget=label)
        frame.draw(Size(800, 600))
        app.push_frame(frame)
        label.update_text('World')
        app.set_dirty(label)
        app.update_dirty_widgets()
        self.assertTrue(mock.called)
        app.reset()


class TestFrameDirtyUpdates(SDLTest):
    def test_widget_area_no_offset(self):
        label = TextLabel('Hello', align=Align.CENTER)
        frame = Frame(size=Size(800, 600), pos=Position(0, 0), widget=label)
        frame.draw(Size(800, 600))
        area = frame.update_dirty_widget(label)
        # this should be the area of the text widget on screen.
        self.assertEqual(area, pygame.Rect(0, 0, 800, 600))

    def test_widget_area_with_offset(self):
        label = TextLabel('Hello', align=Align.CENTER)
        frame = Frame(size=Size(800, 600), pos=Position(0, 0), widget=label, margin=Margin(20, 20, 20, 20))
        frame.draw(Size(800, 600))
        area = frame.update_dirty_widget(label)
        # this should be the area of the text widget on screen.
        self.assertEqual(area, pygame.Rect(20, 20, 760, 560))

    def test_nested_widget(self):
        m = Margin(16, 16, 16, 16)
        button = Button('Click Me', Size(120, 60), margin=m, align=Align.CENTER)
        label = TextLabel('Clicked 0 times', margin=m, align=Align.CENTER)
        box = VBox(align=Align.CENTER, widgets=[button, label])
        frame = Frame(size=Size(800, 600), pos=Position(0, 0), widget=box, background=(80, 80, 80))
        frame.draw(Size(800, 600))
        area = frame.update_dirty_widget(label)
        self.assertEqual(area, pygame.Rect(316, 304, 167, 51))
