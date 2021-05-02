from typing import List, Tuple, Set

from db.dataclasses.road_data import RoadData
from server.geometry.line import Line
from server.geometry.point import Point

import server.simulation_objects.lanes.i_lane as il
import server.simulation_objects.lanes.notified_lane as nlane
import server.simulation_objects.lanes.unnotified_lane as unlane
import server.simulation_objects.roadsections.i_road_section as irs


class RoadSection(irs.IRoadSection):

    def __init__(self, road_data: RoadData, notified_lanes_nums: Set[int]):
        # data from road_data
        self.__id: int = road_data.idnum
        self.__coordinates: List[Tuple[Point, Point]] = road_data.coordinates
        self.__number_of_lanes: int = road_data.num_lanes
        self.__max_speed: float = road_data.max_speed
        self.__lanes: List[il.ILane] = self.__create_lanes(road_data.num_lanes, notified_lanes_nums)

    @property
    def coordinates(self) -> List[Tuple[Point, Point]]:
        return self.__coordinates

    def __create_lanes(self, number_of_lanes: int, notified_lanes_nums: Set[int]) -> List[il.ILane]:
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
        lanes: List[il.ILane] = list()
        for i in range(number_of_lanes):
            # now check if the lane should have a traffic light, and act accordingly
            if i in notified_lanes_nums:
                lanes.append(nlane.NotifiedLane(self, lanes_coordinates[i]))
            else:
                lanes.append(unlane.UnnotifiedLane(self, lanes_coordinates[i]))
        return lanes

    def get_lane(self, index: int) -> il.ILane:
        """
        :param index: index of lane from left, 0 based.
        :return: the lane in that index
        """
        return self.__lanes[index]

    def get_left_lane(self, curr: il.ILane) -> il.ILane:
        curr_index = self.__lanes.index(curr)
        if curr_index == 0:
            raise Exception("already at most left lane")
        return self.__lanes[curr_index - 1]

    def get_most_right_lane_index(self) -> int:
        return len(self.__lanes) - 1

    def get_right_lane(self, curr: il.ILane) -> il.ILane:
        curr_index = self.__lanes.index(curr)
        if curr_index == len(self.__lanes) - 1:
            raise Exception("already at most right lane")
        return self.__lanes[curr_index - 1]

    @property
    def max_speed(self) -> float:
        return self.__max_speed

    @property
    def lanes(self) -> List[il.ILane]:
        return self.__lanes

    def get_lines_between_lanes(self) -> List[List[Point]]:
        # main list's length is number of lanes - 1, number of points for each line is length of coordinates list
        lines = list()
        for line_num in range(self.__number_of_lanes - 1):
            # add the right side points of the lanes, except from the most right lane
            lines.append([pair[1] for pair in self.__lanes[line_num].coordinates])
        return lines
