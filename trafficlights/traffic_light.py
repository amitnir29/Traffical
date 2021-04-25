from typing import List

from lanes.i_lane import ILane
from lanes.i_notified_lane import INotifiedLane
from trafficlights.i_traffic_light import ITrafficLight


class TrafficLight(ITrafficLight):

    def __init__(self, lanes: List[INotifiedLane]):
        self.__can_pass = False
        self.__coming_from_lanes = lanes
        # set the lanes to have this traffic light
        for lane in lanes:
            lane.traffic_light = self

    def can_pass(self) -> bool:
        return self.__can_pass
