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
        self.assertFalse(self.mouse.left.state)
        self.assertFalse(self.mouse.middle.state)
        self.assertFalse(self.mouse.right.state)
        self.assertFalse(self.mouse.left.up)
        self.assertFalse(self.mouse.left.down)
        self.assertFalse(self.mouse.middle.up)
        self.assertFalse(self.mouse.middle.down)
        self.assertFalse(self.mouse.right.up)
        self.assertFalse(self.mouse.right.down)
    
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
        self.assertTrue(self.mouse.left.state)
        self.assertFalse(self.mouse.middle.state)
        self.assertFalse(self.mouse.right.state)
        
    def test_set_middle(self):
        self.mouse.update((0, 0), (False, True, False))
        self.assertFalse(self.mouse.left.state)
        self.assertTrue(self.mouse.middle.state)
        self.assertFalse(self.mouse.right.state)
        
    def test_set_right(self):
        self.mouse.update((0, 0), (False, False, True))
        self.assertFalse(self.mouse.left.state)
        self.assertFalse(self.mouse.middle.state)
        self.assertTrue(self.mouse.right.state)
        
    def test_set_all_buttons(self):
        self.mouse.update((0, 0), (True, True, True))
        self.assertTrue(self.mouse.left.state)
        self.assertTrue(self.mouse.middle.state)
        self.assertTrue(self.mouse.right.state)
    
    def test_left_button_down(self):
        self.mouse.update((0, 0), (False, False, False))
        self.mouse.update((0, 0), (True, False, False))
        self.assertTrue(self.mouse.left.down)
        self.assertFalse(self.mouse.left.up)
        
    def test_left_button_up(self):
        self.mouse.update((0, 0), (True, False, False))
        self.mouse.update((0, 0), (False, False, False))
        self.assertFalse(self.mouse.left.down)
        self.assertTrue(self.mouse.left.up)

    def test_middle_button_down(self):
        self.mouse.update((0, 0), (False, False, False))
        self.mouse.update((0, 0), (False, True, False))
        self.assertTrue(self.mouse.middle.down)
        self.assertFalse(self.mouse.middle.up)
    
    def test_middle_button_up(self):
        self.mouse.update((0, 0), (False, True, False))
        self.mouse.update((0, 0), (False, False, False))
        self.assertFalse(self.mouse.middle.down)
        self.assertTrue(self.mouse.middle.up)
    
    def test_right_button_down(self):
        self.mouse.update((0, 0), (False, False, False))
        self.mouse.update((0, 0), (False, False, True))
        self.assertTrue(self.mouse.right.down)
        self.assertFalse(self.mouse.right.up)
    
    def test_right_button_up(self):
        self.mouse.update((0, 0), (False, False, True))
        self.mouse.update((0, 0), (False, False, False))
        self.assertFalse(self.mouse.right.down)
        self.assertTrue(self.mouse.right.up)
    
    def test_no_button_events_when_held(self):
        # Press button and check down is true
        self.mouse.update((0, 0), (False, False, False))
        self.mouse.update((0, 0), (True, False, False))
        self.assertTrue(self.mouse.left.down)
        
        # Still holding button, check down is now false but state is still true
        self.mouse.update((0, 0), (True, False, False))
        self.assertFalse(self.mouse.left.down)
        self.assertFalse(self.mouse.left.up)
        self.assertTrue(self.mouse.left.state)
