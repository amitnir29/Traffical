from typing import List

import pygame

from graphics.menu.screens.screen_activity import Screen
from graphics.simaltion_graphics import SimulationGraphics
from server.cars_generator import generate_cars
from server.map_creation import create_map
from server.server_runner import next_iter
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


class SimulationRunner(Screen):
    def __init__(self, screen: pygame.Surface, conf: SimulationConfiguration):
        super().__init__(screen)
        # get the simulation map
        map_path, chosen_algo, cars_amount, path_min_len, is_small_map = conf.to_tuple()
        roads, traffic_lights, all_junctions = create_map(self.screen.get_width(), self.screen.get_height(), map_path)
        self.roads = roads
        self.traffic_lights = traffic_lights
        self.junctions = all_junctions
        # init cars list
        self.cars = generate_cars(roads, cars_amount, p=0.9, min_len=path_min_len, with_prints=False)
        # init traffic lights algorithm
        self.lights_algo = [chosen_algo(junction) for junction in all_junctions]
        # init simulation's stats reporter
        self.reporter = StatsReporter(self.cars, all_junctions)
        self.with_small_map = is_small_map

    def display(self) -> StatsReporter:
        gm = SimulationGraphics(self.screen, fps=10)
        if self.with_small_map:
            gm.set_small_map(self.roads)
        # while the screen is not closed, draw the current state and calculate the next state
        frames_counter = 0
        while gm.draw(self.roads, self.traffic_lights, self.cars, self.junctions):
            frames_counter = frames_counter + 1
            traffic_lights, cars = next_iter(self.lights_algo, self.traffic_lights, self.cars)
            self.reporter.next_iter(cars)
        # when run is over, report the stats
        return self.reporter
