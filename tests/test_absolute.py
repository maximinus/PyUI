import unittest
from unittest.mock import MagicMock, patch

import pygame
from pygame import Surface

from pyui.widgets.absolute import Absolute
from pyui.widget import Widget
from pyui.helpers import Position, Size, Mouse
from pyui.test_helper import PyuiTest


class TestAbsoluteInit(unittest.TestCase):
    def test_basic_initialization(self):
        child = Widget()
        position = Position(10, 20)
        absolute = Absolute(child, position)
        
        self.assertEqual(absolute.offset, position)
        self.assertEqual(absolute.child, child)
    
    def test_rejects_expand_parameter(self):
        child = Widget()
        with self.assertRaises(AssertionError) as context:
            Absolute(child, Position(0, 0), expand="any_value")
        self.assertIn("Absolute layout does not support expand", str(context.exception))
    
    def test_rejects_align_parameter(self):
        child = Widget()
        with self.assertRaises(AssertionError) as context:
            Absolute(child, Position(0, 0), align="any_value")
        self.assertIn("Absolute layout does not support align", str(context.exception))
    
    def test_rejects_background_parameter(self):
        child = Widget()
        with self.assertRaises(AssertionError) as context:
            Absolute(child, Position(0, 0), background="any_value")
        self.assertIn("Absolute layout does not support background", str(context.exception))
    
    def test_rejects_margin_parameter(self):
        child = Widget()
        with self.assertRaises(AssertionError) as context:
            Absolute(child, Position(0, 0), margin="any_value")
        self.assertIn("Absolute layout does not support margin", str(context.exception))


class TestAbsoluteAddChild(unittest.TestCase):
    def test_rejects_adding_second_child(self):
        child = Widget()
        absolute = Absolute(child, Position(0, 0))
        
        with self.assertRaises(AssertionError) as context:
            absolute.add_child(Widget())
        self.assertIn("Absolute layout can only have one child", str(context.exception))


class TestAbsoluteRendering(PyuiTest):
    def test_renders_child_with_offset(self):
        # Create a mock child widget
        child = MagicMock(spec=Widget)
        
        # Create absolute widget with an offset
        offset = Position(10, 15)
        absolute = Absolute(child, offset)
        
        # Prepare test parameters
        mouse = Mouse()
        destination = Surface((100, 100))
        position = Position(5, 5)
        size = Size(50, 50)
        
        # Call render method
        absolute.render(mouse, destination, position, size)
        
        # Verify child's render was called with the correct offset position
        expected_position = Position(15, 20)  # position + offset
        child.render.assert_called_once()
        call_args = child.render.call_args[0]
        self.assertEqual(call_args[0], mouse)
        self.assertEqual(call_args[1], destination)
        self.assertEqual(call_args[2], expected_position)
        self.assertEqual(call_args[3], size)
    
    def test_position_offset_calculation(self):
        # Create a real widget that will draw a visible color
        from pyui.widgets import ColorRect
        
        # Create test objects
        child = ColorRect(color=(255, 0, 0), size=Size(10, 10))
        absolute = Absolute(child, Position(10, 10))
        
        # Create a surface and render
        surface = Surface((100, 100))
        surface.fill((0, 0, 0))  # Black background
        
        # Render at position 0,0
        absolute.render(self.mouse, surface, Position(0, 0), Size(100, 100))
        
        # Check that the color appears at the offset position
        self.assertPixel(surface, Position(10, 10), (255, 0, 0))
        self.assertPixel(surface, Position(19, 19), (255, 0, 0))
        
        # Verify position outside the ColorRect is still black
        self.assertPixel(surface, Position(0, 0), (0, 0, 0))
        self.assertPixel(surface, Position(9, 9), (0, 0, 0))
        self.assertPixel(surface, Position(20, 20), (0, 0, 0))


if __name__ == '__main__':
    unittest.main()
