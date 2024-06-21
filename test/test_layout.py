import unittest

from pyui.base import Color, Expand, Size, Margin, Align
from pyui.widgets import HBox, VBox, ColorRect


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
        self.assertEqual(sizes[1].width, 20)
        self.assertEqual(sizes[1].height, 10)


class TestOldFailingExamples(unittest.TestCase):
    def test_1(self):
        # a single HBox filling all space, has 3 widgets: the middle does not fill vertically
        box = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, expand=Expand.BOTH),
                            ColorRect(Size(50, 50), Color.GREEN, expand=Expand.HORIZONTAL),
                            ColorRect(Size(50, 50), Color.BLUE, expand=Expand.BOTH)])
        sizes = box.calculate_sizes(Size(900, 600))
        self.assertEqual(sizes[0], Size(300, 600))
        self.assertEqual(sizes[1], Size(300, 50))
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
