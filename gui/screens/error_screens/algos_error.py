import pygame

from gui.screens.error_screens.error_screen import ErrorScreen


class AlgosError(ErrorScreen):

    def display(self):
        self.screen.fill(self.background)
        # write the text
        self.write_text("You must choose at least one algorithm", self.screen.get_width() // 2,
                        self.screen.get_height() // 2, 35)
        # Draws the surface object to the screen.
        pygame.display.update()
        # block until click
        self.default_click_disappear()
