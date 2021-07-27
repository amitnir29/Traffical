import pygame.font

from gui.gui_flow.comparison_path import run_comparison
from gui.gui_flow.simulation_path import run_simulation
from gui.screens.path_screens.map_choosing import MapChoosing
from gui.screens.path_screens.open_screen import OpenScreen
from gui.screens.screens_enum import Screens


def run(screen: pygame.Surface):
    __run_open_screen(screen)


def __run_open_screen(screen):
    maps_screen = MapChoosing(screen)  # to save computation time
    open_screen = OpenScreen(screen)
    path = open_screen.display()
    while True:
        if path == Screens.COMPARISON_PATH:
            run_comparison(screen, maps_screen)
        elif path == Screens.SIMULATION_PATH:
            run_simulation(screen, maps_screen)
        else:
            raise Exception("something is wrong")
        path = open_screen.display()
