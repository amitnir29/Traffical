import pygame.font

from gui.gui_flow.comparison_path import run_comparison
from gui.gui_flow.simulation_path import run_simulation
from gui.screens.map_choosing import MapChoosing
from gui.screens.open_screen import OpenScreen
from gui.screens.screens_enum import Screens
from gui.simulation_graphics.colors import DARK_BLUE


def run(screen: pygame.Surface, background=DARK_BLUE):
    __run_open_screen(screen, background)


def __run_open_screen(screen, background):
    maps_screen = MapChoosing(screen, background)  # to save computation time
    open_screen = OpenScreen(screen, background)
    path = open_screen.display()
    while True:
        if path == Screens.COMPARISON_PATH:
            run_comparison(screen, background, maps_screen)
        elif path == Screens.SIMULATION_PATH:
            run_simulation(screen, background, maps_screen)
        else:
            raise Exception("something is wrong")
        path = open_screen.display()
