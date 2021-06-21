from typing import List

from db.dataclasses.junction_data import JunctionData
from db.dataclasses.road_data import RoadData
from db.pickle_help import jsonpickle_to_file


def save_junctions(junctions: List[JunctionData], path):
    jsonpickle_to_file(junctions, path + "/Junctions.json")


def save_road_sections(roads: List[RoadData], path):
    jsonpickle_to_file(roads, path + "/RoadSections.json")
