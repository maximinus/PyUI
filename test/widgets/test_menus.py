import pygame
import unittest

from pyui.events.events import MouseMove
from pyui.setup import init
from pyui.base import Position, Size
from pyui.theme import THEME
from pyui.widgets import MenuItem, Menu, MenuBar, Frame


class TestMenuItem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

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


class TestMenu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_equal_heights(self):
        menu1 = MenuItem('Hello')
        menu2 = MenuItem('World')
        menu3 = MenuItem('There')
        menu = Menu(Position(0, 0), items=[menu1, menu2, menu3])
        height = menu.min_size.height
        # must be a multiple of 3
        self.assertTrue((height % 3) == 0)


class TestSimpleCollision(unittest.TestCase):
    def test_simple_collision(self):
        render_rect = pygame.Rect(0, 0, 100, 100)
        self.assertTrue(render_rect.collidepoint(50, 50))

    def test_simple_collision_with_offset(self):
        render_rect = pygame.Rect(100, 100, 100, 100)
        self.assertTrue(render_rect.collidepoint(150, 150))

    def test_real_collision(self):
        # pygame seems funny about this
        # the rect is actually left, top, width, height
        render_rect = pygame.Rect(206, 156, 105, 24)
        # the collide_rect does not actually allow for the top and bottom, it checks against width and height
        self.assertTrue(render_rect.collidepoint(210, 160))

    def test_real_no_collision(self):
        render_rect = pygame.Rect(206, 156, 105, 24)
        self.assertFalse(render_rect.collidepoint(0, 0))


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


class TestHighlightDetection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        # we need pygame setup else the font is not there
        self.menuitem = MenuItem('Test')
        # we are going to fake a render_rect to avoid rendering to screen
        self.menuitem.render_rect = pygame.Rect(100, 100, 100, 100)
        self.menu = Menu(Position(0, 0), items=[self.menuitem])

    def test_starts_unhighlighted(self):
        self.assertFalse(self.menuitem.highlighted)

    def test_highlight_added_after_move(self):
        event = MouseMove(FakeMoveEvent([150, 150]))
        self.menu.mouse_move(event)
        self.assertTrue(self.menuitem.highlighted)
        self.menuitem.highlighted = False

    def test_highlighted_false_after_missed_move(self):
        event = MouseMove(FakeMoveEvent([0, 0]))
        self.menu.mouse_move(event)
        self.assertFalse(self.menuitem.highlighted)

    def test_highlighted_false_after_over_and_not_over(self):
        first_event = MouseMove(FakeMoveEvent([150, 150]))
        second_event = MouseMove(FakeMoveEvent([0, 0]))
        self.menu.mouse_move(first_event)
        self.assertTrue(self.menuitem.highlighted)
        self.menu.mouse_move(second_event)
        self.assertFalse(self.menuitem.highlighted)


class TestMenuItemHeights(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

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
        style.size = 40
        item2 = MenuItem('Hello', style=style)
        _ = Menu(Position(0, 0), items=[item1, item2])
        # the min size height of both should be the same
        self.assertEqual(item1.min_size.height, item2.min_size.height)
