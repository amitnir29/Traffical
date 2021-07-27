from typing import Union, Tuple, Optional

import pygame

from gui.screens.helps_screens.configuration_help import ConfigurationHelp
from gui.screens.path_screens.path_screen import PathScreen
from gui.screens.screen_activity import TITLES_SCREEN_PORTION
from gui.screens.screens_enum import Screens
from gui.utils.button import Button
from gui.utils.checkbox import CheckBox
from gui.utils.colors import RED
from gui.utils.slider import Slider
from server.geometry.point import Point

SLIDERS_START = 500


class ConfigurationScreen(PathScreen):
    def __init__(self, screen: pygame.Surface, simulation_mode: bool):
        super().__init__(screen)
        self.help_screen = ConfigurationHelp(screen, simulation_mode)
        self.help_button = Button(Point(0, 0), 80, screen.get_height() // (3 * TITLES_SCREEN_PORTION), "HELP")
        self.back_button = Button(Point(screen.get_width() - 80, 0, ), 80,
                                  screen.get_height() // (3 * TITLES_SCREEN_PORTION), "BACK")
        max_cars_amount = 30 if simulation_mode else 60
        self.cars_amount_slider = Slider(SLIDERS_START, 300, 200, 1, max_cars_amount, init_val=10)
        self.path_length_slider = Slider(SLIDERS_START, 400, 200, 1, 30, init_val=15)
        self.pressed_slider: Optional[Slider] = None
        self.sliders = [self.cars_amount_slider, self.path_length_slider]
        self.is_small_map = CheckBox(Point(SLIDERS_START, 500), 20, 20, init_val=True)
        self.show_run = CheckBox(Point(SLIDERS_START, 500), 20, 20, init_val=False)
        self.done_button = Button(Point(200, self.screen.get_height() - 100),
                                  self.screen.get_width() - 400, 100, "CONTINUE")
        self.simulation_mode = simulation_mode

    def display(self) -> Union[Tuple[int, int, bool], Screens]:
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
                            return Screens.BACK
                        for slider in self.sliders:
                            if slider.click_on_slider(press_point):
                                self.pressed_slider = slider
                                break
                        if self.simulation_mode:
                            if self.is_small_map.is_click_inside(press_point):
                                self.is_small_map.was_clicked()
                                self.__draw_configurations()
                        else:
                            if self.show_run.is_click_inside(press_point):
                                self.show_run.was_clicked()
                                self.__draw_configurations()
                        if self.done_button.click_inside(press_point):
                            b = self.is_small_map.is_checked if self.simulation_mode else self.show_run.is_checked
                            return self.cars_amount_slider.curr_value, self.path_length_slider.curr_value, b
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
        # check box
        if self.simulation_mode:
            self.is_small_map.draw(self)
        else:
            self.show_run.draw(self)
        # button
        self.done_button.draw(self)
        # texts
        self.write_text("choose number of cars", SLIDERS_START - 200, self.cars_amount_slider.y, 20)
        self.write_text("choose min length of car path", SLIDERS_START - 200, self.path_length_slider.y, 20)
        if self.simulation_mode:
            self.write_text("show small map", SLIDERS_START - 200, self.is_small_map.y, 20)
        else:
            self.write_text("show run of algorithms", SLIDERS_START - 150, self.show_run.y, 20)
            self.write_text("NOTE: the displaying of the runs slows the simulation down",
                            SLIDERS_START - 80, self.show_run.y + 40, 20, color=RED)

        # Draws the surface object to the screen.
        pygame.display.flip()
        pygame.display.update()
