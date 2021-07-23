from enum import Enum
from typing import List

import pygame.font

from graphics.colors import DARK_BLUE, WHITE
from graphics.menu.algos import all_algos_list, Algo
from graphics.menu.screens.algo_choosing import AlgoChoosing
from graphics.menu.screens.map_choosing import MapChoosing
from graphics.menu.screens.open_screen import OpenScreen
from graphics.menu.screens.simulation_runner import SimulationRunner
from graphics.menu.small_maps.menu_small_map import MenuSmallMap
from graphics.menu.small_maps.menu_small_maps_creator import load_all_small_maps
from server.geometry.point import Point


class Screens(Enum):
    OPEN = 0
    MAPS_SCREEN = 1
    MAPS_SCREEN_HELP = 1.5
    ALGOS_SCREEN = 2
    ALGOS_SCREEN_HELP = 2.5
    RUNNING = 3
    FINISH = 4


def run(screen: pygame.Surface, background=DARK_BLUE):
    open_screen = OpenScreen(screen, background)
    maps_screen = MapChoosing(screen, background)
    algos_screen = AlgoChoosing(screen, background)

    open_screen.display()
    map_path = maps_screen.display()
    chosen_algo = algos_screen.display()

    sim_runner = SimulationRunner(screen, map_path, chosen_algo)
    sim_runner.display()
