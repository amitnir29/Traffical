from typing import List, Dict

import pygame.font
from gui.simulation_graphics.camera import Camera
from gui.utils.colors import TURQUOISE, GRAY
from gui.simulation_graphics.drawables.car import DrawableCar
from gui.simulation_graphics.drawables.junction import DrawableJunction
from gui.simulation_graphics.drawables.road import DrawableRoad
from gui.simulation_graphics.drawables.corner_small_map import CornerSmallMap
from gui.simulation_graphics.drawables.traffic_light import DrawableLight
from server.simulation_objects.cars.i_car import ICar
from server.geometry.line import Line
from server.geometry.point import Point
from server.simulation_objects.junctions.i_junction import IJunction
from server.simulation_objects.roadsections.i_road_section import IRoadSection
from server.simulation_objects.trafficlights.i_traffic_light import ITrafficLight
from copy import *


class SimulationGraphics:

    def __init__(self, screen: pygame.Surface, background=TURQUOISE, fps=60, title=None):
        self.running = True
        self.background = background
        self.screen = screen
        self.camera = Camera(0, 0, screen.get_width(), screen.get_height(), screen.get_width(), screen.get_height())
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.small_map: CornerSmallMap = None
        self.current_roads: List[DrawableRoad] = None
        self.current_junctions: List[DrawableJunction] = None
        self.current_lights: List[DrawableLight] = None
        self.current_cars: Dict[int, DrawableCar] = None  # dict from id to car
        self.title = title

    def set_small_map(self, roads, width=100, height=100):
        self.small_map = CornerSmallMap.from_server_obj(
            (width, height, self.screen.get_width(), self.screen.get_height(),
             roads, self.screen, self.camera))

    def draw(self, roads: List[IRoadSection], lights: List[ITrafficLight],
             cars: List[ICar], junctions: List[IJunction], events=None, with_final_display=True):
        self.screen.fill(self.background)
        # Check if window has been closed
        self.handle_events(events)
        if not self.running:
            return False
        # Convert the data to drawables
        self.update_drawables(roads, lights, cars, junctions)
        # Draw all data
        self.draw_all()
        # draw small map
        if self.small_map is not None:
            self.small_map.draw(self.screen)
        if self.title is not None:
            font = pygame.font.Font("freesansbold.ttf", self.screen.get_width() // 30)
            # create a text surface object, on which text is drawn on it.
            text = font.render(self.title, True, GRAY)
            # create a rectangular object for the text surface object
            textRect = text.get_rect()
            # set the center of the rectangular object.
            textRect.center = (self.screen.get_width() // 8, self.screen.get_width() // 20)
            # write the text
            self.screen.blit(text, textRect)
        # Display
        if with_final_display:
            pygame.display.flip()
            pygame.display.update()
        # Setting FPS
        self.clock.tick(self.fps)

    def update_drawables(self, roads: List[IRoadSection], lights: List[ITrafficLight],
                         cars: List[ICar], junctions: List[IJunction]):
        # update roads and juncs
        self.current_roads = [DrawableRoad.from_server_obj(road) for road in roads]
        self.current_junctions = [DrawableJunction.from_server_obj(junc) for junc in junctions]
        if self.current_lights is None:
            # create lights
            self.current_lights = [DrawableLight.from_server_obj(tl) for tl in lights]
        if self.current_cars is None:
            self.current_cars = {car.get_id(): DrawableCar.from_server_obj(car) for car in cars}
        else:
            # update cars
            new_cars_ids: Dict[int, ICar] = {car.get_id(): car for car in cars}
            # for each car that is now out:
            for out_car_id in set(self.current_cars.keys()).difference(new_cars_ids):
                out_car: DrawableCar = self.current_cars[out_car_id]
                out_car.reached_target = True
            # update positions of all cars
            for car in cars:
                self.current_cars[car.get_id()].center = deepcopy(car.position)
                self.current_cars[car.get_id()].angle = car.get_angle()
            # update lights
            for i, light in enumerate(lights):
                self.current_lights[i].is_green = lights[i].can_pass
                self.current_lights[i].center = deepcopy(lights[i].coordinate)
        self.normalize_data()

    def normalize_data(self):
        all_points: List[Point] = list()
        points2: List[Point] = list()
        # get all points of the simulation
        for road in self.current_roads:
            all_points += road.get_all_points()
        for light in self.current_lights:
            points2 += light.get_all_points()
        for car in self.current_cars.values():
            points2 += car.get_all_points()
        for junc in self.current_junctions:
            all_points += junc.get_all_points()
        # get min and max x,y values of the whole map
        x_values = [p.x for p in all_points]
        y_values = [p.y for p in all_points]
        min_x = min(x_values)
        min_y = min(y_values)
        max_x = max(x_values)
        max_y = max(y_values)
        all_points = all_points + points2
        """
        now, create the normalization function based on the found min/max x/y, and self.camera
        we want linear realtions, s.t. the ratio between the camera's min_x/max_x and width (same for y and height),
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

    def handle_events(self, events):
        if events is None:
            events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                exit()
            elif event.type == pygame.KEYDOWN:
                # moving camera to the sides
                if event.key == pygame.K_UP:
                    self.camera.up()
                if event.key == pygame.K_DOWN:
                    self.camera.down()
                if event.key == pygame.K_RIGHT:
                    self.camera.right()
                if event.key == pygame.K_LEFT:
                    self.camera.left()
                # zooming in and out
                if event.key == pygame.K_z:
                    self.camera.zoom_in(*pygame.mouse.get_pos())
                if event.key == pygame.K_x:
                    self.camera.zoom_out(*pygame.mouse.get_pos())

    def draw_all(self):
        self.draw_roads()
        self.draw_junctions()
        self.draw_cars()
        self.draw_lights()

    def draw_roads(self):
        for road in self.current_roads:
            road.draw(self.screen)

    def draw_cars(self):
        scale = 0.04 * (self.camera.width / self.camera.delta_x)
        for car in self.current_cars.values():
            car.draw(self.screen, scale)

    def draw_lights(self):
        # scale formula that looks nice:
        scale = 0.05 * pow((self.camera.width / self.camera.delta_x), 1 / 3)
        for light in self.current_lights:
            if light.is_inside_camera(self.camera):
                light.draw(self.screen, scale)

    def draw_junctions(self):
        for junc in self.current_junctions:
            junc.draw(self.screen)
