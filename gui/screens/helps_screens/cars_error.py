import pygame

from gui.screens.screen_activity import Screen


class CarsError(Screen):

    def display(self):
        self.screen.fill(self.background)
        # write the text
        self.write_text("Could not find paths of this length in this map", self.screen.get_width() // 2,
                        self.screen.get_height() // 2 - 30, 30)
        self.write_text("Please choose a shorter path length", self.screen.get_width() // 2,
                        self.screen.get_height() // 2 + 50, 40)
        # Draws the surface object to the screen.
        pygame.display.update()
        # block until click
        self.default_click_disappear()
