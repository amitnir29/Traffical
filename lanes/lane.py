from typing import List, Dict, Optional
from collections import deque

from cars.i_car import ICar
from lanes.i_lane import ILane
from roadsections.i_road_section import IRoadSection
from trafficlights.i_traffic_light import ITrafficLight


class Lane(ILane):
    def __init__(self):
        """
        public LinkedList<ICar> cars = new LinkedList<ICar>();
        public Dictionary<RoadSection, Lane> goesTo = new Dictionary<RoadSection, Lane>();
        public TrafficLight light;
        """
        self.__cars = deque()
        self.__goes_to: Dict[IRoadSection] = dict()
        self.__light: ITrafficLight  # TODO
        self.__vertical: bool
        self.__length: float

    @property
    def is_vertical(self):
        return self.__vertical

    def get_car_ahead(self, car: ICar) -> Optional[ICar]:
        car_index = self.__cars.index(car)

        if car_index == 0:
            return None

        return self.__cars[car_index - 1]

    def cars_amount(self) -> int:
        return len(self.__cars)

    def add_car(self, car):
        self.__cars.append(car)

    def remove_car(self, car):
        self.__cars.remove(car)

    def cars_from_end(self, distance: float) -> List[ICar]:
        return self.get_cars_between(self.__length - distance, self.__length)

    def get_cars_between(self, start: float, end: float) -> List[ICar]:
        res = list()

        for car in reversed(self.__cars):
            position_in_line = self.car_position_in_lane(car)

            if start <= position_in_line <= end:
                res.append(car)

            elif position_in_line < start:
                break

        return res

    def car_position_in_lane(self, car):
        return car.position.y if self.is_vertical else car.position.x

