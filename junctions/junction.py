from typing import List

from db_dataclasses.junction_data import JunctionData
from geometry.point import Point
from junctions.i_junction import IJunction
from roadsections.i_road_section import IRoadSection
from trafficlights.i_traffic_light import ITrafficLight


class Junction(IJunction):
    def __init__(self, junction_data: JunctionData, in_roads, out_roads, traffic_lights):
        self.__idnum: int = junction_data.idnum
        self.__in_roads: List[IRoadSection] = in_roads
        self.__out_roads: List[IRoadSection] = out_roads
        self.__lights: List[ITrafficLight] = traffic_lights
        self.__coordinates: List[Point] = junction_data.coordinates
