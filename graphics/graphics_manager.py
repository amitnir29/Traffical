from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple

import pygame.font

from graphics.camera import Camera
from graphics.colors import GREEN
from graphics.drawables.car import DrawableCar
from graphics.drawables.drawable import Drawable
from graphics.drawables.junction import DrawableJunction
from graphics.drawables.road import DrawableRoad
from graphics.drawables.small_map import SmallMap
from graphics.drawables.traffic_light import DrawableLight
from graphics.gm_data import GMData
from server.simulation_objects.cars.i_car import ICar
from server.geometry.line import Line
from server.geometry.point import Point
from server.simulation_objects.junctions.i_junction import IJunction
from server.simulation_objects.roadsections.i_road_section import IRoadSection
from server.simulation_objects.trafficlights.i_traffic_light import ITrafficLight


class GraphicsManager:

    def __init__(self, roads, juncs, background=GREEN, width=800, height=800, fps=60):
        # Start pygame
        pygame.init()
        self.running = True
        self.background = background
        self.screen = self.create_screen(width, height)
        self.camera = Camera(0, 0, width, height, width, height)
        self.screen_width = width
        self.screen_height = height
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.small_map: SmallMap = None
        self.gm_data = self.create_base_data(roads, juncs)
        self.normalize_data(self.gm_data.roads, self.gm_data.juncs)

    def create_screen(self, width, height):
        screen = pygame.display.set_mode((width, height))
        return screen

    def create_base_data(self, roads, juncs) -> GMData:
        d_roads = [DrawableRoad.from_server_obj(road) for road in roads]
        d_juncs = [DrawableJunction.from_server_obj(junc) for junc in juncs]
        return GMData(d_roads, d_juncs)

    def set_small_map(self, roads, juncs, width=100, height=100):
        self.small_map = SmallMap.from_server_obj((width, height, self.screen_width, self.screen_height,
                                                   roads, juncs, self.screen, self.camera))

    def __del__(self):
        # Shutdown
        pygame.quit()

    def draw(self, lights: List[ITrafficLight], cars: List[ICar]) -> bool:
        self.screen.fill(self.background)
        # Check if window has been closed
        self.handle_events()
        if not self.running:
            return False
        # Convert the data to drawables
        drawable_lights, drawable_cars = self.create_drawables(lights, cars)
        # Draw all data
        self.draw_roads()
        self.draw_junctions()
        self.draw_cars(drawable_cars)
        self.draw_lights(drawable_lights)
        # draw small map
        if self.small_map is not None:
            self.small_map.draw(self.screen)

        # Display
        pygame.display.flip()
        pygame.display.update()
        # Setting FPS
        self.clock.tick(self.fps)
        return len(cars) > 0

    def create_drawables(self, lights: List[ITrafficLight], cars: List[ICar]) \
            -> Tuple[List[DrawableLight], List[DrawableCar]]:
        lights = [DrawableLight.from_server_obj(tl) for tl in lights]
        cars = [DrawableCar.from_server_obj(car) for car in cars]
        self.normalize_data(lights, cars)
        return lights, cars

    def normalize_data(self, *drawables_lists: List[Drawable]):
        normalization_objects: List[Drawable] = self.gm_data.roads + self.gm_data.juncs
        normalization_points: List[Point] = list()
        # get all points of the simulation
        for drawable in normalization_objects:
            normalization_points += drawable.get_all_points()
        # get min and max x,y values of the whole map
        x_values = [p.x for p in normalization_points]
        y_values = [p.y for p in normalization_points]
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
        all_drawables = sum(drawables_lists, [])
        for drawable in all_drawables:
            for point in drawable.get_all_points():
                point.normalize(norm_x, norm_y)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    # scroll up
                    self.camera.zoom_in(*pygame.mouse.get_pos())
                    self.normalize_data(self.gm_data.roads, self.gm_data.juncs)
                elif event.button == 5:
                    # scroll down
                    self.camera.zoom_out(*pygame.mouse.get_pos())
                    self.normalize_data(self.gm_data.roads, self.gm_data.juncs)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.camera.up()
                if event.key == pygame.K_DOWN:
                    self.camera.down()
                if event.key == pygame.K_RIGHT:
                    self.camera.right()
                if event.key == pygame.K_LEFT:
                    self.camera.left()

    def draw_roads(self):
        for road in self.gm_data.roads:
            road.draw(self.screen)

    def draw_junctions(self):
        for junc in self.gm_data.juncs:
            junc.draw(self.screen)

    def draw_cars(self, cars: List[DrawableCar]):
        scale = 0.05
        for car in cars:
            car.draw(self.screen, scale)

    def draw_lights(self, traffic_lights: List[DrawableLight]):
        # scale formula that looks nice:
        scale = 0.1 * pow((self.camera.width / self.camera.delta_x), 1 / 3)
        for light in traffic_lights:
            light.draw(self.screen, scale)
