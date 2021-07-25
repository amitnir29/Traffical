from typing import List, Optional
from random import random, choice

from server.simulation_objects.cars.car import Car
from server.simulation_objects.cars.i_car import ICar
from server.simulation_objects.roadsections.i_road_section import IRoadSection

DEF_P = 0.95
WITH_PRINTS = False
MIN_LEN = 1


def generate_cars(roads, amount: int, p=DEF_P, min_len=MIN_LEN, with_prints=WITH_PRINTS) -> Optional[List[ICar]]:
    tries = 0
    cars = list()
    while len(cars) < amount:
        if tries == 100 * amount:
            return None
        car = generate_car(roads, p, min_len, with_prints)
        if car is not None:
            cars.append(car)
        tries += 1
    return cars


def generate_car(roads: List[IRoadSection],  p=DEF_P, min_len=MIN_LEN, with_prints=WITH_PRINTS) -> Optional[ICar]:
    if p < 0.01 or p > 0.99:
        raise Exception("p should be in [0.01,0.99]")

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
        return None
    if with_prints:
        print(path)
    return Car(path)
