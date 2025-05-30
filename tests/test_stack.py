import unittest
import pygame

from pygame import Surface

from pyui.test_helper import PyuiTest
from pyui.widget import Widget
from pyui.widgets.stack import Stack
from pyui.widgets import ColorRect
from pyui.helpers import Size, Position, Expand, Align, Margin


class TestStack(PyuiTest):
    def test_stack_init(self):
        """Test initialization of Stack widget."""
        # Test default initialization
        stack = Stack()
        self.assertEqual(len(stack.children), 0)
        self.assertIsNone(stack.parent)
        self.assertIsNone(stack.background)
        stack = Stack(background=(255, 0, 0), margin=Margin(5, 10, 15, 20))
        self.assertEqual(stack.background, (255, 0, 0))
        self.assertEqual(stack.margin.left, 5)
        self.assertEqual(stack.margin.right, 10)
        self.assertEqual(stack.margin.top, 15)
        self.assertEqual(stack.margin.bottom, 20)
        
    def test_stack_min_size(self):
        """Test that the min_size is the size of the largest child."""
        stack = Stack()
        # Create widgets with different sizes
        widget1 = ColorRect(color=(255, 0, 0), size=Size(100, 50))
        widget2 = ColorRect(color=(0, 255, 0), size=Size(200, 100))
        stack.add_child(widget1)
        stack.add_child(widget2)
        self.assertEqual(stack.min_size, Size(200, 100))
        
    def test_stack_background(self):
        """Test that the child backgrounds are set to None."""
        stack = Stack(background=(255, 0, 0))        
        widget1 = Widget(background=(0, 255, 0))
        widget2 = Widget(background=(0, 0, 255))
        stack.add_child(widget1)
        stack.add_child(widget2)
        # Child backgrounds should be None
        self.assertIsNone(widget1.background)
        self.assertIsNone(widget2.background)
        # Stack background should remain
        self.assertEqual(stack.background, (255, 0, 0))
    
    def test_add_remove_child(self):
        """Test adding and removing children from Stack."""
        stack = Stack()
        widget = Widget()   
        # Add child
        stack.add_child(widget)
        self.assertEqual(len(stack.children), 1)
        self.assertEqual(stack.children[0], widget)
        self.assertEqual(widget.parent, stack)
        # Remove child
        stack.remove_child(widget)
        self.assertEqual(len(stack.children), 0)
        self.assertIsNone(widget.parent)
    
    def test_min_size_with_margin(self):
        """Test min_size calculation with margins."""
        stack = Stack(margin=Margin(5, 10, 15, 20))
        
        # Empty stack should have min_size equal to margins
        empty_min_size = stack.min_size
        self.assertEqual(empty_min_size.width, 15)  # left + right margin
        self.assertEqual(empty_min_size.height, 35)  # top + bottom margin
    
        widget = ColorRect(color=(0, 0, 255), size=Size(100, 100))
        stack.add_child(widget)
        
        # min_size should now include widget size plus margins
        with_widget_min_size = stack.min_size
        self.assertEqual(with_widget_min_size.width, 115)  # 100 + left + right margin
        self.assertEqual(with_widget_min_size.height, 135)  # 100 + top + bottom margin
        
    def test_render_stacking_order(self):
        """Test that widgets are rendered in the correct stacking order (last on top)."""
        stack = Stack(background=(128, 128, 128))
        
        # Create colored widgets to test rendering order
        red_rect = ColorRect(color=(255, 0, 0), size=Size(100, 100))
        green_rect = ColorRect(color=(0, 255, 0), size=Size(100, 100))
        blue_rect = ColorRect(color=(0, 0, 255), size=Size(100, 100))
        
        stack.add_child(red_rect)
        stack.add_child(green_rect)
        stack.add_child(blue_rect)
        
        # Render the stack to a test surface
        test_surface = Surface((100, 100), flags=pygame.SRCALPHA)
        mouse = self.create_mouse()
        stack.render(mouse, test_surface, Position(0, 0), Size(100, 100))
        
        # The center pixel should be the color of the top widget (blue)
        self.assertPixel(test_surface, Position(50, 50), (0, 0, 255, 255))
        
    def test_rendering_with_margins(self):
        """Test that margins are applied correctly during rendering."""
        stack = Stack(background=(0, 0, 0), margin=Margin(10, 10, 10, 10))
        
        # Create a red rect that fills the entire available area
        red_rect = ColorRect(color=(255, 0, 0), size=Size(80, 80))
        red_rect.expand = Expand.BOTH
        stack.add_child(red_rect)
        
        # Render the stack to a test surface
        test_surface = Surface((100, 100), flags=pygame.SRCALPHA)
        test_surface.fill((255, 255, 255))  # White background
        mouse = self.create_mouse()
        stack.render(mouse, test_surface, Position(0, 0), Size(100, 100))
        
        # Check colors at different positions
        # Inside margins (should be black - the stack's background)
        self.assertPixel(test_surface, Position(5, 5), (0, 0, 0, 255))        
        # Inside content area (should be red)
        self.assertPixel(test_surface, Position(50, 50), (255, 0, 0, 255))

    def test_multiple_children_rendering(self):
        """Test rendering of multiple children in a stack."""
        stack = Stack()
        
        # Create widgets with different alignments
        rect1 = ColorRect(color=(255, 0, 0), size=Size(50, 50))
        rect2 = ColorRect(color=(0, 255, 0), size=Size(50, 50))
        rect3 = ColorRect(color=(0, 0, 255), size=Size(50, 50))
        rect3.align = Align(Align.CENTER, Align.CENTER)
        
        stack.add_child(rect1)
        stack.add_child(rect2)
        stack.add_child(rect3)

        test_surface = Surface((200, 200), flags=pygame.SRCALPHA)
        mouse = self.create_mouse()
        stack.render(mouse, test_surface, Position(0, 0), Size(200, 200))
        # Blue rect (last added) should be visible in the center
        self.assertPixel(test_surface, Position(100, 100), (0, 0, 255, 255))
    
    def test_child_expansion(self):
        """Test that children can expand within the stack."""
        stack = Stack(margin=Margin(5, 5, 5, 5))
        
        # Create a widget that expands to fill available space
        rect = ColorRect(color=(255, 0, 0), size=Size(50, 50))
        rect.expand = Expand.BOTH
        stack.add_child(rect)
        
        # Render the stack with a size larger than the minimum
        test_surface = Surface((200, 200), flags=pygame.SRCALPHA)
        mouse = self.create_mouse()
        stack.render(mouse, test_surface, Position(0, 0), Size(200, 200))
        
        # Check that the rectangle has expanded to fill the available space (minus margins)
        self.assertPixel(test_surface, Position(100, 100), (255, 0, 0, 255))        
        # Check near the edges (inside the margins)
        self.assertNotPixel(test_surface, Position(2, 2), (255, 0, 0, 255))
