from typing import List

from db_dataclasses.junction_data import JunctionData
from geometry.point import Point
import junctions.i_junction as ij
import roadsections.i_road_section as irs
import trafficlights.i_traffic_light as itl


class Junction(ij.IJunction):
    def __init__(self, junction_data: JunctionData, in_roads, out_roads, traffic_lights):
        self.__idnum: int = junction_data.idnum
        self.__in_roads: List[irs.IRoadSection] = in_roads
        self.__out_roads: List[irs.IRoadSection] = out_roads
        self.__lights: List[itl.ITrafficLight] = traffic_lights
        self.__coordinates: List[Point] = junction_data.coordinates
