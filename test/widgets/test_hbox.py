import unittest

from pyui.base import Size, Color, Margin, Expand
from pyui.widgets import HBox, ColorRect, VBox


class TestHBoxMinSize(unittest.TestCase):
    def test_empty_width_zero(self):
        box = HBox()
        self.assertEqual(box.min_size.width, 0)

    def test_size_one_widget(self):
        box = HBox()
        box.add_widget(ColorRect(Size(100, 100), Color.RED))
        self.assertEqual(box.min_size.width, 100)

    def test_size_widget_and_margin(self):
        box = HBox()
        box.add_widget(ColorRect(Size(100, 100), Color.RED, margin=Margin(5, 5, 5, 5)))
        self.assertEqual(box.min_size.width, 110)

    def test_size_two_widgets(self):
        box = HBox()
        box.add_widget(ColorRect(Size(100, 100), Color.RED))
        box.add_widget(ColorRect(Size(150, 100), Color.RED))
        self.assertEqual(box.min_size.width, 250)

    def test_size_two_widgets_margin(self):
        box = HBox()
        box.add_widget(ColorRect(Size(10, 10), Color.RED, margin=Margin(3, 3, 3, 3)))
        box.add_widget(ColorRect(Size(25, 10), Color.RED, margin=Margin(5, 5, 5, 5)))
        self.assertEqual(box.min_size.width, 51)


class TestHBoxRenderSizes(unittest.TestCase):
    def test_empty(self):
        box = HBox()
        self.assertEqual(box.calculate_sizes(Size(100, 100)), [])

    def test_single_item_non_expanding(self):
        box = HBox()
        box.add_widget(ColorRect(Size(40, 40), Color.RED))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(len(sizes), 1)
        self.assertEqual(sizes[0].width, 40)

    def test_single_item_expanding(self):
        box = HBox()
        box.add_widget(ColorRect(Size(40, 40), Color.RED, expand=Expand.BOTH))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].width, 200)

    def test_single_expanding_single_direction(self):
        box = HBox()
        box.add_widget(ColorRect(Size(40, 40), Color.RED, expand=Expand.HORIZONTAL))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].width, 200)

    def test_single_expanding_wrong_direction(self):
        box = HBox()
        box.add_widget(ColorRect(Size(40, 40), Color.RED, expand=Expand.VERTICAL))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].width, 40)

    def test_two_widgets_one_expanding(self):
        box = HBox()
        box.add_widget(ColorRect(Size(40, 40), Color.RED, expand=Expand.HORIZONTAL))
        box.add_widget(ColorRect(Size(40, 40), Color.RED))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].width, 160)
        self.assertEqual(sizes[1].width, 40)

    def test_two_widgets_both_expanding(self):
        box = HBox()
        box.add_widget(ColorRect(Size(40, 40), Color.RED, expand=Expand.HORIZONTAL))
        box.add_widget(ColorRect(Size(40, 40), Color.RED, expand=Expand.HORIZONTAL))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].width, 100)
        self.assertEqual(sizes[1].width, 100)

    def test_three_widgets_middle_expanding(self):
        box = HBox()
        box.add_widget(ColorRect(Size(40, 40), Color.RED))
        box.add_widget(ColorRect(Size(40, 40), Color.RED, expand=Expand.HORIZONTAL))
        box.add_widget(ColorRect(Size(40, 40), Color.RED))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].width, 40)
        self.assertEqual(sizes[1].width, 120)
        self.assertEqual(sizes[2].width, 40)

    def test_pixel_exact(self):
        box = HBox()
        box.add_widget(ColorRect(Size(20, 40), Color.RED, expand=Expand.HORIZONTAL))
        box.add_widget(ColorRect(Size(20, 40), Color.RED, expand=Expand.HORIZONTAL))
        sizes = box.calculate_sizes(Size(45, 200))
        total_rendered_size = sizes[0].width + sizes[1].width
        self.assertEqual(total_rendered_size, 45)


class TestHBoxHeights(unittest.TestCase):
    def test_single_no_expansion(self):
        box = HBox()
        box.add_widget(ColorRect(Size(20, 30), Color.RED))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].height, 30)

    def test_single_expansion(self):
        box = HBox()
        box.add_widget(ColorRect(Size(20, 30), Color.RED, expand=Expand.VERTICAL))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].height, 200)

    def test_single_wrong_expansion(self):
        box = HBox()
        box.add_widget(ColorRect(Size(20, 30), Color.RED, expand=Expand.HORIZONTAL))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].height, 30)

    def test_two_one_expanding(self):
        # if 2 items are in an HBox, then all children will get the same size height
        # Whether they choose to use it or not is a different thing
        box = HBox()
        box.add_widget(ColorRect(Size(20, 30), Color.RED, expand=Expand.VERTICAL))
        box.add_widget(ColorRect(Size(20, 30), Color.RED))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].height, 200)
        self.assertEqual(sizes[1].height, 200)

    def test_two_both_expanding(self):
        box = HBox()
        box.add_widget(ColorRect(Size(20, 30), Color.RED, expand=Expand.VERTICAL))
        box.add_widget(ColorRect(Size(20, 30), Color.RED, expand=Expand.VERTICAL))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].height, 200)
        self.assertEqual(sizes[1].height, 200)


class TestExpandingHBox(unittest.TestCase):
    box1 = HBox(expand=Expand.HORIZONTAL)
    box2 = HBox(expand=Expand.NONE)
    box1.add_widget(ColorRect(Size(10, 10), Color.RED))
    box2.add_widget(ColorRect(Size(10, 10), Color.RED))
    box3 = HBox(widgets=[box1, box2])
