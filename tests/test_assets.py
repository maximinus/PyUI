import unittest

from pygame import Surface

from pyui.assets import get_image, get_nine_patch


class TestAssets(unittest.TestCase):
    def test_load_image(self):
        image = get_image("dog.png")
        self.assertTrue(isinstance(image, Surface))
    
    def test_load_nine_patch(self):
        nine_patch = get_nine_patch("button.png")
        self.assertTrue(isinstance(nine_patch, Surface))
