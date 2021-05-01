from typing import Dict, List, Tuple

import pygame.font

from graphics.camera import Camera
from graphics.colors import GREEN
from graphics.drawables.car import DrawableCar
from graphics.drawables.road import DrawableRoad
from graphics.drawables.traffic_light import DrawableLight
from simulation_objects.cars.i_car import ICar
from simulation_objects.geometry.line import Line
from simulation_objects.geometry.point import Point
from simulation_objects.roadsections.i_road_section import IRoadSection
from simulation_objects.trafficlights.i_traffic_light import ITrafficLight


class GraphicsManager:

    def __init__(self, background=GREEN, width=800, height=800, scale=0.1, fps=60):
        # Start pygame
        pygame.init()
        self.running = True
        self.scale = scale
        self.screen = self.create_screen(width, height, background)
        self.camera = Camera(0, 0, width, height, width, height)
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
        # Check if window has been closed
        self.handle_events()
        if not self.running:
            return False
        # Convert the data to drawables
        drawable_roads, drawable_lights, drawable_cars = self.create_drawables(roads, lights, cars)
        # Draw all data
        self.draw_roads(drawable_roads)
        self.draw_cars(drawable_cars, self.x)
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
        cars = [DrawableCar.from_server_obj(car) for car in cars]
        self.normalize_data(roads, lights, cars)
        return roads, lights, cars

    def normalize_data(self, roads: List[DrawableRoad], lights: List[DrawableLight], cars: List[DrawableCar]):
        all_points: List[Point] = list()
        # get all points of the simulation
        for road in roads:
            all_points += road.get_all_points()
        for light in lights:
            all_points += light.get_all_points()
        for car in cars:
            all_points += car.get_all_points()
        # get min and max x,y values of the whole map
        x_values = [p.x for p in all_points]
        y_values = [p.y for p in all_points]
        min_x = min(x_values)
        min_y = min(y_values)
        max_x = max(x_values)
        max_y = max(y_values)
        """
        now, create the normalization function based on the found min/max x/y, and self.camera
        we want linear realtions, s.t. the ratio between the caemra's min_x/max_x and width (same for y and height),
        is the same as the ratio between the shown map's part relative to the whole map size.
        which means, we want to map the min x value of that ratio to 0 and max x value of that ratio to width
        so, for x, we want a line s.t. the points: 
        (min_x+(max_x-min_x)*(camera.min_x/width),0) and (min_x+(max_x-min_x)*(camera.max_x/width),width)
        are on it, and same for y.
        1. create the x and y relations line
        2. create the normalization functions based on the lines
        3. apply on all points
        """
        # part 1
        x_line = Line(Point(min_x + (max_x - min_x) * (self.camera.min_x / self.camera.width), 0),
                      Point(min_x + (max_x - min_x) * (self.camera.max_x / self.camera.width), self.camera.width))
        y_line = Line(Point(min_y + (max_y - min_y) * (self.camera.min_y / self.camera.height), 0),
                      Point(min_y + (max_y - min_y) * (self.camera.max_y / self.camera.height), self.camera.height))
        # part 2
        norm_x = lambda x: x_line.value_at_x(x)
        norm_y = lambda y: y_line.value_at_x(y)
        # part 3
        for point in all_points:
            point.normalize(norm_x, norm_y)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    # scroll up
                    print("up")
                    self.x -= 10
                elif event.button == 5:
                    # scroll down
                    print("down")
                    self.x += 10

    def draw_roads(self, roads: List[DrawableRoad]):
        for road in roads:
            road.draw(self.screen, self.scale)

    def draw_cars(self, cars: List[DrawableCar], x):
        c = DrawableCar(Point(150, 150 + x), 180)
        c.draw(self.screen, self.scale)

    def draw_lights(self, traffic_lights: List[DrawableLight]):
        for light in traffic_lights:
            light.draw(self.screen, self.scale)
