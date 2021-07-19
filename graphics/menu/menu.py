import pygame.font

from graphics.colors import DARK_BLUE, WHITE
from graphics.menu.menu_small_maps_creator import load_all_small_maps
from server.geometry.point import Point

NUMBER_OF_SMALL_MAPS = 4


class Menu:

    def __init__(self, screen: pygame.Surface, background=DARK_BLUE):
        self.background = background
        self.screen = screen

    def run(self):
        maps_padding = 10
        menu_small_maps = load_all_small_maps(self.screen,
                                              self.screen.get_width() // NUMBER_OF_SMALL_MAPS - 2 * maps_padding,
                                              self.screen.get_height() // NUMBER_OF_SMALL_MAPS - 2 * maps_padding)
        self._start_screen()
        self._map_choosing(menu_small_maps, maps_padding)

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click
                        running = False
                        break

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

    def _map_choosing(self, menu_small_maps, padding):
        """
        first load all small maps. say there are NUMBER_OF_SMALL_MAPS in each row and column, when text is not there.
        then add a padding to each dimension
        """
        total_delta_y = 0
        scroll_delta_y = 20
        self.__draw_map_choosing_menu(menu_small_maps, padding, total_delta_y)
        # block until click
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click
                        # find the clicked map

                        running = False
                        break
                    if event.button == 4:
                        # scroll up
                        total_delta_y = max(0, total_delta_y - scroll_delta_y)
                        self.__draw_map_choosing_menu(menu_small_maps, padding, total_delta_y)
                    elif event.button == 5:
                        # scroll down
                        max_scroll = (len(menu_small_maps) // NUMBER_OF_SMALL_MAPS - 2) \
                                     * (self.screen.get_height() // NUMBER_OF_SMALL_MAPS)
                        total_delta_y = min(max_scroll, total_delta_y + scroll_delta_y)
                        self.__draw_map_choosing_menu(menu_small_maps, padding, total_delta_y)
