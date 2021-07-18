from typing import List, Dict

from graphics.drawables.junction import DrawableJunction
from graphics.drawables.road import DrawableRoad
from graphics.drawables.traffic_light import DrawableLight


class GMData:
    def __init__(self, roads, juncs):
        self.roads: List[DrawableRoad] = roads
        self.juncs: List[DrawableJunction] = juncs
