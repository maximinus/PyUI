import unittest

from pyui.base import Size, Color, Margin, Expand
from pyui.widgets import VBox, ColorRect


class TestVBoxMinSize(unittest.TestCase):
    def test_empty_width_zero(self):
        box = VBox()
        self.assertEqual(box.min_size.height, 0)

    def test_size_one_widget(self):
        box = VBox()
        box.add_widget(ColorRect(Size(100, 100), Color.RED))
        self.assertEqual(box.min_size.height, 100)

    def test_size_widget_and_margin(self):
        box = VBox()
        box.add_widget(ColorRect(Size(100, 100), Color.RED, margin=Margin(5, 5, 5, 5)))
        self.assertEqual(box.min_size.height, 110)

    def test_size_two_widgets(self):
        box = VBox()
        box.add_widget(ColorRect(Size(100, 135), Color.RED))
        box.add_widget(ColorRect(Size(150, 100), Color.RED))
        self.assertEqual(box.min_size.height, 235)

    def test_size_two_widgets_margin(self):
        box = VBox()
        box.add_widget(ColorRect(Size(10, 10), Color.RED, margin=Margin(3, 3, 3, 3)))
        box.add_widget(ColorRect(Size(25, 20), Color.RED, margin=Margin(5, 5, 5, 5)))
        self.assertEqual(box.min_size.height, 46)


class TestVBoxRenderSizes(unittest.TestCase):
    def test_empty(self):
        box = VBox()
        self.assertEqual(box.calculate_sizes(Size(100, 100)), [])

    def test_single_item_non_expanding(self):
        box = VBox()
        box.add_widget(ColorRect(Size(40, 40), Color.RED))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(len(sizes), 1)
        self.assertEqual(sizes[0].height, 40)

    def test_single_item_expanding(self):
        box = VBox()
        box.add_widget(ColorRect(Size(40, 40), Color.RED, expand=Expand.BOTH))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].height, 200)

    def test_single_expanding_single_direction(self):
        box = VBox()
        box.add_widget(ColorRect(Size(40, 40), Color.RED, expand=Expand.VERTICAL))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].height, 200)

    def test_single_expanding_wrong_direction(self):
        box = VBox()
        box.add_widget(ColorRect(Size(40, 40), Color.RED, expand=Expand.HORIZONTAL))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].height, 40)

    def test_two_widgets_one_expanding(self):
        box = VBox()
        box.add_widget(ColorRect(Size(40, 40), Color.RED, expand=Expand.VERTICAL))
        box.add_widget(ColorRect(Size(40, 40), Color.RED))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].height, 160)
        self.assertEqual(sizes[1].height, 40)

    def test_two_widgets_both_expanding(self):
        box = VBox()
        box.add_widget(ColorRect(Size(40, 40), Color.RED, expand=Expand.VERTICAL))
        box.add_widget(ColorRect(Size(40, 40), Color.RED, expand=Expand.VERTICAL))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].height, 100)
        self.assertEqual(sizes[1].height, 100)

    def test_three_widgets_middle_expanding(self):
        box = VBox()
        box.add_widget(ColorRect(Size(40, 40), Color.RED))
        box.add_widget(ColorRect(Size(40, 40), Color.RED, expand=Expand.VERTICAL))
        box.add_widget(ColorRect(Size(40, 40), Color.RED))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].height, 40)
        self.assertEqual(sizes[1].height, 120)
        self.assertEqual(sizes[2].height, 40)

    def test_pixel_exact(self):
        box = VBox()
        box.add_widget(ColorRect(Size(20, 40), Color.RED, expand=Expand.VERTICAL))
        box.add_widget(ColorRect(Size(20, 40), Color.RED, expand=Expand.VERTICAL))
        sizes = box.calculate_sizes(Size(200, 89))
        total_rendered_size = sizes[0].height + sizes[1].height
        self.assertEqual(total_rendered_size, 89)


class TestVBoxWidths(unittest.TestCase):
    def test_single_no_expansion(self):
        box = VBox()
        box.add_widget(ColorRect(Size(20, 30), Color.RED))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].width, 20)

    def test_single_expansion(self):
        box = VBox()
        box.add_widget(ColorRect(Size(20, 30), Color.RED, expand=Expand.HORIZONTAL))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].width, 200)

    def test_single_wrong_expansion(self):
        box = VBox()
        box.add_widget(ColorRect(Size(20, 30), Color.RED, expand=Expand.VERTICAL))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].width, 20)

    def test_two_one_expanding(self):
        box = VBox()
        box.add_widget(ColorRect(Size(20, 30), Color.RED, expand=Expand.HORIZONTAL))
        box.add_widget(ColorRect(Size(20, 30), Color.RED))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].width, 200)
        self.assertEqual(sizes[1].width, 20)

    def test_two_both_expanding(self):
        box = VBox()
        box.add_widget(ColorRect(Size(20, 30), Color.RED, expand=Expand.HORIZONTAL))
        box.add_widget(ColorRect(Size(20, 30), Color.RED, expand=Expand.HORIZONTAL))
        sizes = box.calculate_sizes(Size(200, 200))
        self.assertEqual(sizes[0].width, 200)
        self.assertEqual(sizes[1].width, 200)


class TestVBoxInVbox(unittest.TestCase):
    def test_simple(self):
        box1 = VBox()
        box1.add_widget(ColorRect(Size(50, 50), Color.RED))
        box2 = VBox(expand=Expand.VERTICAL)
        box2.add_widget(ColorRect(Size(50, 50), Color.RED))
        main_box = VBox()
        main_box.add_widget(box1)
        main_box.add_widget(box2)
        sizes = main_box.calculate_sizes(Size(200, 300))
        self.assertEqual(sizes[0].height, 50)
        self.assertEqual(sizes[1].height, 250)
