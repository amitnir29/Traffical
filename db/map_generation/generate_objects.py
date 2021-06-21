from db.dataclasses.junction_data import JunctionData
from db.dataclasses.road_data import RoadData
from server.geometry.point import Point


def generate_junc():
    coors = [Point(100, 100), Point(100, 150), Point(160, 180), Point(140, 150)]
    x = JunctionData(idnum=0, coordinates=coors, goes_to=[])
    return x
