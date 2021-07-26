import pygame


def create_screen(width, height):
    # Start pygame
    pygame.init()
    pygame.display.set_caption('Traffical')
    screen = pygame.display.set_mode((width, height))
    return screen


def quit_screen():
    pygame.quit()
