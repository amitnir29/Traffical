from typing import Dict, List

import pygame.font
from graphics.window import Window
from simulation_objects.roadsections.i_road_section import IRoadSection
from simulation_objects.trafficlights.i_traffic_light import ITrafficLight


class GraphicsManager:

    def __init__(self, background=(0, 255, 0), width=1280, height=800, scale=0.1, fps=60):
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

    def draw(self, roads, traffic_lights, cars) -> bool:
        # Check if window has been closed
        if self.check_stop():
            return False
        # Draw all data
        self.draw_roads(roads)
        self.draw_cars(cars, self.x)
        self.x += 1
        self.draw_lights(traffic_lights)
        # Display
        pygame.display.flip()
        pygame.display.update()
        # Setting FPS
        self.clock.tick(self.fps)
        return True

    def check_stop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def draw_roads(self, roads: Dict[int, IRoadSection]):
        for road in roads.values():
            self.window.draw_road(road)

    def draw_cars(self, cars, x):
        self.window.draw_car(150, 150 + x, 180)

    def draw_lights(self, traffic_lights: List[ITrafficLight]):
        # self.window.draw_light(400, 400, True)
        for light in traffic_lights:
            self.window.draw_light(light)
