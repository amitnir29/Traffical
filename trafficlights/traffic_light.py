from typing import List

from lanes.i_lane import ILane
from trafficlights.i_traffic_light import ITrafficLight


class TrafficLight(ITrafficLight):

    def __init__(self, lanes: List[ILane]):
        self.__can_pass = False
        self.__coming_from_lanes = lanes

    def can_pass(self) -> bool:
        return self.__can_pass
