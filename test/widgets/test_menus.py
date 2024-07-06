from unittest.mock import patch

import pygame
import unittest
from test.sdl_test import SDLTest, FakeEvent, FakeTexture

from pyui.events.events import MouseMove
from pyui.events.loop import CallbackData, app
from pyui.base import Position, Size
from pyui.theme import THEME
from pyui.widgets import MenuItem, Menu, MenuBar, Frame


class TestMenuItem(SDLTest):
    def test_has_width(self):
        menu = MenuItem('Test')
        min_size = menu.min_size
        self.assertTrue(min_size.width > 0)
        self.assertTrue(min_size.height > 0)

    def test_equal_height(self):
        menu1 = MenuItem('Hello')
        menu2 = MenuItem('World')
        m1_size = menu1.min_size
        m2_size = menu2.min_size
        self.assertEqual(m1_size.height, m2_size.height)


class TestSimpleOverlap(unittest.TestCase):
    def test_overlap(self):
        rect1 = pygame.Rect(0, 0, 100, 100)
        rect2 = pygame.Rect(50, 50, 100, 100)
        self.assertTrue(rect1.colliderect(rect2))

    def test_overlap_area(self):
        rect1 = pygame.Rect(0, 0, 100, 100)
        rect2 = pygame.Rect(50, 50, 100, 100)
        collide_area = rect1.clip(rect2)
        self.assertEqual(collide_area.x, 50)
        self.assertEqual(collide_area.y, 50)
        self.assertEqual(collide_area.width, 50)
        self.assertEqual(collide_area.height, 50)

    def test_no_overlap(self):
        rect1 = pygame.Rect(0, 0, 100, 100)
        rect2 = pygame.Rect(150, 150, 100, 100)
        self.assertFalse(rect1.colliderect(rect2))


class FakeMoveEvent:
    def __init__(self, pos):
        self.pos = pos
        self.rel = [0, 0]


class TestHighlightDetection(SDLTest):
    def setUp(self):
        # we need pygame setup else the font is not there
        self.menuitem = MenuItem('Test')
        self.menu = Menu(Position(0, 0), items=[self.menuitem])

    def test_starts_unhighlighted(self):
        self.assertFalse(self.menuitem.highlighted)

    def test_highlight_added_after_move(self):
        event = MouseMove(FakeMoveEvent([150, 150]))
        self.menu.mouse_move(CallbackData(event, None))
        self.assertTrue(self.menuitem.highlighted)
        self.menuitem.highlighted = False

    def test_highlighted_false_after_missed_move(self):
        event = MouseMove(FakeMoveEvent([0, 0]))
        self.menu.mouse_move(CallbackData(event, None))
        self.assertFalse(self.menuitem.highlighted)

    def test_highlighted_false_after_over_and_not_over(self):
        first_event = MouseMove(FakeMoveEvent([150, 150]))
        second_event = MouseMove(FakeMoveEvent([0, 0]))
        self.menu.mouse_move(CallbackData(first_event, None))
        self.assertTrue(self.menuitem.highlighted)
        self.menu.mouse_move(CallbackData(second_event, None))
        self.assertFalse(self.menuitem.highlighted)


class TestMenuItemHeights(SDLTest):
    def test_default_margin_is_zero(self):
        item = MenuItem('Hello')
        self.assertEqual(item.margin.top, 0)
        self.assertEqual(item.margin.bottom, 0)

    def test_one_item_no_change(self):
        item = MenuItem('Hello')
        _ = Menu(Position(0, 0), items=[item])
        self.assertEqual(item.margin.top, 0)
        self.assertEqual(item.margin.bottom, 0)

    def test_two_items_mismatched_margins(self):
        # use 2 different text styles, but the final heights should be equal
        style = THEME.text['default']
        item1 = MenuItem('Hello', style=style)
        style.text_size = 40
        item2 = MenuItem('Hello', style=style)
        _ = Menu(Position(0, 0), items=[item1, item2])
        # the min size height of both should be the same
        self.assertEqual(item1.min_size.height, item2.min_size.height)


class TestMenuBarParent(SDLTest):
    def test_parent_is_frame(self):
        item = MenuItem('Hello')
        menu = Menu(items=[item])
        menubar = MenuBar()
        menubar.add_menu('File', menu)
        window = Frame(size=Size(800, 800), widget=menubar)
        self.assertEqual(window, menubar.get_root())


class TestMenuBarHighlight(SDLTest):
    def setUp(self):
        app.reset()

    def test_heading_is_highlighted(self):
        menu1 = Menu(items=[MenuItem('Hello')])
        menu2 = Menu(items=[MenuItem('Goodbye')])
        menubar = MenuBar()
        menubar.add_menu('Test', menu1)
        menubar.add_menu('Menu', menu2)
        window = Frame(size=Size(800, 600), widget=menubar)
        window.render()
        header = menubar.widgets[0]
        with patch.object(header, 'get_texture') as mock_fill:
            fake_tex = FakeTexture()
            mock_fill.return_value = fake_tex
            # click the menu
            header.clicked(FakeEvent(xpos=10, ypos=10))
            # the background of the menubar should have changed
            self.assertEqual(header.background, THEME.color['menu_header_highlight'])
            mock_fill.assert_called()
            self.assertEqual(header.background, fake_tex.fill_color)

    def test_menubar_updated(self):
        # we should see a draw after updating
        menu1 = Menu(items=[MenuItem('Hello')])
        menu2 = Menu(items=[MenuItem('Goodbye')])
        menubar = MenuBar()
        menubar.add_menu('Test', menu1)
        menubar.add_menu('Menu', menu2)
        window = Frame(size=Size(800, 600), widget=menubar)
        window.render()
        app.push_frame(window)
        # we want to see that the display is updated with the new dirty_rect
        header = menubar.widgets[0]
        # put in loop mode, else frame is added instantly and causes test to fail
        app.looping = True
        header.clicked(FakeEvent(xpos=10, ypos=10))
        self.assertEqual(len(app.dirty_widgets), 1)
        app.display = FakeTexture()
        app.update_dirty_widgets()
        self.assertTrue(app.display.blit_called)
        self.assertEqual(app.display.sdl_surface, window.texture)

    def test_header_rendered_to_window(self):
        # we should see a draw FROM the widget after updating
        menu1 = Menu(items=[MenuItem('Hello')])
        menu2 = Menu(items=[MenuItem('Goodbye')])
        menubar = MenuBar()
        menubar.add_menu('Test', menu1)
        menubar.add_menu('Menu', menu2)
        window = Frame(size=Size(800, 600), widget=menubar)
        window.render()
        app.push_frame(window)
        # we want to see that the display is updated with the new dirty_rect
        header = menubar.widgets[0]
        # put in loop mode, else frame is added instantly and causes test to fail
        app.looping = True
        header.clicked(FakeEvent(xpos=10, ypos=10))
        menubar.texture = FakeTexture()
        app.display = FakeTexture()
        window.texture = FakeTexture()
        app.update_dirty_widgets()
        self.assertTrue(window.texture.blit_called)
        # the call will be from the menubar
        self.assertEqual(window.texture.sdl_surface, menubar.texture)
        self.assertEqual(menubar.texture.sdl_surface, header.texture)

    def test_final_surface_correct_color(self):
        # after the click, the app display should contain a pixel at (1,1) of the expected color
        menu1 = Menu(items=[MenuItem('Hello')])
        menu2 = Menu(items=[MenuItem('Goodbye')])
        menubar = MenuBar()
        menubar.add_menu('Test', menu1)
        menubar.add_menu('Menu', menu2)
        window = Frame(size=Size(800, 600), widget=menubar)
        window.render()
        app.push_frame(window)
        # we want to see that the display is updated with the new dirty_rect
        header = menubar.widgets[0]
        # put in loop mode, else frame is added instantly and causes test to fail
        app.looping = True
        header.clicked(FakeEvent(xpos=10, ypos=10))
        app.update_dirty_widgets()
        # grab the pixel at (1,1) and test the color; [:3] removes the alpha
        pixel = list(app.display.get_at((1, 1))[:3])
        expected_color = THEME.color['menu_header_highlight']
        self.assertEqual(pixel, expected_color)
        # this should also be the case on the all the children
        menubar_pixel = list(menubar.texture.get_at((1, 1))[:3])
        header_pixel = list(menubar.widgets[0].texture.get_at((1, 1))[:3])
        self.assertEqual(menubar_pixel, expected_color)
        self.assertEqual(header_pixel, expected_color)
