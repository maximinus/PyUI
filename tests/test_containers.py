import unittest

from pygame import Surface

from pyui.widgets import HBox, ColorRect
from pyui.helpers import Margin, Position, Size, Expand
from pyui.widgets.containers import split_pixels
from pyui.test_helper import PyuiTest


class TestSplitPixels(unittest.TestCase):
    def test_no_children(self):
        result = split_pixels(0, 10)
        self.assertEqual(result, [])

    def test_one_child(self):
        result = split_pixels(1, 10)
        self.assertEqual(result, [10])

    def test_two_children_even(self):
        result = split_pixels(2, 10)
        self.assertEqual(result, [5, 5])

    def test_two_children_odd(self):
        result = split_pixels(2, 11)
        self.assertEqual(result, [6, 5])

    def test_three_children_even(self):
        result = split_pixels(3, 12)
        self.assertEqual(result, [4, 4, 4])

    def test_three_children_odd(self):
        result = split_pixels(3, 13)
        self.assertEqual(result, [5, 4, 4])
    
    def test_failing_example(self):
        result = split_pixels(2, 60)
        self.assertEqual(result, [30, 30])


class TestHBox(PyuiTest):
    # many tests here to get things right
    def test_single_box_no_margins(self):
        box = HBox(spacing=0, margin=Margin(0, 0, 0, 0))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(50, 50)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(0, 0), Size(100, 100))
        self.assertPixel(image, Position(0, 0), (255, 0, 0))
        self.assertPixel(image, Position(50, 0), (0, 0, 0))

    def test_single_box_with_margins(self):
        box = HBox(spacing=0, margin=Margin(10, 10, 10, 10))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(50, 50)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(0, 0), Size(100, 100))
        # With margins, the box should start at (10, 10)
        self.assertPixel(image, Position(0, 0), (0, 0, 0))
        self.assertPixel(image, Position(10, 10), (255, 0, 0))
        self.assertPixel(image, Position(60, 10), (0, 0, 0))

    def test_single_box_with_left_margin(self):
        box = HBox(spacing=0, margin=Margin(15, 0, 0, 0))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(50, 50)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(0, 0), Size(100, 100))
        # With left margin, the box should start at (15, 0)
        self.assertPixel(image, Position(0, 0), (0, 0, 0))
        self.assertPixel(image, Position(15, 0), (255, 0, 0))
        self.assertPixel(image, Position(65, 0), (0, 0, 0))

    def test_single_box_with_top_margin(self):
        box = HBox(spacing=0, margin=Margin(0, 0, 20, 0))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(50, 50)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(0, 0), Size(100, 100))
        # With top margin, the box should start at (0, 20)
        self.assertPixel(image, Position(0, 0), (0, 0, 0))
        self.assertPixel(image, Position(0, 20), (255, 0, 0))
        self.assertPixel(image, Position(50, 20), (0, 0, 0))

    def test_single_box_with_position_offset(self):
        box = HBox(spacing=0, margin=Margin(0, 0, 0, 0))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(50, 50)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(10, 10), Size(80, 80))
        # With position offset, the box should start at (10, 10)
        self.assertPixel(image, Position(0, 0), (0, 0, 0))
        self.assertPixel(image, Position(10, 10), (255, 0, 0))
        self.assertPixel(image, Position(60, 10), (0, 0, 0))

    def test_two_boxes_no_spacing(self):
        box = HBox(spacing=0, margin=Margin(0, 0, 0, 0))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(30, 50)))
        box.add_child(ColorRect(color=(0, 255, 0), size=Size(30, 50)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(0, 0), Size(100, 100))
        # First box at (0, 0), second box at (30, 0)
        self.assertPixel(image, Position(0, 0), (255, 0, 0))
        self.assertPixel(image, Position(30, 0), (0, 255, 0))
        self.assertPixel(image, Position(60, 0), (0, 0, 0))

    def test_two_boxes_with_spacing(self):
        box = HBox(spacing=10, margin=Margin(0, 0, 0, 0))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(30, 50)))
        box.add_child(ColorRect(color=(0, 255, 0), size=Size(30, 50)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(0, 0), Size(100, 100))
        # First box at (0, 0), 10px spacing, second box at (40, 0)
        self.assertPixel(image, Position(0, 0), (255, 0, 0))
        self.assertPixel(image, Position(30, 0), (0, 0, 0))  # Spacing
        self.assertPixel(image, Position(40, 0), (0, 255, 0))
        self.assertPixel(image, Position(70, 0), (0, 0, 0))

    def test_three_boxes_with_spacing_and_margin(self):
        box = HBox(spacing=5, margin=Margin(5, 5, 5, 5))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(20, 40)))
        box.add_child(ColorRect(color=(0, 255, 0), size=Size(20, 40)))
        box.add_child(ColorRect(color=(0, 0, 255), size=Size(20, 40)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(0, 0), Size(100, 100))
        # Boxes at (5,5), (30,5), and (55,5) with 5px spacing and 5px margin
        self.assertPixel(image, Position(5, 5), (255, 0, 0))
        self.assertPixel(image, Position(25, 5), (0, 0, 0))  # Spacing
        self.assertPixel(image, Position(30, 5), (0, 255, 0))
        self.assertPixel(image, Position(50, 5), (0, 0, 0))  # Spacing
        self.assertPixel(image, Position(55, 5), (0, 0, 255))
        self.assertPixel(image, Position(75, 5), (0, 0, 0))

    def test_expanding_child(self):
        box = HBox(spacing=0, margin=Margin(0, 0, 0, 0))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(30, 50), expand=Expand.HORIZONTAL))
        box.add_child(ColorRect(color=(0, 255, 0), size=Size(30, 50)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(0, 0), Size(100, 100))
        # First box should expand to fill available space (40px extra)
        self.assertPixel(image, Position(69, 0), (255, 0, 0))
        self.assertPixel(image, Position(70, 0), (0, 255, 0))

    def test_multiple_expanding_children(self):
        box = HBox(spacing=0, margin=Margin(0, 0, 0, 0))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(20, 50), expand=Expand.HORIZONTAL))
        box.add_child(ColorRect(color=(0, 255, 0), size=Size(20, 50), expand=Expand.HORIZONTAL))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(0, 0), Size(100, 100))
        # Both boxes should expand equally (30px extra each)
        self.assertPixel(image, Position(0, 0), (255, 0, 0))
        self.assertPixel(image, Position(49, 0), (255, 0, 0))
        self.assertPixel(image, Position(50, 0), (0, 255, 0))
        self.assertPixel(image, Position(99, 0), (0, 255, 0))

    def test_uneven_expanding_children(self):
        box = HBox(spacing=0, margin=Margin(0, 0, 0, 0))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(20, 50), expand=Expand.HORIZONTAL))
        box.add_child(ColorRect(color=(0, 255, 0), size=Size(20, 50), expand=Expand.HORIZONTAL))
        box.add_child(ColorRect(color=(0, 0, 255), size=Size(20, 50)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(0, 0), Size(100, 100))
        # First two boxes should expand by 20px each
        self.assertPixel(image, Position(0, 0), (255, 0, 0))
        self.assertPixel(image, Position(39, 0), (255, 0, 0))
        self.assertPixel(image, Position(40, 0), (0, 255, 0))
        self.assertPixel(image, Position(79, 0), (0, 255, 0))
        self.assertPixel(image, Position(80, 0), (0, 0, 255))

    def test_vertical_expanding_has_no_effect(self):
        box = HBox(spacing=0, margin=Margin(0, 0, 0, 0))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(30, 30), expand=Expand.VERTICAL))
        box.add_child(ColorRect(color=(0, 255, 0), size=Size(30, 30)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(0, 0), Size(100, 100))
        # Vertical expansion shouldn't affect horizontal layout
        self.assertPixel(image, Position(0, 0), (255, 0, 0))
        self.assertPixel(image, Position(30, 0), (0, 255, 0))
        self.assertPixel(image, Position(60, 0), (0, 0, 0))

    def test_both_directional_expand(self):
        box = HBox(spacing=0, margin=Margin(0, 0, 0, 0))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(30, 30), expand=Expand.BOTH))
        box.add_child(ColorRect(color=(0, 255, 0), size=Size(30, 30)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(0, 0), Size(100, 100))
        # BOTH expansion should include horizontal
        self.assertPixel(image, Position(0, 0), (255, 0, 0))
        self.assertPixel(image, Position(69, 0), (255, 0, 0))
        self.assertPixel(image, Position(70, 0), (0, 255, 0))

    def test_different_height_children(self):
        box = HBox(spacing=0, margin=Margin(0, 0, 0, 0))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(30, 20)))
        box.add_child(ColorRect(color=(0, 255, 0), size=Size(30, 40)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(0, 0), Size(100, 100))
        # Both children should align at the top
        self.assertPixel(image, Position(0, 0), (255, 0, 0))
        self.assertPixel(image, Position(0, 19), (255, 0, 0))
        self.assertPixel(image, Position(0, 20), (0, 0, 0))
        self.assertPixel(image, Position(30, 0), (0, 255, 0))
        self.assertPixel(image, Position(30, 39), (0, 255, 0))
        self.assertPixel(image, Position(30, 40), (0, 0, 0))

    def test_spacing_without_margin(self):
        box = HBox(spacing=10, margin=Margin(0, 0, 0, 0))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(20, 20)))
        box.add_child(ColorRect(color=(0, 255, 0), size=Size(20, 20)))
        box.add_child(ColorRect(color=(0, 0, 255), size=Size(20, 20)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(0, 0), Size(100, 100))
        # 10px spacing between each child
        self.assertPixel(image, Position(0, 0), (255, 0, 0))
        self.assertPixel(image, Position(20, 0), (0, 0, 0))  # Spacing
        self.assertPixel(image, Position(30, 0), (0, 255, 0))
        self.assertPixel(image, Position(50, 0), (0, 0, 0))  # Spacing
        self.assertPixel(image, Position(60, 0), (0, 0, 255))

    def test_min_size_calculation(self):
        box = HBox(spacing=5, margin=Margin(10, 10, 10, 10))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(20, 30)))
        box.add_child(ColorRect(color=(0, 255, 0), size=Size(20, 20)))
        # Min size should be children sizes + spacing + margins
        # (20 + 20) + 5 + (10 + 10) width, 30 + (10 + 10) height
        self.assertEqual(box.min_size, Size(65, 50))

    def test_min_size_with_single_child(self):
        box = HBox(spacing=5, margin=Margin(10, 10, 10, 10))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(20, 30)))
        # No spacing is added with a single child
        # 20 + (10 + 10) width, 30 + (10 + 10) height
        self.assertEqual(box.min_size, Size(40, 50))

    def test_min_size_with_no_children(self):
        box = HBox(spacing=5, margin=Margin(10, 10, 10, 10))
        # Just the margins
        self.assertEqual(box.min_size, Size(20, 20))

    def test_add_and_remove_child(self):
        box = HBox(spacing=0, margin=Margin(0, 0, 0, 0))
        child = ColorRect(color=(255, 0, 0), size=Size(20, 20))
        box.add_child(child)
        self.assertEqual(len(box.children), 1)
        self.assertEqual(child.parent, box)
        box.remove_child(child)
        self.assertEqual(len(box.children), 0)
        self.assertEqual(child.parent, None)

    def test_not_enough_space(self):
        box = HBox(spacing=0, margin=Margin(0, 0, 0, 0))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(60, 50)))
        box.add_child(ColorRect(color=(0, 255, 0), size=Size(60, 50)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        box.render(image, Position(0, 0), Size(100, 100))
        # Children should render but not expand beyond their natural size
        self.assertPixel(image, Position(0, 0), (255, 0, 0))
        self.assertPixel(image, Position(59, 0), (255, 0, 0))
        self.assertPixel(image, Position(60, 0), (0, 255, 0))
        
    def test_zero_size_container(self):
        box = HBox(spacing=0, margin=Margin(0, 0, 0, 0))
        box.add_child(ColorRect(color=(255, 0, 0), size=Size(30, 50)))
        image = Surface((100, 100))
        image.fill((0, 0, 0))
        # Providing zero size should still render properly based on min_size
        box.render(image, Position(0, 0), Size(0, 0))
        self.assertPixel(image, Position(0, 0), (255, 0, 0))
