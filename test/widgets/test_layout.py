import pygame
import unittest

from pyui.setup import init
from pyui.base import Color, Expand, Size, Margin, Align, Position
from pyui.widgets import HBox, VBox, ColorRect, Spacer, TextLabel, Border


class TestMixedBoxes(unittest.TestCase):
    def test_simple(self):
        # a vbox contains 2 rows, each of 2 HBoxes
        # Each hbox contains a single ColorRect of size 10x10
        # the top left one is set to expand in both directions
        tl_box = HBox(widgets=[ColorRect(Size(10, 10), Color.RED, expand=Expand.BOTH)])
        tr_box = HBox(widgets=[ColorRect(Size(10, 10), Color.RED)])
        bl_box = HBox(widgets=[ColorRect(Size(10, 10), Color.RED)])
        br_box = HBox(widgets=[ColorRect(Size(10, 10), Color.RED)])
        top_row = HBox(widgets=[tl_box, tr_box])
        bottom_row = HBox(widgets=[bl_box, br_box])
        main_box = VBox(widgets=[top_row, bottom_row])
        sizes = main_box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].width, 200)
        self.assertEqual(sizes[0].height, 190)
        self.assertEqual(sizes[1].width, 200)
        self.assertEqual(sizes[1].height, 10)


class TestOldFailingExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_1(self):
        # a single HBox filling all space, has 3 widgets: the middle does not fill vertically
        box = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, expand=Expand.BOTH),
                            ColorRect(Size(50, 50), Color.GREEN, expand=Expand.HORIZONTAL),
                            ColorRect(Size(50, 50), Color.BLUE, expand=Expand.BOTH)])
        sizes = box.calculate_sizes(Size(900, 600))
        self.assertEqual(sizes[0], Size(300, 600))
        self.assertEqual(sizes[1], Size(300, 600))
        self.assertEqual(sizes[2], Size(300, 600))

    def test_2(self):
        m = Margin(10, 10, 10, 10)
        box = HBox(widgets=[ColorRect(Size(50, 50), Color.BLUE, align=Align.CENTER,
                                      expand=Expand.BOTH, fill=Expand.HORIZONTAL, margin=m),
                            ColorRect(Size(50, 50), Color.BLUE, align=Align.CENTER,
                                      expand=Expand.BOTH, fill=Expand.HORIZONTAL, margin=m),
                            ColorRect(Size(50, 50), Color.BLUE, align=Align.CENTER,
                                      expand=Expand.BOTH, fill=Expand.HORIZONTAL, margin=m)])
        sizes = box.calculate_sizes(Size(800, 600))
        # we expect them to all have very similar sizes, around 800/3 = 266 or 267
        self.assertTrue(266 <= sizes[0].width <= 267)
        self.assertTrue(266 <= sizes[1].width <= 267)
        self.assertTrue(266 <= sizes[2].width <= 267)

    def test_3(self):
        box = HBox(widgets=[ColorRect(Size(50, 50), Color.BLUE, margin=Margin(10, 10, 10, 10)),
                            Spacer(Size(200, 0)),
                            ColorRect(Size(50, 50), Color.BLUE, margin=Margin(10, 10, 10, 10))])
        size = box.min_size
        # since nothing is growing, the size should be ((50 + 10 + 10) * 2) + 200 = 340
        self.assertEqual(size.width, 340)

    def test_4(self):
        box = HBox(widgets=[ColorRect(Size(50, 50), Color.BLUE), TextLabel('Hello, World')])
        # there is no margin, and the textsize is 24, so we expect the min_size to be 50 height
        min_size = box.min_size
        self.assertEqual(min_size.height, 50)
        # if it's in a border, it will be bigger by twice the corner height
        border = Border(Size(100, 100), widget=box)
        min_size = border.min_size
        # the border size is the size of it's defined size + margin
        self.assertEqual(min_size.height, 100)
        # which should be equal to it's size
        self.assertEqual(border.current_size.height, min_size.height)

    def test_5(self):
        box = HBox(widgets=[ColorRect(Size(50, 50), Color.BLUE, margin=Margin(10, 10, 10, 10)),
                            Spacer(Size(200, 0)),
                            ColorRect(Size(50, 50), Color.BLUE, margin=Margin(10, 10, 10, 10))])
        min_size = box.min_size
        self.assertEqual(min_size.width, 70 + 200 + 70)
        self.assertEqual(min_size.height, 70)
