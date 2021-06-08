from typing import List
from random import random, choice

from server.simulation_objects.cars.car import Car
from server.simulation_objects.cars.i_car import ICar
from server.simulation_objects.roadsections.i_road_section import IRoadSection

DEF_P = 0.95
WITH_PRINTS = False
MIN_LEN = 1


def generate_cars(roads, amount: int, p=DEF_P, min_len=MIN_LEN, with_prints=WITH_PRINTS) -> List[ICar]:
    return [generate_car(roads, p, min_len, with_prints) for _ in range(amount)]


def generate_car(roads: List[IRoadSection], p=DEF_P, min_len=MIN_LEN, with_prints=WITH_PRINTS) -> ICar:
    start = choice(roads)
    path = [start]
    while random() < p:
        last_road = path[-1]
        next_roads = last_road.goes_to_roads()
        if len(next_roads) == 0:
            break
        chosen_next_road = choice(next_roads)
        path.append(chosen_next_road)

    if len(path) < min_len:
        return generate_car(roads, p, min_len, with_prints)
    if with_prints:
        print(path)
    return Car(path)
