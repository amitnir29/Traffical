from dataclasses import dataclass
from typing import List, Union, Tuple, Type

import pygame

from gui.screens.error_screens.cars_error import CarsError
from gui.screens.path_screens.path_screen import PathScreen
from gui.simulation_graphics.simultion_graphics import SimulationGraphics
from gui.utils.button import Button
from gui.utils.colors import RED
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
    show_runs = None


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
    lights_algos: List[Type]
    show_runs: bool


class SimulationRunner(PathScreen):
    def __init__(self, screen: pygame.Surface, conf: Union[SimulationConfiguration, ComparisonConfiguration]):
        super().__init__(screen)
        error_screen = CarsError(screen)
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
            raise Exception("couldnt create cars path")
        for car in cars:
            car.enter_first_road()
        # init traffic lights algorithm
        lights_algo = [conf.chosen_algo(junction) for junction in all_junctions]
        # init simulation's stats reporter
        reporter = StatsReporter(cars, conf.chosen_algo.__name__)
        return SimulationData(roads, traffic_lights, all_junctions, cars, lights_algo, reporter, conf.is_small_map)

    def __create_configuration_data(self, conf: ComparisonConfiguration, error_screen):
        # get the simulation map
        roads, traffic_lights, all_junctions = create_map(self.screen.get_width(),
                                                          self.screen.get_height(), conf.map_path)
        # init cars list
        cars = generate_cars(roads, conf.cars_amount, p=0.9, min_len=conf.path_min_len, with_prints=False)
        if cars is None:
            error_screen.display()
            raise Exception("couldnt create cars path")
        # init simulation's stats reporter
        return ComparisonData(roads, traffic_lights, all_junctions, cars, conf.chosen_algos, conf.show_runs)

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused

        # when run is over, report the stats
        return self.data.reporter

    def run_silent(self) -> List[Tuple[str, StatsReporter]]:
        self.data: ComparisonData
        # while the screen is not closed, draw the current state and calculate the next state
        reporters: List[Tuple[str, StatsReporter]] = list()
        for i, lights_algo_class in enumerate(self.data.lights_algos):
            self.__draw_loading_screen(i, lights_algo_class.__name__)
            if self.data.show_runs:
                gm = SimulationGraphics(self.screen, title=lights_algo_class.__name__)
            frames_counter = 0
            curr_cars = self.__init_cars()
            for car in curr_cars:
                car.enter_first_road()
            curr_lights = self.data.lights
            reporter = StatsReporter(curr_cars, lights_algo_class.__name__)
            lights_algo = [lights_algo_class(junc) for junc in self.data.junctions]
            if not self.data.show_runs:
                self.__draw_comparison_init(i, lights_algo_class.__name__)
            while len(curr_cars) > 0:
                if self.data.show_runs:
                    gm.draw(self.data.roads, curr_lights, curr_cars, self.data.junctions, with_final_display=True)
                else:
                    self.__draw_comparison_update(frames_counter)
                frames_counter = frames_counter + 1
                curr_lights, curr_cars = next_iter(lights_algo, curr_lights, curr_cars)
                reporter.next_iter(curr_cars)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
            reporters.append((lights_algo_class.__name__, reporter))
        return reporters

    def __init_cars(self):
        return [car.car_with_same_path() for car in self.data.cars]

    def __draw_comparison_init(self, index, algo_name):
        self.screen.fill(self.background)
        # write the text
        self.write_text(f"Working on algo {index + 1}", self.screen.get_width() // 2,
                        self.screen.get_height() // 2 - 100,
                        70)
        self.write_text(f"{algo_name}", self.screen.get_width() // 2, self.screen.get_height() // 2 + 40, 140)
        # Draws the surface object to the screen.
        pygame.display.update()

    def __draw_comparison_update(self, frames_count):
        pygame.draw.rect(self.screen, self.background,
                         [0, self.screen.get_height() // 2 + 120, self.screen.get_width(), 150])
        self.write_text(f"iteration number: {frames_count}", self.screen.get_width() // 2,
                        self.screen.get_height() // 2 + 200, 70)
        pygame.display.update()

    def __draw_loading_screen(self, index, algo_name):
        self.screen.fill(self.background)
        # write the text
        self.write_text(f"Loading algo {index + 1}", self.screen.get_width() // 2,
                        self.screen.get_height() // 2 - 100, 70)
        self.write_text(f"{algo_name}", self.screen.get_width() // 2, self.screen.get_height() // 2 + 40, 140)
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
