from typing import List

import pygame

from graphics.menu.screens.screen_activity import Screen
from graphics.simaltion_graphics import SimulationGraphics
from server.cars_generator import generate_cars
from server.map_creation import create_map
from server.server_runner import next_iter
from server.statistics.stats_reporter import StatsReporter


class SimulationRunner(Screen):
    def __init__(self, screen: pygame.Surface, map_path, chosen_algo):
        super().__init__(screen)
        # get the simulation map
        roads, traffic_lights, all_junctions = create_map(self.screen.get_width(), self.screen.get_height(), map_path)
        self.roads = roads
        self.traffic_lights = traffic_lights
        self.junctions = all_junctions
        # init cars list
        self.cars = generate_cars(roads, 1, p=0.9, min_len=20, with_prints=False)
        # init traffic lights algorithm
        self.lights_algo = [chosen_algo(junction) for junction in all_junctions]
        # init simulation's stats reporter
        self.reporter = StatsReporter(self.cars, all_junctions)

    def display(self):
        gm = SimulationGraphics(self.screen, fps=10)
        gm.set_small_map(self.roads)
        # while the screen is not closed, draw the current state and calculate the next state
        frames_counter = 0
        while gm.draw(self.roads, self.traffic_lights, self.cars, self.junctions):
            frames_counter = frames_counter + 1
            traffic_lights, cars = next_iter(self.lights_algo, self.traffic_lights, self.cars)
            self.reporter.next_iter(cars)
        # when run is over, report the stats
        self.reporter.report()
