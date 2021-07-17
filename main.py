from typing import List

from algorithms.cost_based import CostBased
from algorithms.naive import NaiveAlgo
from graphics.graphics_manager import GraphicsManager
from server.cars_generator import generate_cars
from server.map_creation import create_map
from server.server_runner import next_iter
from server.statistics.stats_reporter import StatsReporter


def main():
    # size of window
    win_width, win_height = (800, 800)
    # get the simulation map
    roads, traffic_lights, all_junctions = create_map(win_width, win_height, "db/databases/generated/10")
    # init cars list
    cars: List = generate_cars(roads, 3, p=0.9, min_len=20, with_prints=True)
    # init traffic lights algorithm
    light_algos = choose_algorithm(all_junctions)
    # init simulation's stats reporter
    reporter = StatsReporter(cars, all_junctions)
    # create the graphics manager
    gm = GraphicsManager(width=win_width, height=win_height, fps=10)
    gm.set_small_map(roads, all_junctions)
    # while the screen is not closed, draw the current state and calculate the next state
    frames_counter = 0
    while gm.draw(roads, traffic_lights, cars, all_junctions):
        frames_counter = frames_counter + 1
        traffic_lights, cars = next_iter(light_algos, traffic_lights, cars)
        reporter.next_iter(cars)
    # when run is over, report the stats
    reporter.report()


def choose_algorithm(all_junctions):
    # return [NaiveAlgo(junction) for junction in all_junctions]
    # return [MCAlgo(junction) for junction in all_junctions]
    # return [MCTL(junction) for junction in all_junctions]
    # return [RLQTL(junction) for junction in all_junctions]
    # return [RLQRS(junction) for junction in all_junctions]
    return [CostBased(junction) for junction in all_junctions]


if __name__ == '__main__':
    main()
