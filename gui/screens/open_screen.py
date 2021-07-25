import pygame

from gui.utils.button import Button
from gui.screens.screen_activity import Screen
from gui.screens.screens_enum import Screens
from server.geometry.point import Point


class OpenScreen(Screen):

    def __init__(self, screen, background):
        super().__init__(screen, background)
        self.comparison_button = Button(Point(100, 500), 250, 200, "Algos comparison", font_size=25)
        self.simulation_button = Button(Point(450, 500), 250, 200, "Simulation runner", font_size=25)

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

    def __draw(self):
        self.screen.fill(self.background)
        # write the text
        self.write_text("Welcome to", self.screen.get_width() // 2, self.screen.get_height() // 4, 80)
        self.write_text("Traffical", self.screen.get_width() // 2, self.screen.get_height() // 4 + 140, 140)
        self.comparison_button.draw(self)
        self.simulation_button.draw(self)
        # Draws the surface object to the screen.
        pygame.display.update()
