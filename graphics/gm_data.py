from typing import List

from graphics.drawables.junction import DrawableJunction
from graphics.drawables.road import DrawableRoad


class GMData:
    def __init__(self, roads, juncs):
        self.roads: List[DrawableRoad] = roads
        self.juncs: List[DrawableJunction] = juncs
