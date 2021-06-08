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


def main():
    # create the graphics object
    win_width, win_height = (800, 800)
    gm = GraphicsManager(fps=10, width=win_width, height=win_height)

    # get the simulation map
    roads, traffic_lights, all_junctions = create_map(win_width, win_height)

    cars: List = generate_cars(roads, 4, p=1, min_len=6, with_prints=True)

    # while the screen is not closed, draw the current state and calculate the next state
    # lights_algorithm = NaiveAlgo(traffic_lights, all_junctions)
    # lights_algorithm = MCAlgo(traffic_lights, all_junctions)
    lights_algorithm = MCTL(traffic_lights, all_junctions)

    # run the simulation
    frames_count = 0
    while gm.draw(roads, traffic_lights, cars):
        traffic_lights, cars = next_iter(lights_algorithm, traffic_lights, cars)
        frames_count += 1
        if frames_count % 10 == 0:
            cars.append(generate_car(roads, min_len=3))


if __name__ == '__main__':
    main()
