import pygame
from unittest.mock import patch, call

from pyui.base import Color, Size, Position
from pyui.widgets import ColorRect, Frame, HBox
from test.sdl_test import SDLTest


class TestSanityCheck(SDLTest):
    def test_simple(self):
        # confirm simple SDL test works
        self.assertTrue(True)


class TestSimpleDirty(SDLTest):
    def test_simple_collision(self):
        color_rect = ColorRect(size=Size(50, 50), color=Color.RED)
        frame = Frame(Position(0, 0), widget=color_rect)
        # frame needs to be drawn
        frame.render(self.__class__.display, None)
        dirty_rect = pygame.Rect(20, 20, 10, 10)
        self.assertTrue(frame.render_rect.colliderect(dirty_rect))

    def test_clip_rect(self):
        color_rect = ColorRect(size=Size(50, 50), color=Color.RED)
        frame = Frame(Position(0, 0), widget=color_rect)
        # frame needs to be drawn
        frame.render(self.__class__.display, None)
        dirty_rect = pygame.Rect(40, 40, 20, 30)
        overlap = frame.render_rect.clip(dirty_rect)
        self.assertEqual(overlap.x, 40)
        self.assertEqual(overlap.y, 40)
        self.assertEqual(overlap.width, 10)
        self.assertEqual(overlap.height, 10)

    def test_simplest_test(self):
        color_rect = ColorRect(size=Size(50, 50), color=Color.RED)
        frame = Frame(Position(0, 0), widget=color_rect)
        # frame needs to be drawn
        frame.render(self.__class__.display, None)
        with patch.object(color_rect, 'update_dirty_rect') as mm1:
            dirty_rect = pygame.Rect(10, 10, 10, 10)
            frame.update_dirty_rects(self.__class__.display, [dirty_rect])
            mm1.assert_not_called()

    def test_hbox_2_items(self):
        cr1 = ColorRect(size=Size(50, 50), color=Color.RED)
        cr2 = ColorRect(size=Size(80, 80), color=Color.RED)
        box = HBox(widgets=[cr1, cr2])
        frame = Frame(Position(0, 0), size=Size(200, 200), widget=box)
        frame.render(self.__class__.display, None)
        # first color rect should be called, next shouldn't be
        with patch.object(cr1, 'update_dirty_rect') as mm1, patch.object(box, 'update_dirty_rect') as mm2:
            dirty_rect = pygame.Rect(10, 10, 10, 10)
            frame.update_dirty_rects(self.__class__.display, [dirty_rect])
            mm1.assert_not_called()
            mm2.assert_called()
