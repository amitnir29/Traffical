import pygame

from gui.screens.screen_activity import Screen

TITLE_SCREEN_PORTION = 10
TITLE_TEXT_SIZE = 40


class AlgosHelp(Screen):

    def display(self):
        self.screen.fill(self.background)
        # write the text
        self.write_text("In this screen you choose an", self.screen.get_width() // 2,
                        self.screen.get_height() // TITLE_SCREEN_PORTION, TITLE_TEXT_SIZE)
        self.write_text("algorithm which will determine the ", self.screen.get_width() // 2,
                        self.screen.get_height() // TITLE_SCREEN_PORTION + TITLE_TEXT_SIZE, TITLE_TEXT_SIZE)
        self.write_text("traffic light's colors", self.screen.get_width() // 2,
                        self.screen.get_height() // TITLE_SCREEN_PORTION + TITLE_TEXT_SIZE * 2, TITLE_TEXT_SIZE)
        self.write_text("click to go back", self.screen.get_width() // 2,
                        (TITLE_SCREEN_PORTION - 1) * self.screen.get_height() // TITLE_SCREEN_PORTION, TITLE_TEXT_SIZE)
        # Draws the surface object to the screen.
        pygame.display.update()
        # block until click
        self.default_click_disappear()
