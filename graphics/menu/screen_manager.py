import pygame.font

from graphics.colors import DARK_BLUE
from graphics.menu.screens.algo_choosing import AlgoChoosing
from graphics.menu.screens.configuration_screen import ConfigurationScreen
from graphics.menu.screens.finish_screen import FinishScreen
from graphics.menu.screens.map_choosing import MapChoosing
from graphics.menu.screens.open_screen import OpenScreen
from graphics.menu.screens.simulation_runner import SimulationRunner, SimulationConfiguration, ComparisonConfiguration
from graphics.menu.screens.stats_screens.comparison_stats_screen import ComparisonStatsScreen
from graphics.menu.screens.stats_screens.simulation_stats_screen import SimulationStatsScreen
from graphics.menu.screens_enum import Screens


def run(screen: pygame.Surface, background=DARK_BLUE):
    __run_open_screen(screen, background)


def __run_open_screen(screen, background):
    maps_screen = MapChoosing(screen, background) # to save computation time
    open_screen = OpenScreen(screen, background)
    path = open_screen.display()
    while True:
        if path == Screens.COMPARISON_PATH:
            __comparison_maps_screen(screen, background, maps_screen)
        elif path == Screens.SIMULATION_PATH:
            __simulation_maps_screen(screen, background, maps_screen)
        else:
            raise Exception("something is wrong")
        path = open_screen.display()


# SIMULATION PATH
def __simulation_maps_screen(screen, background, maps_screen):

    conf = SimulationConfiguration()
    while True:
        res = maps_screen.display()
        if res == Screens.BACK:
            return
        conf.map_path = res
        __simulation_algos_screen(screen, background, conf)


def __simulation_algos_screen(screen, background, conf):
    algos_screen = AlgoChoosing(screen, background, 1)
    while True:
        res = algos_screen.display()
        if res == Screens.BACK:
            return
        conf.chosen_algo = res[0].algo_class
        __simulation_conf_screen(screen, background, conf)


def __simulation_conf_screen(screen, background, conf):
    conf_screen = ConfigurationScreen(screen, background, simulation_mode=True)
    while True:
        res = conf_screen.display()
        if res == Screens.BACK:
            return
        cars_amount, path_min_len, is_small_map = res
        conf.cars_amount = cars_amount
        conf.path_min_len = path_min_len
        conf.is_small_map = is_small_map
        __simulation_run_simulation(screen, background, conf)


def __simulation_run_simulation(screen, background, conf):
    sim_runner = SimulationRunner(screen, conf)
    reporter = sim_runner.display()
    __simulation_finish_screen(screen, background, reporter)


def __simulation_finish_screen(screen, background, reporter):
    stats_screen = SimulationStatsScreen(screen, background, reporter)
    finish_screen = FinishScreen(screen, background, stats_screen)
    finish_screen.display()


# COMPARISON PATH
def __comparison_maps_screen(screen, background, maps_screen):
    conf = ComparisonConfiguration()
    while True:
        res = maps_screen.display()
        if res == Screens.BACK:
            return
        conf.map_path = res
        __comparison_algos_screen(screen, background, conf)


def __comparison_algos_screen(screen, background, conf):
    algos_screen = AlgoChoosing(screen, background, 2)
    while True:
        res = algos_screen.display()
        if res == Screens.BACK:
            return
        conf.chosen_algos = [algo.algo_class for algo in res]
        __comparison_conf_screen(screen, background, conf)


def __comparison_conf_screen(screen, background, conf):
    conf_screen = ConfigurationScreen(screen, background, simulation_mode=False)
    while True:
        res = conf_screen.display()
        if res == Screens.BACK:
            return
        cars_amount, path_min_len, _ = res
        conf.cars_amount = cars_amount
        conf.path_min_len = path_min_len
        __comparison_run_simulation(screen, background, conf)


def __comparison_run_simulation(screen, background, conf):
    sim_runner = SimulationRunner(screen, conf)
    reporters = sim_runner.run_silent()
    __comparison_finish_screen(screen, background, reporters)


def __comparison_finish_screen(screen, background, reporters):
    stats_screen = ComparisonStatsScreen(screen, background, reporters)
    finish_screen = FinishScreen(screen, background, stats_screen)
    finish_screen.display()
