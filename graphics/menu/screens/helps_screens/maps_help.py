import pygame

from graphics.menu.screens.screen_activity import Screen


class MapsHelp(Screen):

    def display(self):
        self.screen.fill(self.background)
        # write the text
        self.write_text("This is the", self.screen.get_width() // 2, self.screen.get_height() // 4, 80)
        self.write_text("Maps help screen", self.screen.get_width() // 2, self.screen.get_height() // 4 + 80, 80)
        self.write_text("click to go back", self.screen.get_width() // 2, 3 * self.screen.get_height() // 4, 40)
        # Draws the surface object to the screen.
        pygame.display.update()
        # block until click
        self.default_click_disappear()
