from pygame import Surface

from pyui.test_helper import PyuiTest
from pyui.assets import get_image, get_nine_patch, file_cache

class TestAssets(PyuiTest):
    def test_load_image(self):
        image = get_image("dog.png")
        self.assertTrue(isinstance(image, Surface))
    
    def test_load_nine_patch(self):
        nine_patch = get_nine_patch("button.png")
        self.assertTrue(isinstance(nine_patch, Surface))
    
    def test_image_cache(self):
        file_cache.clear()
        get_image("dog.png")
        self.assertTrue("dog.png" in file_cache.images)

    def test_cache_works(self):
        file_cache.clear()
        img1 = get_image("dog.png")
        img2 = get_image("dog.png")
        self.assertIs(img1, img2)
