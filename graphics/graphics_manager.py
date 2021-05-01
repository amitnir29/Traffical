from typing import Dict, List, Tuple

import pygame.font

from graphics.colors import GREEN
from graphics.drawables.car import DrawableCar
from graphics.drawables.road import DrawableRoad
from graphics.drawables.traffic_light import DrawableLight
from graphics.window import Window
from simulation_objects.cars.i_car import ICar
from simulation_objects.roadsections.i_road_section import IRoadSection
from simulation_objects.trafficlights.i_traffic_light import ITrafficLight


class GraphicsManager:

    def __init__(self, background=GREEN, width=800, height=800, scale=0.1, fps=60):
        # Start pygame
        pygame.init()
        self.done = False
        screen = pygame.display.set_mode((width, height))
        screen.fill(background)
        self.window = Window(screen, scale)
        # Screen Update Speed (FPS)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.x = 0

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
        roads = [DrawableRoad(road.coordinates, road.get_lines_between_lanes()) for road in roads]
        lights = [DrawableLight(tl.coordinate, tl.can_pass) for tl in lights]
        cars = [DrawableCar(None, None) for car in cars]  # TODO
        return roads, lights, cars

    def check_stop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def draw_roads(self, roads: List[DrawableRoad]):
        for road in roads:
            # self.window.draw_road(road)
            road.draw(self.window)

    def draw_cars(self, cars, x):
        self.window.draw_car(150, 150 + x, 180)

    def draw_lights(self, traffic_lights: List[DrawableLight]):
        # self.window.draw_light(400, 400, True)
        for light in traffic_lights:
            light.draw(self.window)
            # self.window.draw_light(light)
