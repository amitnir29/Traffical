# COMPARISON PATH
from gui.screens.algo_choosing import AlgoChoosing
from gui.screens.configuration_screen import ConfigurationScreen
from gui.screens.finish_screen import FinishScreen
from gui.screens.screens_enum import Screens
from gui.screens.simulation_runner import ComparisonConfiguration, SimulationRunner
from gui.screens.stats_screens.comparison_stats_screen import ComparisonStatsScreen


def run_comparison(screen, background, maps_screen):
    __comparison_maps_screen(screen, background, maps_screen)


def __comparison_maps_screen(screen, background, maps_screen):
    conf = ComparisonConfiguration()
    while True:
        res = maps_screen.display()
        if res == Screens.BACK:
            return
        conf.map_path = res
        __comparison_algos_screen(screen, background, conf)


def __comparison_algos_screen(screen, background, conf):
    algos_screen = AlgoChoosing(screen, background, simulation_mode=False)
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
        cars_amount, path_min_len, show_runs = res
        conf.cars_amount = cars_amount
        conf.path_min_len = path_min_len
        conf.show_runs = show_runs
        __comparison_run_simulation(screen, background, conf)


def __comparison_run_simulation(screen, background, conf):
    try:
        sim_runner = SimulationRunner(screen, conf)
    except:
        return
    reporters = sim_runner.run_silent()
    __comparison_finish_screen(screen, background, reporters)


def __comparison_finish_screen(screen, background, reporters):
    stats_screen = ComparisonStatsScreen(screen, background, reporters)
    finish_screen = FinishScreen(screen, background, stats_screen)
    finish_screen.display()
