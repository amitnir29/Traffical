import pygame

from gui.screens.screen_activity import Screen

HELP_START_PORTION = 3
HELP_TEXT_SIZE = 30
LINE_HEIGHT = HELP_TEXT_SIZE + 5


class ConfigurationHelp(Screen):
    def __init__(self, screen: pygame.Surface, is_simulation_mode: bool):
        super().__init__(screen)
        self.simulation_mode = is_simulation_mode

    def display(self):
        self.screen.fill(self.background)
        # write the text
        self.write_text("Choose the configurations", self.screen.get_width() // 2, self.screen.get_height() // 8, 60)
        self.write_text("of the simulation", self.screen.get_width() // 2, self.screen.get_height() // 8 + 60, 60)

        self.write_text("The first slider sets the number of cars",
                        self.screen.get_width() // 2, self.screen.get_height() // HELP_START_PORTION, HELP_TEXT_SIZE)
        self.write_text("that will run in the simulation",
                        self.screen.get_width() // 2, self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT,
                        HELP_TEXT_SIZE)

        self.write_text("The second slider sets the minimum length",
                        self.screen.get_width() // 2,
                        self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT * 3, HELP_TEXT_SIZE)
        self.write_text("of each of the car's path",
                        self.screen.get_width() // 2,
                        self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT * 4, HELP_TEXT_SIZE)

        if self.simulation_mode:
            self.write_text("If the checkbox is set to True, a small image",
                            self.screen.get_width() // 2,
                            self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT * 6, HELP_TEXT_SIZE)
            self.write_text("of the whole map will be shown in the top left corner.",
                            self.screen.get_width() // 2,
                            self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT * 7, HELP_TEXT_SIZE)
            self.write_text("By default, the checkbox is set to True",
                            self.screen.get_width() // 2,
                            self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT * 8, HELP_TEXT_SIZE)
        else:
            self.write_text("If the checkbox is set to True, the runs",
                            self.screen.get_width() // 2,
                            self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT * 6, HELP_TEXT_SIZE)
            self.write_text("of the algorithms will be shown graphically.",
                            self.screen.get_width() // 2,
                            self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT * 7, HELP_TEXT_SIZE)
            self.write_text("By default, the checkbox is set to False",
                            self.screen.get_width() // 2,
                            self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT * 8, HELP_TEXT_SIZE)
            self.write_text("NOTE: the displaying of the runs slows the simulation down",
                            self.screen.get_width() // 2,
                            self.screen.get_height() // HELP_START_PORTION + LINE_HEIGHT * 9,
                            int(HELP_TEXT_SIZE * 0.75))

        self.write_text("click to go back", self.screen.get_width() // 2, 9 * self.screen.get_height() // 10, 40)
        # Draws the surface object to the screen.
        pygame.display.update()
        # block until click
        self.default_click_disappear()
