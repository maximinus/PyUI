import unittest
from unittest.mock import patch, MagicMock
import pygame
from pyui.keys import Key, KeyState, keys


class TestKey(unittest.TestCase):
    def test_key_constants(self):
        self.assertEqual(Key.ESCAPE, pygame.K_ESCAPE)
        self.assertEqual(Key.ENTER, pygame.K_RETURN)


class TestKeyState(unittest.TestCase):
    def setUp(self):
        self.keystate = KeyState()
    
    def test_init(self):
        self.assertEqual(self.keystate.pressed, [])
        self.assertEqual(self.keystate.released, [])
        self.assertEqual(self.keystate.mods, pygame.KMOD_NONE)
    
    def test_update(self):
        pressed = [pygame.K_a, pygame.K_b]
        released = [pygame.K_c]
        
        with patch('pygame.key.get_mods', return_value=pygame.KMOD_SHIFT):
            self.keystate.update(pressed, released)
        
        self.assertEqual(self.keystate.pressed, pressed)
        self.assertEqual(self.keystate.released, released)
        self.assertEqual(self.keystate.mods, pygame.KMOD_SHIFT)
    
    def test_is_pressed(self):
        self.keystate.pressed = [pygame.K_a, pygame.K_b]
        
        self.assertTrue(self.keystate.is_pressed(pygame.K_a))
        self.assertTrue(self.keystate.is_pressed(pygame.K_b))
        self.assertFalse(self.keystate.is_pressed(pygame.K_c))
    
    def test_is_released(self):
        self.keystate.released = [pygame.K_a, pygame.K_b]
        
        self.assertTrue(self.keystate.is_released(pygame.K_a))
        self.assertTrue(self.keystate.is_released(pygame.K_b))
        self.assertFalse(self.keystate.is_released(pygame.K_c))
    
    def test_shift_property(self):
        # Test when shift is pressed
        self.keystate.mods = pygame.KMOD_SHIFT
        self.assertTrue(self.keystate.shift)
        
        # Test when shift is not pressed
        self.keystate.mods = pygame.KMOD_NONE
        self.assertFalse(self.keystate.shift)
        
        # Test when shift and other modifiers are pressed
        self.keystate.mods = pygame.KMOD_SHIFT | pygame.KMOD_CTRL
        self.assertTrue(self.keystate.shift)
    
    def test_ctrl_property(self):
        # Test when ctrl is pressed
        self.keystate.mods = pygame.KMOD_CTRL
        self.assertTrue(self.keystate.ctrl)
        
        # Test when ctrl is not pressed
        self.keystate.mods = pygame.KMOD_NONE
        self.assertFalse(self.keystate.ctrl)
        
        # Test when ctrl and other modifiers are pressed
        self.keystate.mods = pygame.KMOD_CTRL | pygame.KMOD_ALT
        self.assertTrue(self.keystate.ctrl)
    
    def test_alt_property(self):
        # Test when alt is pressed
        self.keystate.mods = pygame.KMOD_ALT
        self.assertTrue(self.keystate.alt)
        
        # Test when alt is not pressed
        self.keystate.mods = pygame.KMOD_NONE
        self.assertFalse(self.keystate.alt)
        
        # Test when alt and other modifiers are pressed
        self.keystate.mods = pygame.KMOD_ALT | pygame.KMOD_SHIFT
        self.assertTrue(self.keystate.alt)


class TestGlobalKeysInstance(unittest.TestCase):
    def test_global_keys_instance(self):
        self.assertIsInstance(keys, KeyState)


if __name__ == '__main__':
    unittest.main()
