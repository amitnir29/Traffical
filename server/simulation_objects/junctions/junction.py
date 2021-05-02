from typing import List

from db.dataclasses.junction_data import JunctionData
from server.geometry.point import Point
import server.simulation_objects.junctions.i_junction as ij
import server.simulation_objects.roadsections.i_road_section as irs
import server.simulation_objects.trafficlights.i_traffic_light as itl
from server.simulation_objects.trafficlights import traffic_light as tl


class Junction(ij.IJunction):

    def update_traffic_lights(self, change: List[tl.TrafficLight]) -> None:
        # TODO
        pass

    def naive_algorithm(self) -> None:
        # TODO
        pass

    def __init__(self, junction_data: JunctionData, in_roads, out_roads, traffic_lights):
        self.__idnum: int = junction_data.idnum
        self.__in_roads: List[irs.IRoadSection] = in_roads
        self.__out_roads: List[irs.IRoadSection] = out_roads
        self.__lights: List[itl.ITrafficLight] = traffic_lights
        self.__coordinates: List[Point] = junction_data.coordinates

    @property
    def coordinates(self) -> List[Point]:
        return self.__coordinates
