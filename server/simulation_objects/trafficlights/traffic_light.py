from copy import deepcopy
from typing import List

import server.simulation_objects.lanes.i_notified_lane as nlane
import server.simulation_objects.trafficlights.i_traffic_light as itl
from server.geometry.point import Point


class TrafficLight(itl.ITrafficLight):

    def change_light(self, turn_to_green) -> None:
        if self.__can_pass != turn_to_green:
            self.__light_time = 0
        self.__can_pass = turn_to_green

    def __init__(self, lanes: List[nlane.INotifiedLane], coordinate: Point):
        self.__can_pass = False
        self.__coming_from_lanes = lanes
        self.__light_time = 0
        # set the lanes to have this traffic light
        for lane in lanes:
            lane.traffic_light = self
        self.__coordinate = deepcopy(coordinate)

    @property
    def can_pass(self) -> bool:
        return self.__can_pass

    @property
    def coordinate(self) -> Point:
        return self.__coordinate

    def activate(self):
        self.__light_time += 1

    @property
    def light_time(self):
        return self.__light_time

    @property
    def lanes(self) -> List[nlane.INotifiedLane]:
        return self.__coming_from_lanes

    @property
    def all_cars(self):
        return sum([[car for car in lane.get_all_cars()] for lane in self.lanes], [])

    def reset_time(self):
        self.__light_time = 0
