from dataclasses import dataclass


@dataclass(init=True, repr=True)
class Camera:
    min_x: int
    min_y: int
    max_x: int
    max_y: int
    width: int
    height: int
