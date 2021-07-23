import pygame


def create_screen(width, height):
    # Start pygame
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    return screen


def quit_screen():
    pygame.quit()
