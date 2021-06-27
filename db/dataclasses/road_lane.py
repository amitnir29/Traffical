from dataclasses import dataclass


@dataclass(init=True, repr=True, eq=True, unsafe_hash=True)
class RoadLane:
    road_id: int
    lane_num: int
