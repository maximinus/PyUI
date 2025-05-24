import pygame
from pathlib import Path

ASSETS_FOLDER = Path(__file__).parent / "assets"


def get_image(image_name: str) -> Path:
    image_path = ASSETS_FOLDER / "images" / image_name
    if not image_path.exists():
        raise FileNotFoundError(f"Image '{image_name}' not found in assets.")
    return pygame.image.load(image_path)


def get_nine_patch(patch_name: str) -> Path:
    patch_path = ASSETS_FOLDER / "nine_patch" / patch_name
    if not patch_path.exists():
        raise FileNotFoundError(f"Nine patch '{patch_name}' not found in assets.")
    return pygame.image.load(patch_path)
