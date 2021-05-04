from typing import List

import server.simulation_objects.lanes.i_notified_lane as nlane
import server.simulation_objects.trafficlights.i_traffic_light as itl
from server.geometry.point import Point


class TrafficLight(itl.ITrafficLight):

    def changeLight(self) -> None:
        self.__can_pass = not self.__can_pass

    def __init__(self, lanes: List[nlane.INotifiedLane], coordinate: Point):
        self.__can_pass = False
        self.__coming_from_lanes = lanes
        # set the lanes to have this traffic light
        for lane in lanes:
            lane.traffic_light = self
        self.__coordinate = coordinate

    @property
    def can_pass(self) -> bool:
        return self.__can_pass

    @property
    def coordinate(self) -> Point:
        return self.__coordinate