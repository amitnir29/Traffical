from typing import List, Tuple

from geometry.point import Point
from lanes.i_notified_lane import INotifiedLane
from lanes.lane import Lane
from roadsections.i_road_section import IRoadSection
from trafficlights.i_traffic_light import ITrafficLight


class NotifiedLane(INotifiedLane, Lane):

    def __init__(self, road: IRoadSection, coordinates: List[Tuple[Point, Point]], vertical: bool = False):
        Lane.__init__(self, road, coordinates, vertical)
        self.__light = None

    @property
    def traffic_light(self) -> ITrafficLight:
        return self.__light

    @traffic_light.setter
    def traffic_light(self, new_traffic_light):
        if self.__light is not None:
            raise Exception("traffic light is already set!")
        self.__light = new_traffic_light
