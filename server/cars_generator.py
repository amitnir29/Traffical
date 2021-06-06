from typing import List
from random import random, choice

from server.simulation_objects.cars.car import Car
from server.simulation_objects.cars.i_car import ICar
from server.simulation_objects.roadsections.i_road_section import IRoadSection


def generate_car(roads: List[IRoadSection], p=0.95) -> ICar:
    start = choice(roads)
    path = [start]
    while random() < p:
        last_road = path[-1]
        next_roads = last_road.goes_to_roads()
        if len(next_roads) == 0:
            break
        chosen_next_road = choice(next_roads)
        path.append(chosen_next_road)
    return Car(path)
