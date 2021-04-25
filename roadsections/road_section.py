from typing import List, Tuple, Optional, Set

from db_dataclasses.road_data import RoadData
from geometry.line import Line
from geometry.point import Point
from lanes.i_lane import ILane
from lanes.lane import Lane
from lanes.notified_lane import NotifiedLane
from lanes.unnotified_lane import UnnotifiedLane
from roadsections.i_road_section import IRoadSection
from trafficlights.i_traffic_light import ITrafficLight


class RoadSection(IRoadSection):

    def __init__(self, road_data: RoadData, notified_lanes_nums: Set[int]):
        # data from road_data
        self.__id: int = road_data.idnum
        self.__coordinates: List[Tuple[Point, Point]] = road_data.coordinates
        self.__number_of_lanes: int = road_data.num_lanes
        self.__max_speed: float = road_data.max_speed
        self.__pcross: Tuple[bool, bool] = road_data.pcross
        self.__is_stop: bool = road_data.is_stop
        self.__is_yield: bool = road_data.is_yield
        self.__is_parking: bool = road_data.is_parking
        # else
        self.__lanes: List[ILane] = self.__create_lanes(road_data.num_lanes, notified_lanes_nums)

    @property
    def coordinates(self) -> List[Tuple[Point, Point]]:
        return self.__coordinates

    def __create_lanes(self, number_of_lanes: int, notified_lanes_nums: Set[int]) -> List[ILane]:
        # split the coordinates based on the number of lanes. also works for single laned road
        # first, one-time calculate the line of each points pair
        coordinates_lines = [Line(pair[0], pair[1]) for pair in self.__coordinates]
        # then, calculate all (number_of_lanes+1) points of each line
        coordinates_lines_split = [[line.split_by_ratio(ratio / number_of_lanes)
                                    for ratio in range(number_of_lanes + 1)] for line in coordinates_lines]
        # then, for each lane, create a list of all points that match the lane index
        lanes_coordinates = [[(coordinates_lines_split[points_pair_index][lane_left_index],
                               coordinates_lines_split[points_pair_index][lane_left_index + 1])
                              for points_pair_index in range(len(self.__coordinates))]
                             for lane_left_index in range(number_of_lanes)]
        # now, each index in the lanes_coordinates list is a list of coordinates points, as we wanted
        lanes: List[ILane] = list()
        for i in range(number_of_lanes):
            # now check if the lane should have a traffic light, and act accordingly
            if i in notified_lanes_nums:
                lanes.append(NotifiedLane(self, lanes_coordinates[i]))
            else:
                lanes.append(UnnotifiedLane(self, lanes_coordinates[i]))
        return lanes

    def get_lane(self, index: int) -> ILane:
        """
        :param index: index of lane from left, 0 based.
        :return: the lane in that index
        """
        return self.__lanes[index]

    def get_left_lane(self, curr: ILane) -> ILane:
        curr_index = self.__lanes.index(curr)
        if curr_index == 0:
            raise Exception("already at most left lane")
        return self.__lanes[curr_index - 1]

    def get_right_lane(self, curr: ILane) -> ILane:
        curr_index = self.__lanes.index(curr)
        if curr_index == len(self.__lanes) - 1:
            raise Exception("already at most right lane")
        return self.__lanes[curr_index - 1]

    @property
    def max_speed(self) -> float:
        return self.__max_speed
