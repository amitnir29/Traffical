from copy import deepcopy
from typing import List, Tuple

import pygame.font

from graphics.camera import Camera
from graphics.colors import GREEN, TURQUOISE, DARK_BLUE
from graphics.drawables.car import DrawableCar
from graphics.drawables.drawable import Drawable
from graphics.drawables.junction import DrawableJunction
from graphics.drawables.road import DrawableRoad
from graphics.drawables.small_map import SmallMap
from graphics.drawables.traffic_light import DrawableLight
from server.simulation_objects.cars.i_car import ICar
from server.geometry.line import Line
from server.geometry.point import Point
from server.simulation_objects.junctions.i_junction import IJunction
from server.simulation_objects.roadsections.i_road_section import IRoadSection
from server.simulation_objects.trafficlights.i_traffic_light import ITrafficLight


class Menu:

    def __init__(self, screen: pygame.Surface, background=DARK_BLUE):
        self.background = background
        self.screen = screen
        self.start_screen()

    def start_screen(self):
        running = True
        while running:
            self.screen.fill(self.background)
            font = pygame.font.Font('freesansbold.ttf', 32)

            # create a text surface object,
            # on which text is drawn on it.
            text = font.render('GeeksForGeeks', True, GREEN, DARK_BLUE)

            # create a rectangular object for the
            # text surface object
            textRect = text.get_rect()

            # set the center of the rectangular object.
            textRect.center = (self.screen.get_width() // 2, self.screen.get_height() // 8)
            self.screen.blit(text, textRect)

            for event in pygame.event.get():
                # if event object type is QUIT
                # then quitting the pygame
                # and program both.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
                    break
                # Draws the surface object to the screen.
                pygame.display.update()
