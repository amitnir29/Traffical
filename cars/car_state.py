from dataclasses import dataclass
from typing import Optional

from cars.i_car import ICar
from lanes.i_lane import ILane


@dataclass(init=True, repr=True)
class CarState:
    driving: bool = True
    moving_lane: Optional[ILane] = None
    stopping: bool = False
    letting_car_in: Optional[ICar] = None

    def __setattr__(self, key, value):
        super.__setattr__(self, key, value)
        self.__dict__['driving'] = not (self.moving_lane is not None or
                                        self.stopping or self.letting_car_in is not None)
