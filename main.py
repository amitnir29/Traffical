from typing import List

from graphics.menu import screen_manager
from graphics.screen import create_screen, quit_screen
from graphics.simaltion_graphics import SimulationGraphics
from server.cars_generator import generate_cars
from server.map_creation import create_map
from server.server_runner import next_iter
from server.statistics.stats_reporter import StatsReporter


def main():
    # size of window
    win_width, win_height = (800, 800)
    screen = create_screen(win_width, win_height)
    # run the menu
    screen_manager.run(screen)
    # quit at the end
    quit_screen()


if __name__ == '__main__':
    main()
