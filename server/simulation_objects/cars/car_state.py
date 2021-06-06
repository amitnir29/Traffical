from dataclasses import dataclass
from typing import Optional

import server.simulation_objects.cars.i_car as ic
import server.simulation_objects.lanes.i_lane as il


@dataclass(init=True, repr=True)
class CarState:
    driving: bool = True
    moving_lane: Optional[il.ILane] = None
    stopping: bool = False
    letting_car_in: Optional[ic.ICar] = None

    def __setattr__(self, key, value):
        super.__setattr__(self, key, value)
        self.__dict__['driving'] = not (self.moving_lane is not None or
                                        self.stopping or self.letting_car_in is not None)
