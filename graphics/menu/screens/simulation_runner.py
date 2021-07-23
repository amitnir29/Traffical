from dataclasses import dataclass

from typing import List

import pygame

from graphics.colors import BLACK, RED
from graphics.menu.screens.screen_activity import Screen
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


class SimulationConfiguration:
    def __init__(self):
        self.map_path = None
        self.chosen_algo = None
        self.cars_amount = None
        self.path_min_len = None
        self.is_small_map = None

    def to_tuple(self):
        return self.map_path, self.chosen_algo, self.cars_amount, self.path_min_len, self.is_small_map


@dataclass
class SimulationData:
    roads: List[IRoadSection]
    lights: List[ITrafficLight]
    junctions: List[IJunction]
    cars: List[ICar]
    lights_algo: List
    reporter: StatsReporter
    with_small_map: bool


class SimulationRunner(Screen):
    def __init__(self, screen: pygame.Surface, conf: SimulationConfiguration):
        super().__init__(screen)
        self.data = self.__create_simulation_data(conf)
        self.pause_button = Button(Point(self.screen.get_width() - 50, 0), 50, 50, "PAUSE")
        self.paused = False

    def __create_simulation_data(self, conf: SimulationConfiguration) -> SimulationData:
        # get the simulation map
        map_path, chosen_algo, cars_amount, path_min_len, with_small_map = conf.to_tuple()
        roads, traffic_lights, all_junctions = create_map(self.screen.get_width(), self.screen.get_height(), map_path)
        # init cars list
        cars = generate_cars(roads, cars_amount, p=0.9, min_len=path_min_len, with_prints=False)
        # init traffic lights algorithm
        lights_algo = [chosen_algo(junction) for junction in all_junctions]
        # init simulation's stats reporter
        reporter = StatsReporter(cars, all_junctions)
        return SimulationData(roads, traffic_lights, all_junctions, cars, lights_algo, reporter, conf.is_small_map)

    def display(self) -> StatsReporter:
        gm = SimulationGraphics(self.screen, fps=10)
        if self.data.with_small_map:
            gm.set_small_map(self.data.roads)
        # while the screen is not closed, draw the current state and calculate the next state
        frames_counter = 0
        events = []
        while gm.draw(self.data.roads, self.data.lights, self.data.cars, self.data.junctions, events,
                      with_final_display=False):
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
