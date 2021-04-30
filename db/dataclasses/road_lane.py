from dataclasses import dataclass


@dataclass(init=True, repr=True)
class RoadLane:
    road_id: int
    lane_num: int
