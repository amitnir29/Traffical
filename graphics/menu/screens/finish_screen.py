import pygame

from graphics.menu.screens.screen_activity import Screen


class FinishScreen(Screen):

    def display(self):
        self.screen.fill(self.background)
        # write the text
        self.write_text("Goodbye!", self.screen.get_width() // 2, self.screen.get_height() // 2, 140)
        # Draws the surface object to the screen.
        pygame.display.update()
        # block until click
        self.default_click_disappear()
