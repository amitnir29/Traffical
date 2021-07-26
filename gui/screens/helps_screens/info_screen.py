import pygame

from gui.screens.screen_activity import Screen

HELP_START_PORTION = 3
HELP_TEXT_SIZE = 20
LINE_HEIGHT = HELP_TEXT_SIZE + 5


class InfoScreen(Screen):

    def display(self):
        self.screen.fill(self.background)
        # write the text
        self.write_text("About us", self.screen.get_width() // 2, self.screen.get_height() // 8, 100)

        self.write_text("Traffical is a project developed by 4 students from Bar Ilan University",
                        self.screen.get_width() // 2, self.screen.get_height() // HELP_START_PORTION, HELP_TEXT_SIZE)
        self.write_text("as their final project in their Bachelor's degree.",
                        self.screen.get_width() // 2, self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT,
                        HELP_TEXT_SIZE)

        self.write_text("Traffical attempts to change the traffic light systems",
                        self.screen.get_width() // 2, self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT * 3,
                        HELP_TEXT_SIZE)
        self.write_text("in our world, by making it dynamic,",
                        self.screen.get_width() // 2, self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT * 4,
                        HELP_TEXT_SIZE)
        self.write_text("and finding algorithms that improve the current situation.",
                        self.screen.get_width() // 2, self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT * 5,
                        HELP_TEXT_SIZE)

        self.write_text("In this program you can run a simulation with algorithm of your choosing,",
                        self.screen.get_width() // 2, self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT * 7,
                        HELP_TEXT_SIZE)
        self.write_text("compare algorithms and see the results.",
                        self.screen.get_width() // 2, self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT * 8,
                        HELP_TEXT_SIZE)

        self.write_text("click to go back", self.screen.get_width() // 2, 9 * self.screen.get_height() // 10, 40)
        # Draws the surface object to the screen.
        pygame.display.update()
        # block until click
        self.default_click_disappear()
