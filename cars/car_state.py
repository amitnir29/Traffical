from dataclasses import dataclass


@dataclass(init=True, repr=True)
class CarState:
    driving: bool = True
    moving_lane: bool = False
    stopping: bool = False
    letting_car_in: bool = False

    def __setattr__(self, key, value):
        super.__setattr__(self, key, value)
        self.__dict__['driving'] = not (self.moving_lane or self.stopping or self.letting_car_in)
