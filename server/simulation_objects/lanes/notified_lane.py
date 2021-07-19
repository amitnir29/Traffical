from typing import List, Tuple

from server.geometry.point import Point
import server.simulation_objects.lanes.i_notified_lane as inlane
import server.simulation_objects.lanes.lane as lane
import server.simulation_objects.roadsections.i_road_section as irs
import server.simulation_objects.trafficlights.i_traffic_light as itl


class NotifiedLane(inlane.INotifiedLane, lane.Lane):
    def __init__(self, road: irs.IRoadSection, coordinates: List[Tuple[Point, Point]]):
        lane.Lane.__init__(self, road, coordinates)
        self.__light = None

    @property
    def traffic_light(self) -> itl.ITrafficLight:
        return self.__light

    @traffic_light.setter
    def traffic_light(self, new_traffic_light):
        if self.__light is not None:
            raise Exception("traffic light is already set!")
        self.__light = new_traffic_light
