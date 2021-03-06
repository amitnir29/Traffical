import pygame

from gui.screens.helps_screens.info_screen import InfoScreen
from gui.screens.path_screens.path_screen import PathScreen
from gui.screens.screen_activity import TITLES_SCREEN_PORTION
from gui.screens.screens_enum import Screens
from gui.utils.button import Button
from server.geometry.point import Point


class OpenScreen(PathScreen):

    def __init__(self, screen):
        super().__init__(screen)
        self.comparison_button = Button(Point(100, 500), 250, 200, "Algos comparison", font_size=25)
        self.simulation_button = Button(Point(450, 500), 250, 200, "Simulation runner", font_size=25)
        self.info_button = Button(Point(0, 0), 80, screen.get_height() // (3 * TITLES_SCREEN_PORTION), "INFO")
        self.info_screen = InfoScreen(screen)

    def display(self) -> Screens:
        self.__draw()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click
                        press_point = Point(*pygame.mouse.get_pos())
                        if self.comparison_button.click_inside(press_point):
                            return Screens.COMPARISON_PATH
                        if self.simulation_button.click_inside(press_point):
                            return Screens.SIMULATION_PATH
                        if self.info_button.click_inside(press_point):
                            self.info_screen.display()
                            self.__draw()

    def __draw(self):
        self.screen.fill(self.background)
        # write the text
        self.write_text("Welcome to", self.screen.get_width() // 2, self.screen.get_height() // 4, 80)
        self.write_text("Traffical", self.screen.get_width() // 2, self.screen.get_height() // 4 + 140, 140)
        self.comparison_button.draw(self)
        self.simulation_button.draw(self)
        self.info_button.draw(self)
        # Draws the surface object to the screen.
        pygame.display.update()
