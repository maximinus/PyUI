import unittest
from pyui.helpers import Mouse, Position

class TestMouse(unittest.TestCase):
    
    def setUp(self):
        self.mouse = Mouse()
    
    def test_initial_state(self):
        self.assertEqual(self.mouse.position.x, 0)
        self.assertEqual(self.mouse.position.y, 0)
        self.assertEqual(self.mouse.old_position.x, 0)
        self.assertEqual(self.mouse.old_position.y, 0)
        self.assertFalse(self.mouse.current.left)
        self.assertFalse(self.mouse.current.middle)
        self.assertFalse(self.mouse.current.right)
        self.assertFalse(self.mouse.previous.left)
        self.assertFalse(self.mouse.previous.middle)
        self.assertFalse(self.mouse.previous.right)
    
    def test_update_position(self):
        self.mouse.update((100, 200), (False, False, False))
        self.assertEqual(self.mouse.position.x, 100)
        self.assertEqual(self.mouse.position.y, 200)
        self.assertEqual(self.mouse.old_position.x, 0)
        self.assertEqual(self.mouse.old_position.y, 0)
        
        self.mouse.update((150, 250), (False, False, False))
        self.assertEqual(self.mouse.position.x, 150)
        self.assertEqual(self.mouse.position.y, 250)
        self.assertEqual(self.mouse.old_position.x, 100)
        self.assertEqual(self.mouse.old_position.y, 200)
    
    def test_set_left(self):
        self.mouse.update((0, 0), (True, False, False))
        self.assertTrue(self.mouse.current.left)
        self.assertFalse(self.mouse.current.middle)
        self.assertFalse(self.mouse.current.right)
        
    def test_set_middle(self):
        self.mouse.update((0, 0), (False, True, False))
        self.assertFalse(self.mouse.current.left)
        self.assertTrue(self.mouse.current.middle)
        self.assertFalse(self.mouse.current.right)
        
    def test_set_right(self):
        self.mouse.update((0, 0), (False, False, True))
        self.assertFalse(self.mouse.current.left)
        self.assertFalse(self.mouse.current.middle)
        self.assertTrue(self.mouse.current.right)
        
    def test_set_all_buttons(self):
        self.mouse.update((0, 0), (True, True, True))
        self.assertTrue(self.mouse.current.left)
        self.assertTrue(self.mouse.current.middle)
        self.assertTrue(self.mouse.current.right)
    
    def test_left_click_down(self):
        self.mouse.update((0, 0), (False, False, False))
        self.mouse.update((0, 0), (True, False, False))
        self.assertTrue(self.mouse.left_click_down)
        self.assertFalse(self.mouse.left_click_up)
        
    def test_left_click_up(self):
        self.mouse.update((0, 0), (True, False, False))
        self.mouse.update((0, 0), (False, False, False))
        self.assertFalse(self.mouse.left_click_down)
        self.assertTrue(self.mouse.left_click_up)

    def test_middle_click_down(self):
        # Test middle click down
        self.mouse.update((0, 0), (False, False, False))
        self.mouse.update((0, 0), (False, True, False))
        self.assertTrue(self.mouse.middle_click_down)
        self.assertFalse(self.mouse.middle_click_up)
    
    def test_middle_click_up(self):
        self.mouse.update((0, 0), (False, True, False))
        self.mouse.update((0, 0), (False, False, False))
        self.assertFalse(self.mouse.middle_click_down)
        self.assertTrue(self.mouse.middle_click_up)
    
    def test_right_click_down(self):
        # Test right click down
        self.mouse.update((0, 0), (False, False, False))
        self.mouse.update((0, 0), (False, False, True))
        self.assertTrue(self.mouse.right_click_down)
        self.assertFalse(self.mouse.right_click_up)
    
    def test_right_click_up(self):
        self.mouse.update((0, 0), (False, False, True))
        self.mouse.update((0, 0), (False, False, False))
        self.assertFalse(self.mouse.right_click_down)
        self.assertTrue(self.mouse.right_click_up)
    
    def test_no_click_when_held(self):
        # Press button and check click down is true
        self.mouse.update((0, 0), (False, False, False))
        self.mouse.update((0, 0), (True, False, False))
        self.assertTrue(self.mouse.left_click_down)
        
        # Still holding button, check click down is now false
        self.mouse.update((0, 0), (True, False, False))
        self.assertFalse(self.mouse.left_click_down)
        self.assertFalse(self.mouse.left_click_up)
