from abc import ABC, abstractmethod

import pygame

from gui.screens.screen_activity import Screen, TITLES_SCREEN_PORTION
from gui.utils.button import Button
from gui.utils.colors import LIGHT_ORANGE
from server.geometry.point import Point


class StatsScreenParent(Screen, ABC):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen, background=LIGHT_ORANGE)
        self.save_button = Button(Point(0, 0), 80, screen.get_height() // (3 * TITLES_SCREEN_PORTION), "SAVE")
        self.was_saved_text = None

    def display(self):
        reporter_data = self._reporters_data()
        total_delta_y = 0
        scroll_delta_y = 75
        self._draw_all_data(total_delta_y, reporter_data)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click
                        press_point = Point(*pygame.mouse.get_pos())
                        if self.save_button.click_inside(press_point):
                            if self.was_saved_text is None:
                                self._save_to_file()
                                self._draw_all_data(total_delta_y, reporter_data)
                        else:
                            # finish
                            return
                    elif event.button == 4:
                        # scroll up
                        total_delta_y = max(0, total_delta_y - scroll_delta_y)
                        self._draw_all_data(total_delta_y, reporter_data)
                    elif event.button == 5:
                        # scroll down
                        max_scroll = self.max_scroll
                        total_delta_y = min(max_scroll, total_delta_y + scroll_delta_y)
                        self._draw_all_data(total_delta_y, reporter_data)

    def pil_image_to_surface(self, pil_image):
        return pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode).convert()

    def draw_image(self, image, center: Point, scale=0.5):
        img = pygame.transform.rotozoom(image, 0, scale)
        rect = img.get_rect()
        rect.center = center.to_tuple()
        self.screen.blit(img, rect)

    @abstractmethod
    def _draw_all_data(self, total_delta_y, reporter_data):
        pass

    @abstractmethod
    def _reporters_data(self):
        pass

    @abstractmethod
    def _save_to_file(self):
        pass

    @property
    @abstractmethod
    def max_scroll(self):
        pass
