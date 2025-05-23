import sys
import pygame


def wait_for_keypress():
    # Wait for a keypress event
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(True)
            if event.type == pygame.KEYDOWN:
                return
