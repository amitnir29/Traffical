import pygame

from gui.screens.screen_activity import Screen


class MapsHelp(Screen):

    def display(self):
        self.screen.fill(self.background)
        # write the text
        self.write_text("In this screen you", self.screen.get_width() // 2, self.screen.get_height() // 4, 60)
        self.write_text("choose a map", self.screen.get_width() // 2, self.screen.get_height() // 4 + 60, 60)
        self.write_text("which all the", self.screen.get_width() // 2, self.screen.get_height() // 4 + 120, 60)
        self.write_text("cars will run in", self.screen.get_width() // 2, self.screen.get_height() // 4 + 180, 60)
        self.write_text("click to go back", self.screen.get_width() // 2, 3 * self.screen.get_height() // 4, 40)
        # Draws the surface object to the screen.
        pygame.display.update()
        # block until click
        self.default_click_disappear()
