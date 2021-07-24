from enum import Enum
from typing import List

import pygame.font

from graphics.colors import DARK_BLUE, WHITE
from graphics.menu.algos import all_algos_list, Algo
from graphics.menu.screens.algo_choosing import AlgoChoosing
from graphics.menu.screens.configuration_screen import ConfigurationScreen
from graphics.menu.screens.finish_screen import FinishScreen
from graphics.menu.screens.map_choosing import MapChoosing
from graphics.menu.screens.open_screen import OpenScreen
from graphics.menu.screens.simulation_runner import SimulationRunner, SimulationConfiguration
from graphics.menu.screens.stats_screen import StatsScreen
from graphics.menu.screens_enum import Screens
from graphics.menu.small_maps.menu_small_map import MenuSmallMap
from graphics.menu.small_maps.menu_small_maps_creator import load_all_small_maps
from server.geometry.point import Point


def run(screen: pygame.Surface, background=DARK_BLUE):
    __run_open_screen(screen, background)


# def run_simulation_path(open_screen, screen: pygame.Surface, background=DARK_BLUE):
#
#
#
#
#
#     __run_maps_screen(conf, open_screen, maps_screen)
#     __run_algos_screen(conf, open_screen, maps_screen, algos_screen)
#     __run_conf_screen(conf, open_screen, maps_screen, algos_screen, conf_screen)
#
#     sim_runner = SimulationRunner(screen, conf)
#     reporter = sim_runner.display()
#
#     stats_screen = StatsScreen(screen, background, reporter)
#     finish_screen = FinishScreen(screen, background, stats_screen)
#     finish_screen.display()

def __run_open_screen(screen, background):
    open_screen = OpenScreen(screen, background)
    path = open_screen.display()
    while True:
        if path == Screens.COMPARISON_PATH:
            pass
        elif path == Screens.SIMULATION_PATH:
            __run_maps_screen(screen, background)
        else:
            raise Exception("something is wrong")
        path = open_screen.display()


def __run_maps_screen(screen, background):
    maps_screen = MapChoosing(screen, background)
    conf = SimulationConfiguration()
    while True:
        res = maps_screen.display()
        if res == Screens.BACK:
            return
        conf.map_path = res
        __run_algos_screen(screen, background, conf)


def __run_algos_screen(screen, background, conf):
    algos_screen = AlgoChoosing(screen, background)
    while True:
        res = algos_screen.display()
        if res == Screens.BACK:
            return
        conf.chosen_algo = res
        __run_conf_screen(screen, background, conf)


def __run_conf_screen(screen, background, conf):
    conf_screen = ConfigurationScreen(screen, background)
    while True:
        res = conf_screen.display()
        if res == Screens.BACK:
            return
        cars_amount, path_min_len, is_small_map = res
        conf.cars_amount = cars_amount
        conf.path_min_len = path_min_len
        conf.is_small_map = is_small_map
        __run_simulation(screen, background, conf)


def __run_simulation(screen, background, conf):
    sim_runner = SimulationRunner(screen, conf)
    reporter = sim_runner.display()
    __run_finish_screen(screen, background, reporter)


def __run_finish_screen(screen, background, reporter):
    stats_screen = StatsScreen(screen, background, reporter)
    finish_screen = FinishScreen(screen, background, stats_screen)
    finish_screen.display()
