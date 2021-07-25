from typing import Union

import pygame

from gui.utils.button import Button
from gui.screens.helps_screens.maps_help import MapsHelp
from gui.screens.screen_activity import Screen, TITLES_SCREEN_PORTION
from gui.screens.screens_enum import Screens
from gui.simulation_graphics.small_maps.menu_small_maps_creator import load_all_small_maps
from server.geometry.point import Point

NUMBER_OF_SMALL_MAPS = TITLES_SCREEN_PORTION


class MapChoosing(Screen):
    def __init__(self, screen: pygame.Surface, background):
        super().__init__(screen, background)
        self.padding = 10
        self.maps = load_all_small_maps(screen,
                                        screen.get_width() // NUMBER_OF_SMALL_MAPS - 2 * self.padding,
                                        screen.get_height() // NUMBER_OF_SMALL_MAPS - 2 * self.padding)
        self.help_screen = MapsHelp(screen)
        self.help_button = Button(Point(0, 0), 80, screen.get_height() // (3 * TITLES_SCREEN_PORTION), "HELP")
        self.back_button = Button(Point(screen.get_width() - 80, 0, ), 80,
                                  screen.get_height() // (3 * TITLES_SCREEN_PORTION), "BACK")

    def display(self) -> Union[str, Screens]:
        """
        :return: Screens.OPEN or maps_path
        """
        total_delta_y = 0
        scroll_delta_y = 50
        self.__draw_map_choosing_menu(total_delta_y)
        # block until click
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click
                        # find the clicked map
                        press_point = Point(*pygame.mouse.get_pos())
                        # first check if it is one of the buttons
                        if self.help_button.click_inside(press_point):
                            self.help_screen.display()
                            self.__draw_map_choosing_menu(total_delta_y)
                            continue
                        if self.back_button.click_inside(press_point):
                            return Screens.BACK
                        # next, check it if in the title, do nothing
                        if press_point.y < self.screen.get_height() // NUMBER_OF_SMALL_MAPS:
                            continue
                        # else, get the map
                        pressed_map = self.__find_pressed_map(press_point)
                        if pressed_map is not None:
                            return pressed_map.path
                    elif event.button == 4:
                        # scroll up
                        total_delta_y = max(0, total_delta_y - scroll_delta_y)
                        self.__draw_map_choosing_menu(total_delta_y)
                    elif event.button == 5:
                        # scroll down
                        max_scroll = (len(self.maps) // NUMBER_OF_SMALL_MAPS - 2) \
                                     * (self.screen.get_height() // NUMBER_OF_SMALL_MAPS)
                        total_delta_y = min(max_scroll, total_delta_y + scroll_delta_y)
                        self.__draw_map_choosing_menu(total_delta_y)

    def __draw_all_small_maps(self, delta_y):
        # draw the small maps
        for i, small_map in enumerate(self.maps):
            row = i // NUMBER_OF_SMALL_MAPS + 1  # first row is for the title
            col = i % NUMBER_OF_SMALL_MAPS
            row_jump = self.screen.get_width() // NUMBER_OF_SMALL_MAPS
            col_jump = self.screen.get_height() // NUMBER_OF_SMALL_MAPS
            small_map.draw(self.screen, Point(col * col_jump + self.padding, row * row_jump + self.padding - delta_y))

    def __draw_map_choosing_menu(self, scroll_delta_y):
        self.screen.fill(self.background)
        # write the text
        self.__draw_all_small_maps(scroll_delta_y)
        pygame.draw.rect(self.screen, self.background, [0, 0, self.screen.get_width(),
                                                        self.screen.get_height() // NUMBER_OF_SMALL_MAPS])
        self.write_text("Please choose a map", self.screen.get_width() // 2,
                        self.screen.get_height() // (2 * TITLES_SCREEN_PORTION), 50)
        self.help_button.draw(self)
        self.back_button.draw(self)  # XXX

        # Draws the surface object to the screen.
        pygame.display.flip()
        pygame.display.update()

    def __find_pressed_map(self, press_point: Point):
        for small_map in self.maps:
            if small_map.click_inside(press_point):
                return small_map
        return None
