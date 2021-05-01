from typing import Dict, List, Tuple

import pygame.font

from graphics.colors import GREEN
from graphics.drawables.car import DrawableCar
from graphics.drawables.road import DrawableRoad
from graphics.drawables.traffic_light import DrawableLight
from simulation_objects.cars.i_car import ICar
from simulation_objects.geometry.point import Point
from simulation_objects.roadsections.i_road_section import IRoadSection
from simulation_objects.trafficlights.i_traffic_light import ITrafficLight


class GraphicsManager:

    def __init__(self, background=GREEN, width=800, height=800, scale=0.1, fps=60):
        # Start pygame
        pygame.init()
        self.done = False
        self.scale = scale
        self.screen = self.create_screen(width, height, background)
        # Screen Update Speed (FPS)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.x = 0

    def create_screen(self, width, height, background):
        screen = pygame.display.set_mode((width, height))
        screen.fill(background)
        return screen

    def __del__(self):
        # Shutdown
        pygame.quit()

    def draw(self, roads: List[IRoadSection], lights: List[ITrafficLight], cars: List[ICar]) -> bool:
        drawable_roads, drawable_lights, drawable_cars = self.create_drawables(roads, lights, cars)
        # Check if window has been closed
        if self.check_stop():
            return False
        # Draw all data
        self.draw_roads(drawable_roads)
        self.draw_cars(cars, self.x)
        self.x += 1
        self.draw_lights(drawable_lights)
        # Display
        pygame.display.flip()
        pygame.display.update()
        # Setting FPS
        self.clock.tick(self.fps)
        return True

    def create_drawables(self, roads: List[IRoadSection], lights: List[ITrafficLight], cars: List[ICar]) \
            -> Tuple[List[DrawableRoad], List[DrawableLight], List[DrawableCar]]:
        roads = [DrawableRoad.from_server_obj(road) for road in roads]
        lights = [DrawableLight.from_server_obj(tl) for tl in lights]
        cars = [DrawableCar.from_server_obj(car) for car in cars]  # TODO
        return roads, lights, cars

    def check_stop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def draw_roads(self, roads: List[DrawableRoad]):
        for road in roads:
            road.draw(self.screen, self.scale)

    def draw_cars(self, cars, x):
        c = DrawableCar(Point(150, 150 + x), 180)
        c.draw(self.screen, self.scale)

    def draw_lights(self, traffic_lights: List[DrawableLight]):
        for light in traffic_lights:
            light.draw(self.screen, self.scale)
