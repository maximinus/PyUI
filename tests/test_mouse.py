import unittest

from pyui.helpers import Position, Mouse


class TestMouse(unittest.TestCase):
    def test_init(self):
        # Test initial state
        mouse = Mouse()
        self.assertEqual(mouse.position.x, 0)
        self.assertEqual(mouse.position.y, 0)
        self.assertFalse(mouse.left_button)
        self.assertFalse(mouse.middle_button)
        self.assertFalse(mouse.right_button)
    
    def test_update_position(self):
        # Test updating mouse position
        mouse = Mouse()
        
        # Update with new position
        mouse.update((100, 150), (False, False, False))
        
        # Check that position was updated
        self.assertEqual(mouse.position.x, 100)
        self.assertEqual(mouse.position.y, 150)
        self.assertEqual(mouse.position, Position(100, 150))
    
    def test_update_buttons(self):
        # Test updating button states
        mouse = Mouse()
        
        # Test left button pressed
        mouse.update((0, 0), (True, False, False))
        self.assertTrue(mouse.left_button)
        self.assertFalse(mouse.middle_button)
        self.assertFalse(mouse.right_button)
        
        # Test middle button pressed
        mouse.update((0, 0), (False, True, False))
        self.assertFalse(mouse.left_button)
        self.assertTrue(mouse.middle_button)
        self.assertFalse(mouse.right_button)
        
        # Test right button pressed
        mouse.update((0, 0), (False, False, True))
        self.assertFalse(mouse.left_button)
        self.assertFalse(mouse.middle_button)
        self.assertTrue(mouse.right_button)
        
        # Test multiple buttons pressed
        mouse.update((0, 0), (True, True, True))
        self.assertTrue(mouse.left_button)
        self.assertTrue(mouse.middle_button)
        self.assertTrue(mouse.right_button)
        
        # Test all buttons released
        mouse.update((0, 0), (False, False, False))
        self.assertFalse(mouse.left_button)
        self.assertFalse(mouse.middle_button)
        self.assertFalse(mouse.right_button)
    
    def test_update_position_and_buttons(self):
        # Test updating both position and buttons at once
        mouse = Mouse()
        
        mouse.update((100, 150), (True, False, True))
        
        # Check position
        self.assertEqual(mouse.position.x, 100)
        self.assertEqual(mouse.position.y, 150)
        
        # Check buttons
        self.assertTrue(mouse.left_button)
        self.assertFalse(mouse.middle_button)
        self.assertTrue(mouse.right_button)
        
    def test_consecutive_updates(self):
        # Test multiple consecutive updates
        mouse = Mouse()
        
        # First update
        mouse.update((10, 20), (True, False, False))
        self.assertEqual(mouse.position, Position(10, 20))
        self.assertTrue(mouse.left_button)
        
        # Second update
        mouse.update((30, 40), (False, True, False))
        self.assertEqual(mouse.position, Position(30, 40))
        self.assertFalse(mouse.left_button)
        self.assertTrue(mouse.middle_button)
        
        # Third update
        mouse.update((50, 60), (False, False, True))
        self.assertEqual(mouse.position, Position(50, 60))
        self.assertFalse(mouse.left_button)
        self.assertFalse(mouse.middle_button)
        self.assertTrue(mouse.right_button)
