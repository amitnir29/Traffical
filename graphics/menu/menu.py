from typing import List

import pygame.font

from graphics.colors import DARK_BLUE, WHITE
from graphics.menu.algos import all_algos_list, Algo
from graphics.menu.menu_small_map import MenuSmallMap
from graphics.menu.menu_small_maps_creator import load_all_small_maps
from server.geometry.point import Point

TITLES_SCREEN_PORTION = 4
NUMBER_OF_SMALL_MAPS = TITLES_SCREEN_PORTION
HEIGHT_OF_ALGO_ROW = 50


class Menu:

    def __init__(self, screen: pygame.Surface, background=DARK_BLUE):
        self.background = background
        self.screen = screen

    def run(self):
        maps_padding = 10
        menu_small_maps = load_all_small_maps(self.screen,
                                              self.screen.get_width() // NUMBER_OF_SMALL_MAPS - 2 * maps_padding,
                                              self.screen.get_height() // NUMBER_OF_SMALL_MAPS - 2 * maps_padding)
        algos_list = self.__create_algos_list()
        self._start_screen()
        map_path = self._map_choosing(menu_small_maps, maps_padding)
        chosen_algo = self._algo_choosing(algos_list)
        return map_path, chosen_algo

    def __text(self, txt, x, y, size, color=WHITE, font='freesansbold.ttf'):
        """
        write text on the screen
        :param txt: text to write
        :param x: middle x of the text position
        :param y: middle y of the text position
        :param size: font size
        :param color: color of the text
        :param font: font of the text
        :return:
        """
        font = pygame.font.Font(font, size)
        # create a text surface object, on which text is drawn on it.
        text = font.render(txt, True, color, self.background)
        # create a rectangular object for the text surface object
        textRect = text.get_rect()
        # set the center of the rectangular object.
        textRect.center = (x, y)
        # write the text
        self.screen.blit(text, textRect)

    # screen 1
    def _start_screen(self):
        self.screen.fill(self.background)
        # write the text
        self.__text("Welcome to", self.screen.get_width() // 2, self.screen.get_height() // 4, 80)
        self.__text("Traffical", self.screen.get_width() // 2, self.screen.get_height() // 4 + 140, 140)
        self.__text("click to continue", self.screen.get_width() // 2, 3 * self.screen.get_height() // 4, 40)
        # Draws the surface object to the screen.
        pygame.display.update()
        # block until click
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click
                        running = False
                        break

    # screen 2
    def _map_choosing(self, menu_small_maps, padding) -> str:
        """
        first load all small maps. say there are NUMBER_OF_SMALL_MAPS in each row and column, when text is not there.
        then add a padding to each dimension
        :return path of chosen map
        """
        total_delta_y = 0
        scroll_delta_y = 20
        self.__draw_map_choosing_menu(menu_small_maps, padding, total_delta_y)
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
                        if press_point.y < self.screen.get_height() // NUMBER_OF_SMALL_MAPS:
                            continue
                        pressed_map = self.__find_pressed_map(menu_small_maps, press_point)
                        if pressed_map is not None:
                            return pressed_map.path
                    elif event.button == 4:
                        # scroll up
                        total_delta_y = max(0, total_delta_y - scroll_delta_y)
                        self.__draw_map_choosing_menu(menu_small_maps, padding, total_delta_y)
                    elif event.button == 5:
                        # scroll down
                        max_scroll = (len(menu_small_maps) // NUMBER_OF_SMALL_MAPS - 2) \
                                     * (self.screen.get_height() // NUMBER_OF_SMALL_MAPS)
                        total_delta_y = min(max_scroll, total_delta_y + scroll_delta_y)
                        self.__draw_map_choosing_menu(menu_small_maps, padding, total_delta_y)

    def __draw_all_small_maps(self, all_small_maps, padding, delta_y):
        # draw the small maps
        for i, small_map in enumerate(all_small_maps):
            row = i // NUMBER_OF_SMALL_MAPS + 1  # first row is for the title
            col = i % NUMBER_OF_SMALL_MAPS
            row_jump = self.screen.get_width() // NUMBER_OF_SMALL_MAPS
            col_jump = self.screen.get_height() // NUMBER_OF_SMALL_MAPS
            small_map.draw(self.screen, Point(col * col_jump + padding, row * row_jump + padding - delta_y))

    def __draw_map_choosing_menu(self, menu_small_maps, padding, scroll_delta_y):
        self.screen.fill(self.background)
        # write the text
        self.__draw_all_small_maps(menu_small_maps, padding, scroll_delta_y)
        pygame.draw.rect(self.screen, self.background, [0, 0, self.screen.get_width(),
                                                        self.screen.get_height() // NUMBER_OF_SMALL_MAPS])
        self.__text("Please choose a map", self.screen.get_width() // 2, self.screen.get_height() // 10, 70)

        # Draws the surface object to the screen.
        pygame.display.flip()
        pygame.display.update()

    def __find_pressed_map(self, all_maps: List[MenuSmallMap], press_point: Point):
        for small_map in all_maps:
            if small_map.click_inside(press_point):
                return small_map
        return None

    # screen 3
    def _algo_choosing(self, algos_list: List[Algo]):
        """
        first load all small maps. say there are NUMBER_OF_SMALL_MAPS in each row and column, when text is not there.
        then add a padding to each dimension
        :return path of chosen map
        """
        0
        scroll_delta_y = 20
        self.__draw_algos_menu(algos_list)
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
                        pressed_algo = self.__find_pressed_algo(algos_list, press_point)
                        if pressed_algo is not None:
                            return pressed_algo.algo_class
                    elif event.button == 4:
                        # scroll up
                        self.__shift_algos_rectangles(algos_list, scroll_delta_y)
                        self.__draw_algos_menu(algos_list)
                    elif event.button == 5:
                        # scroll down
                        self.__shift_algos_rectangles(algos_list, -scroll_delta_y)
                        self.__draw_algos_menu(algos_list)

    def __create_algos_list(self) -> List[Algo]:
        all_algos_classes = all_algos_list
        algos_list = list()
        for i, algo_name in enumerate(all_algos_classes):
            algos_list.append(Algo(algo_name, 0,
                                   self.screen.get_height() // TITLES_SCREEN_PORTION + i * HEIGHT_OF_ALGO_ROW,
                                   self.screen.get_width(), HEIGHT_OF_ALGO_ROW))
        return algos_list

    def __draw_all_algos(self, algos_list: List[Algo]):
        # draw the small maps
        for algo in algos_list:
            pygame.draw.rect(self.screen, self.background, [algo.x, algo.y, algo.width, algo.height])
            self.__text(str(algo.algo_class.__name__), algo.x + algo.width // 2, algo.y + algo.height // 2, 30)

    def __draw_algos_menu(self, algos_list: List[Algo]):
        self.screen.fill(self.background)
        # write the text
        self.__draw_all_algos(algos_list)
        pygame.draw.rect(self.screen, self.background, [0, 0, self.screen.get_width(),
                                                        self.screen.get_height() // TITLES_SCREEN_PORTION])
        self.__text("Please choose an algorithm", self.screen.get_width() // 2, self.screen.get_height() // 10, 50)

        # Draws the surface object to the screen.
        pygame.display.flip()
        pygame.display.update()

    def __shift_algos_rectangles(self, all_algos: List[Algo], delta: int):
        if delta < 0:  # scroll up
            if all_algos[-1].y < self.screen.get_height() - delta:
                return
        if delta > 0:  # scroll down
            if all_algos[0].y >= self.screen.get_height() // TITLES_SCREEN_PORTION:
                return
        for algo in all_algos:
            algo.y += delta

    def __find_pressed_algo(self, all_algos: List[Algo], pressed_point: Point):
        for algo in all_algos:
            if algo.x <= pressed_point.x <= algo.x + algo.width and algo.y <= pressed_point.y <= algo.y + algo.height:
                return algo
        return None
