from gui.screens.path_screens.algo_choosing import AlgoChoosing
from gui.screens.path_screens.configuration_screen import ConfigurationScreen
from gui.screens.path_screens.finish_screen import FinishScreen
from gui.screens.screens_enum import Screens
from gui.screens.path_screens.simulation_runner import SimulationConfiguration, SimulationRunner
from gui.screens.stats_screens.simulation_stats_screen import SimulationStatsScreen


def run_simulation(screen, maps_screen):
    __simulation_maps_screen(screen, maps_screen)


def __simulation_maps_screen(screen, maps_screen):
    conf = SimulationConfiguration()
    while True:
        res = maps_screen.display()
        if res == Screens.BACK:
            return
        conf.map_path = res
        __simulation_algos_screen(screen, conf)


def __simulation_algos_screen(screen, conf):
    algos_screen = AlgoChoosing(screen, simulation_mode=True)
    while True:
        res = algos_screen.display()
        if res == Screens.BACK:
            return
        conf.chosen_algo = res[0].algo_class
        __simulation_conf_screen(screen, conf)


def __simulation_conf_screen(screen, conf):
    conf_screen = ConfigurationScreen(screen, simulation_mode=True)
    while True:
        res = conf_screen.display()
        if res == Screens.BACK:
            return
        cars_amount, path_min_len, is_small_map = res
        conf.cars_amount = cars_amount
        conf.path_min_len = path_min_len
        conf.is_small_map = is_small_map
        __simulation_run_simulation(screen, conf)


def __simulation_run_simulation(screen, conf):
    try:
        sim_runner = SimulationRunner(screen, conf)
    except:
        return
    reporter = sim_runner.display()
    __simulation_finish_screen(screen, reporter)


def __simulation_finish_screen(screen, reporter):
    stats_screen = SimulationStatsScreen(screen, reporter)
    finish_screen = FinishScreen(screen, stats_screen)
    finish_screen.display()
