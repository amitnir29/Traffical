import pygame


class Window(pygame.sprite.Sprite):
    def __init__(self, screen, scale):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.scale = scale
