from copy import deepcopy
from dataclasses import dataclass

from typing import List, Union, Tuple, Type

import pygame

from graphics.colors import BLACK, RED
from graphics.menu.algos import Algo
from graphics.menu.screens.helps_screens.cars_error import CarsError
from graphics.menu.screens.screen_activity import Screen
from graphics.menu.screens_enum import Screens
from graphics.menu.utils.button import Button
from graphics.simaltion_graphics import SimulationGraphics
from server.cars_generator import generate_cars
from server.geometry.point import Point
from server.map_creation import create_map
from server.server_runner import next_iter
from server.simulation_objects.cars.i_car import ICar
from server.simulation_objects.junctions.i_junction import IJunction
from server.simulation_objects.roadsections.i_road_section import IRoadSection
from server.simulation_objects.trafficlights.i_traffic_light import ITrafficLight
from server.statistics.stats_reporter import StatsReporter


@dataclass
class SimulationConfiguration:
    map_path = None
    chosen_algo = None
    cars_amount = None
    path_min_len = None
    is_small_map = None


@dataclass
class ComparisonConfiguration:
    map_path = None
    chosen_algos = None
    cars_amount = None
    path_min_len = None


@dataclass
class SimulationData:
    roads: List[IRoadSection]
    lights: List[ITrafficLight]
    junctions: List[IJunction]
    cars: List[ICar]
    lights_algo: List
    reporter: StatsReporter
    with_small_map: bool


@dataclass
class ComparisonData:
    roads: List[IRoadSection]
    lights: List[ITrafficLight]
    junctions: List[IJunction]
    cars: List[ICar]
    lights_algos: List[List]


class SimulationRunner(Screen):
    def __init__(self, screen: pygame.Surface, conf: Union[SimulationConfiguration, ComparisonConfiguration]):
        super().__init__(screen)
        error_screen = CarsError(screen, background=RED)
        if isinstance(conf, SimulationConfiguration):
            data = self.__create_simulation_data(conf, error_screen)
        elif isinstance(conf, ComparisonConfiguration):
            data = self.__create_configuration_data(conf, error_screen)
        else:
            raise Exception("something is wrong...")
        self.data = data
        self.pause_button = Button(Point(self.screen.get_width() - 50, 0), 50, 50, "PAUSE")
        self.paused = False

    def __create_simulation_data(self, conf: SimulationConfiguration, error_screen) -> SimulationData:
        # get the simulation map
        roads, traffic_lights, all_junctions = create_map(self.screen.get_width(),
                                                          self.screen.get_height(), conf.map_path)
        # init cars list
        cars = generate_cars(roads, conf.cars_amount, p=0.9, min_len=conf.path_min_len, with_prints=False)
        if cars is None:
            error_screen.display()
            exit()
        # init traffic lights algorithm
        lights_algo = [conf.chosen_algo(junction) for junction in all_junctions]
        # init simulation's stats reporter
        reporter = StatsReporter(cars, all_junctions)
        return SimulationData(roads, traffic_lights, all_junctions, cars, lights_algo, reporter, conf.is_small_map)

    def __create_configuration_data(self, conf: ComparisonConfiguration, error_screen):
        # get the simulation map
        roads, traffic_lights, all_junctions = create_map(self.screen.get_width(),
                                                          self.screen.get_height(), conf.map_path)
        # init cars list
        cars = generate_cars(roads, conf.cars_amount, p=0.9, min_len=conf.path_min_len, with_prints=False)
        if cars is None:
            error_screen.display()
            exit()
        # init traffic lights algorithm
        lights_algos = [[chosen_algo(junction) for junction in all_junctions] for chosen_algo in conf.chosen_algos]
        # init simulation's stats reporter
        return ComparisonData(roads, traffic_lights, all_junctions, cars, lights_algos)

    def display(self) -> StatsReporter:
        self.data: SimulationData
        gm = SimulationGraphics(self.screen, fps=10)
        if self.data.with_small_map:
            gm.set_small_map(self.data.roads)
        # while the screen is not closed, draw the current state and calculate the next state
        frames_counter = 0
        events = []
        while len(self.data.cars) > 0:
            gm.draw(self.data.roads, self.data.lights, self.data.cars, self.data.junctions, events=events,
                    with_final_display=False)
            self.__draw_others()
            frames_counter = frames_counter + 1
            if not self.paused:
                traffic_lights, cars = next_iter(self.data.lights_algo, self.data.lights, self.data.cars)
                self.data.reporter.next_iter(cars)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click
                        press_point = Point(*pygame.mouse.get_pos())
                        if self.paused:
                            self.paused = False
                        elif self.pause_button.click_inside(press_point):
                            self.paused = True
                            break

        # when run is over, report the stats
        return self.data.reporter

    def run_silent(self) -> List[Tuple[str, StatsReporter]]:
        self.data: ComparisonData
        # while the screen is not closed, draw the current state and calculate the next state
        frames_counter = 0
        init_cars = deepcopy(self.data.cars)
        reporters: List[Tuple[str, StatsReporter]] = list()
        for i, lights_algo in enumerate(self.data.lights_algos):
            curr_cars = deepcopy(init_cars)
            reporter = StatsReporter(curr_cars)
            while len(curr_cars) > 0:
                self.__draw_comparison(i, lights_algo[i].__class__.__name__, frames_counter)
                frames_counter = frames_counter + 1
                traffic_lights, cars = next_iter(lights_algo, self.data.lights, curr_cars)
                reporter.next_iter(cars)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
            reporters.append((lights_algo[i].__class__.__name__, reporter))
        return reporters

    def __draw_comparison(self, index, algo_name, frames_count):
        self.screen.fill(self.background)
        # write the text
        self.write_text(f"Working on algo {index+1}", self.screen.get_width() // 2, self.screen.get_height() // 2 - 100,
                        70)
        self.write_text(f"{algo_name}", self.screen.get_width() // 2, self.screen.get_height() // 2 + 40, 140)
        self.write_text(f"iteration number: {frames_count}", self.screen.get_width() // 2,
                        self.screen.get_height() // 2 + 200,
                        70)
        # Draws the surface object to the screen.
        pygame.display.update()

    def __draw_others(self):
        self.pause_button.draw(self)
        if self.paused:
            self.write_text("PAUSED", self.screen.get_width() // 2,
                            self.screen.get_height() // 2, 100, color=RED)
            self.write_text("click anywhere to continue", self.screen.get_width() // 2,
                            self.screen.get_height() // 2 + 100, 50, color=RED)
        # Draws the surface object to the screen.
        pygame.display.flip()
        pygame.display.update()
