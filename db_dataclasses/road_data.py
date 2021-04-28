from dataclasses import dataclass
from typing import Tuple, List

from geometry.point import Point


@dataclass(init=True, repr=True)
class RoadData:
    idnum: int
    coordinates: List[Tuple[Point, Point]]
    num_lanes: int
    max_speed: float
    is_parking: bool
