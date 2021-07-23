from abc import ABC, abstractmethod
from typing import List

import pygame

from graphics.camera import Camera
from graphics.colors import DARK_BLUE
from server.geometry.point import Point


class Screen(ABC):
    def __init__(self, screen: pygame.Surface, background=DARK_BLUE):
        self.screen = screen
        self.background = background

    @abstractmethod
    def display(self):
        pass
