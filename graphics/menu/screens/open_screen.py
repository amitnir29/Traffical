import pygame

from graphics.menu.screens.screen_activity import Screen


class OpenScreen(Screen):

    def display(self):
        self.screen.fill(self.background)
        # write the text
        self.write_text("Welcome to", self.screen.get_width() // 2, self.screen.get_height() // 4, 80)
        self.write_text("Traffical", self.screen.get_width() // 2, self.screen.get_height() // 4 + 140, 140)
        self.write_text("click to continue", self.screen.get_width() // 2, 3 * self.screen.get_height() // 4, 40)
        # Draws the surface object to the screen.
        pygame.display.update()
        # run until click
        self.default_click_disappear()
