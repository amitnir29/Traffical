from abc import ABC, abstractmethod

import pygame

from gui.screens.screen_activity import Screen
from server.geometry.point import Point


class StatsScreenParent(Screen, ABC):

    def display(self):
        reporter_data = self._reporters_data()
        total_delta_y = 0
        scroll_delta_y = 50
        self._draw_all_data(total_delta_y, reporter_data)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click
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

    @property
    @abstractmethod
    def max_scroll(self):
        pass
