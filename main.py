from typing import List

from graphics.graphics_manager import GraphicsManager
from server.geometry.point import Point
from server.map_creation import create_map
from server.server_runner import next_iter
from server.simulation_objects.cars.car import Car
from server.simulation_objects.cars.position import Position
from algorithms.algos_list import *
from server.cars_generator import generate_cars, generate_car
from server.simulation_objects.trafficlights.traffic_light import TrafficLight
from server.statistics.stats_reporter import StatsReporter


def main():
    # create the graphics object
    win_width, win_height = (800, 800)
    gm = GraphicsManager(fps=10, width=win_width, height=win_height)

    # get the simulation map
    roads, traffic_lights, all_junctions = create_map(win_width, win_height)

    cars: List = generate_cars(roads, 14, p=1, min_len=6, with_prints=True)

    # while the screen is not closed, draw the current state and calculate the next state
    # light_algos = [NaiveAlgo(junction) for junction in all_junctions]
    # light_algos = [MCAlgo(junction) for junction in all_junctions]
    light_algos = [MCTL(junction) for junction in all_junctions]
    # light_algos = [RLQTL(junction) for junction in all_junctions]
    # light_algos = [RLQRS(junction) for junction in all_junctions]
    # lights_algorithm = NaiveAlgo(traffic_lights, all_junctions)
    # lights_algorithm = MCAlgo(traffic_lights, all_junctions)
    # lights_algorithm = MCTL(traffic_lights, all_junctions)

    # # run the simulation
    # frames_count = 0
    # while gm.draw(roads, traffic_lights, cars):
    #     traffic_lights, cars = next_iter(light_algos, traffic_lights, cars)
    #     frames_count += 1
    #     if frames_count % 10 == 0:
    #         cars.append(generate_car(roads, min_len=3))

    # run the simulation
    frames_count = 0
    # cars = list()
    # cars.append(Car([roads[26], roads[28], roads[16], roads[5], roads[6], roads[15], roads[24], roads[25]] * 5, 0))
    # cars.append(Car([roads[54], roads[55]]))
    i = 0

    reporter = StatsReporter(cars)

    while gm.draw(roads, traffic_lights, cars):
        i = i + 1
        print(i)
        traffic_lights, cars = next_iter(light_algos, traffic_lights, cars)

    print(reporter.report())

if __name__ == '__main__':
    main()
