from typing import List

from junctions.i_junction import IJunction
from trafficlights.traffic_light import TrafficLight


class Junction(IJunction):
    def __init__(self):
        lights: List[TrafficLight] = list()  # TODO
