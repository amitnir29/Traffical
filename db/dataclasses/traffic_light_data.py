from dataclasses import dataclass
from typing import List

from db.dataclasses.road_lane import RoadLane
from simulation_objects.geometry.point import Point


@dataclass(init=True, repr=True)
class TrafficLightData:
    lanes: List[RoadLane]
    coordinate: Point
