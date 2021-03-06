from typing import List
from copy import deepcopy

import server.simulation_objects.junctions.i_junction as ij
import server.simulation_objects.roadsections.i_road_section as irs
import server.simulation_objects.trafficlights.i_traffic_light as itl
from db.dataclasses.junction_data import JunctionData
from server.geometry.point import Point
from server.simulation_objects.trafficlights.i_traffic_light import ITrafficLight


class Junction(ij.IJunction):
    def __init__(self, junction_data: JunctionData, in_roads, out_roads, traffic_lights):
        self.__idnum: int = junction_data.idnum
        self.__in_roads: List[irs.IRoadSection] = in_roads
        self._out_roads: List[irs.IRoadSection] = out_roads
        self.__lights: List[itl.ITrafficLight] = traffic_lights
        self.__coordinates: List[Point] = deepcopy(junction_data.coordinates)

        self._algo = None

    def set_algo(self, algo):
        self._algo = algo

    @property
    def coordinates(self) -> List[Point]:
        return self.__coordinates

    @property
    def lights(self) -> List[ITrafficLight]:
        return self.__lights

    def __repr__(self):
        return str(self.__idnum)
