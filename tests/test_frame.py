import unittest
from unittest.mock import Mock, patch

import pygame
from pygame import Surface

from pyui.test_helper import PyuiTest
from pyui.widget import Widget
from pyui.widgets.frame import Frame
from pyui.widgets.nine_patch import NinePatchData
from pyui.helpers import Size, Position, Margin, Expand, Align


def create_test_image(width, height):  
    """Create a simple test image with a solid color."""
    image = Surface((width, height), flags=pygame.SRCALPHA)
    image.fill((255, 0, 0, 255))
    return image


class TestFrame(PyuiTest):
    def setUp(self):
        super().setUp()
        self.mock_image = create_test_image(20, 20)
        self.nine_patch_data = NinePatchData(
            top=5, bottom=5, left=5, right=5, image=self.mock_image
        )
        self.mock_child = Mock(spec=Widget)
        self.mock_child.min_size = Size(30, 30)
        self.mock_child.margin = Margin()
        self.mock_child.parent = None
        
    def test_init_sets_child_parent(self):
        frame = Frame(self.mock_child, self.nine_patch_data)
        self.assertEqual(frame.child.parent, frame)
        
    def test_min_size_calculation(self):
        frame = Frame(self.mock_child, self.nine_patch_data)
        expected_width = 30 + 5 + 5  # child width + left + right
        expected_height = 30 + 5 + 5  # child height + top + bottom
        self.assertEqual(frame.min_size, Size(expected_width, expected_height))

    def test_min_size_with_margin(self):
        margin = Margin(1, 2, 3, 4)
        frame = Frame(self.mock_child, self.nine_patch_data, margin=margin)
        expected_width = 30 + 5 + 5 + margin.width
        expected_height = 30 + 5 + 5 + margin.height
        self.assertEqual(frame.min_size, Size(expected_width, expected_height))
        
    def test_render_calls_child_render(self):
        frame = Frame(self.mock_child, self.nine_patch_data)
        destination = Surface((100, 100))
        frame.render(self.mouse, destination, Position(0, 0), Size(100, 100))
        self.mock_child.render.assert_called_once()
        
    def test_render_positions_child_correctly(self):
        frame = Frame(self.mock_child, self.nine_patch_data)
        destination = Surface((100, 100))
        frame.render(self.mouse, destination, Position(0, 0), Size(100, 100))
        
        # Extract the position argument from the child's render call
        _, args, _ = self.mock_child.render.mock_calls[0]
        position_arg = args[2]
        
        # Child should be positioned at (left, top) of nine patch
        self.assertEqual(position_arg.x, 5)
        self.assertEqual(position_arg.y, 5)
