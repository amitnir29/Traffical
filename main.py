from typing import List

from graphics.menu.menu import Menu
from graphics.screen import create_screen, finish_screen
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
    menu = Menu(screen)
    map_path, chosen_algo = menu.run()

    # get the simulation map
    roads, traffic_lights, all_junctions = create_map(win_width, win_height, map_path)
    # init cars list
    cars: List = generate_cars(roads, 10, p=0.9, min_len=20, with_prints=False)
    # init traffic lights algorithm
    light_algos = [chosen_algo(junction) for junction in all_junctions]
    # init simulation's stats reporter
    reporter = StatsReporter(cars, all_junctions)

    # create the graphics manager
    gm = SimulationGraphics(screen, fps=10)
    gm.set_small_map(roads)
    # while the screen is not closed, draw the current state and calculate the next state
    frames_counter = 0
    while gm.draw(roads, traffic_lights, cars, all_junctions):
        frames_counter = frames_counter + 1
        traffic_lights, cars = next_iter(light_algos, traffic_lights, cars)
        reporter.next_iter(cars)
    finish_screen()
    # when run is over, report the stats
    reporter.report()


if __name__ == '__main__':
    main()
