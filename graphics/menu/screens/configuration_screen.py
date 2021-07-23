from typing import Union

import pygame

from graphics.menu.utils.button import Button
from graphics.menu.screens.helps_screens.configuration_help import ConfigurationHelp
from graphics.menu.screens.screen_activity import Screen, TITLES_SCREEN_PORTION
from graphics.menu.screens_enum import Screens
from graphics.menu.utils.slider import Slider
from server.geometry.point import Point

SLIDERS_START = 500


class ConfigurationScreen(Screen):
    def __init__(self, screen: pygame.Surface, background):
        super().__init__(screen, background)
        self.help_screen = ConfigurationHelp(screen)
        self.help_button = Button(Point(0, 0), 80, screen.get_height() // (3 * TITLES_SCREEN_PORTION), "HELP")
        self.back_button = Button(Point(screen.get_width() - 80, 0, ), 80,
                                  screen.get_height() // (3 * TITLES_SCREEN_PORTION), "BACK")
        self.cars_amount_slider = Slider(SLIDERS_START, 300, 200, 0, 30)
        self.path_length_slider = Slider(SLIDERS_START, 400, 200, 1, 30)
        self.pressed_slider: Slider = None
        self.sliders = [self.cars_amount_slider, self.path_length_slider]

    def display(self) -> Union[int, Screens]:  # TODO typing
        """
        first load all small maps. say there are NUMBER_OF_SMALL_MAPS in each row and column, when text is not there.
        then add a padding to each dimension
        :return path of chosen map
        """
        self.__draw_configurations()
        # block until click
        while True:
            # print(self.pressed_slider)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click
                        press_point = Point(*pygame.mouse.get_pos())
                        # first check if it is the help button
                        if self.help_button.click_inside(press_point):
                            self.help_screen.display()
                            self.__draw_configurations()
                            continue
                        if self.back_button.click_inside(press_point):
                            return Screens.ALGOS_SCREEN
                        for slider in self.sliders:
                            if slider.click_on_slider(press_point):
                                self.pressed_slider = slider
                                break
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # release
                        self.pressed_slider = None
                if event.type == pygame.MOUSEMOTION:
                    if self.pressed_slider is not None:
                        self.pressed_slider.update_position(Point(*pygame.mouse.get_pos()))
                        self.__draw_configurations()

    def __draw_configurations(self):
        self.screen.fill(self.background)
        # write the text
        pygame.draw.rect(self.screen, self.background, [0, 0, self.screen.get_width(),
                                                        self.screen.get_height() // TITLES_SCREEN_PORTION])
        self.write_text("Please choose configurations", self.screen.get_width() // 2,
                        self.screen.get_height() // 10, 40)
        self.help_button.draw(self)
        self.back_button.draw(self)
        # sliders
        for slider in self.sliders:
            slider.draw(self)
        # sliders texts
        self.write_text("choose number of cars", SLIDERS_START - 200, self.cars_amount_slider.y, 20)
        self.write_text("choose min length of car path", SLIDERS_START - 200, self.path_length_slider.y, 20)
        # Draws the surface object to the screen.
        pygame.display.flip()
        pygame.display.update()
