import pygame

from gui.screens.screen_activity import Screen
from gui.simulation_graphics.colors import RED


class AlgosError(Screen):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen, background=RED)

    def display(self):
        self.screen.fill(self.background)
        # write the text
        self.write_text("You must choose at least one algorithm", self.screen.get_width() // 2,
                        self.screen.get_height() // 2, 35)
        # Draws the surface object to the screen.
        pygame.display.update()
        # block until click
        self.default_click_disappear()
