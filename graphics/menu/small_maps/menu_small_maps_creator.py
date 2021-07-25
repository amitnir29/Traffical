import os
from typing import List

from db.load_map_data import get_db_road_sections
from graphics.menu.small_maps.menu_small_map import MenuSmallMap
from server.simulation_objects.roadsections.i_road_section import IRoadSection
from server.simulation_objects.roadsections.road_section import RoadSection


def load_all_small_maps(screen, width, height, path: str = "db/databases") -> List[MenuSmallMap]:
    """
    :param path: should be the head path of the databases
    :param screen: screen to draw the menu small maps on
    :param width: width of the small maps
    :param height: height of the small maps
    :return: list of small maps of all database maps
    """
    small_maps: List[MenuSmallMap] = list()
    handmade = path + "/handmade"
    generated = path + "/generated"
    # first, loop on handmade:
    for dirname in os.listdir(handmade):
        full_path = handmade + "/" + dirname
        small_maps.append(__load_small_map(full_path, screen, width, height))
    # then, loop in generated:
    for dirname in os.listdir(generated):
        full_path = generated + "/" + dirname
        small_maps.append(__load_small_map(full_path, screen, width, height))
    # done. return all
    return small_maps


def __load_small_map(path: str, screen, width, height) -> MenuSmallMap:
    roads = __get_roads(path)
    return MenuSmallMap(path, screen, width, height, roads)


def __get_roads(path: str) -> List[IRoadSection]:
    roads: List[IRoadSection] = list()
    # create all roads
    for road_data in get_db_road_sections(path):
        roads.append(RoadSection(road_data, set()))
    return roads
