from dataclasses import dataclass


@dataclass(init=True, repr=True)
class CarState:
    driving: bool = False
    moving_lane: bool = False
    stopping: bool = False
    letting_car_in: bool = False
