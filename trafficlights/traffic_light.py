from typing import List

import lanes.i_notified_lane as nlane
import trafficlights.i_traffic_light as itl


class TrafficLight(itl.ITrafficLight):

    def changeLight(self) -> None:
        self.__can_pass = not self.__can_pass

    def __init__(self, lanes: List[nlane.INotifiedLane]):
        self.__can_pass = False
        self.__coming_from_lanes = lanes
        # set the lanes to have this traffic light
        for lane in lanes:
            lane.traffic_light = self

    def can_pass(self) -> bool:
        return self.__can_pass
