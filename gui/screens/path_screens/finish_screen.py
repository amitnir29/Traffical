import pygame

from gui.screens.path_screens.path_screen import PathScreen
from gui.utils.button import Button
from server.geometry.point import Point


class FinishScreen(PathScreen):

    def __init__(self, screen: pygame.Surface, stats_screen):
        super().__init__(screen)
        self.stats_button = Button(Point(200, 600), 400, 200, "Statistics")
        self.stats_screen = stats_screen

    def display(self):
        self.__draw_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click
                        press_point = Point(*pygame.mouse.get_pos())
                        if self.stats_button.click_inside(press_point):
                            self.stats_screen.display()
                            self.__draw_screen()
                            continue
                        else:
                            # quit all
                            quit()

    def __draw_screen(self):
        self.screen.fill(self.background)
        # write the text
        self.write_text("Run finished", self.screen.get_width() // 2, self.screen.get_height() // 2 - 100, 100)
        self.write_text("Click to exit", self.screen.get_width() // 2, self.screen.get_height() // 2 + 150, 40)
        self.stats_button.draw(self)
        # Draws the surface object to the screen.
        pygame.display.update()
