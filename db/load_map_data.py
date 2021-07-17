from typing import List

from db.dataclasses.junction_data import JunctionData
from db.dataclasses.road_data import RoadData
from db.pickle_help import jsonpickle_from_file


def get_db_road_sections(path) -> List[RoadData]:
    return jsonpickle_from_file(path + "/RoadSections.json")


def get_db_junctions(path) -> List[JunctionData]:
    return jsonpickle_from_file(path + "/Junctions.json")
