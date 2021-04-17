from typing import List, Dict

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
        self.__cars: List[ICar] = list()  # TODO should be a linked list?
        self.__goes_to: Dict[IRoadSection] = dict()
        self.__light: ITrafficLight  # TODO
        self.__vertical: bool

    @property
    def is_vertical(self):
        return self.__vertical
