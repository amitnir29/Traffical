from typing import List

import pygame

from graphics.menu.algos import Algo, all_algos_list
from graphics.menu.screens.screen_activity import Screen, TITLES_SCREEN_PORTION
from server.geometry.point import Point

HEIGHT_OF_ALGO_ROW = 50


class AlgoChoosing(Screen):
    def __init__(self, screen: pygame.Surface, background):
        super().__init__(screen, background)
        self.algos_list = self.__create_algos_list()

    def display(self):
        """
        first load all small maps. say there are NUMBER_OF_SMALL_MAPS in each row and column, when text is not there.
        then add a padding to each dimension
        :return path of chosen map
        """
        scroll_delta_y = 20
        self.__draw_algos_menu()
        # block until click
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click
                        # find the clicked algo
                        press_point = Point(*pygame.mouse.get_pos())
                        if press_point.y < self.screen.get_height() // TITLES_SCREEN_PORTION:
                            continue
                        pressed_algo = self.__find_pressed_algo(press_point)
                        if pressed_algo is not None:
                            return pressed_algo.algo_class
                    elif event.button == 4:
                        # scroll up
                        self.__shift_algos_rectangles(scroll_delta_y)
                        self.__draw_algos_menu()
                    elif event.button == 5:
                        # scroll down
                        self.__shift_algos_rectangles(-scroll_delta_y)
                        self.__draw_algos_menu()

    def __create_algos_list(self) -> List[Algo]:
        all_algos_classes = all_algos_list
        algos_list = list()
        for i, algo_name in enumerate(all_algos_classes):
            algos_list.append(Algo(algo_name, 0,
                                   self.screen.get_height() // TITLES_SCREEN_PORTION + i * HEIGHT_OF_ALGO_ROW,
                                   self.screen.get_width(), HEIGHT_OF_ALGO_ROW))
        return algos_list

    def __draw_all_algos(self):
        # draw the small maps
        for algo in self.algos_list:
            pygame.draw.rect(self.screen, self.background, [algo.x, algo.y, algo.width, algo.height])
            self.write_text(str(algo.algo_class.__name__), algo.x + algo.width // 2,
                            algo.y + algo.height // 2, 30)

    def __draw_algos_menu(self):
        self.screen.fill(self.background)
        # write the text
        self.__draw_all_algos()
        pygame.draw.rect(self.screen, self.background, [0, 0, self.screen.get_width(),
                                                        self.screen.get_height() // TITLES_SCREEN_PORTION])
        self.write_text("Please choose an algorithm", self.screen.get_width() // 2,
                        self.screen.get_height() // 10, 50)

        # Draws the surface object to the screen.
        pygame.display.flip()
        pygame.display.update()

    def __shift_algos_rectangles(self, delta: int):
        if delta < 0:  # scroll up
            if self.algos_list[-1].y < self.screen.get_height() - delta:
                return
        if delta > 0:  # scroll down
            if self.algos_list[0].y >= self.screen.get_height() // TITLES_SCREEN_PORTION:
                return
        for algo in self.algos_list:
            algo.y += delta

    def __find_pressed_algo(self, pressed_point: Point):
        for algo in self.algos_list:
            if algo.x <= pressed_point.x <= algo.x + algo.width and algo.y <= pressed_point.y <= algo.y + algo.height:
                return algo
        return None
