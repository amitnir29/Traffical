from collections import defaultdict
from typing import Dict, List, Tuple, Set

from db.dataclasses.junction_data import JunctionData
from db.dataclasses.road_data import RoadData
from db.dataclasses.road_lane import RoadLane
from db.dataclasses.traffic_light_data import TrafficLightData
from db.load_map_data import get_db_junctions, get_db_road_sections
from server.geometry.point import Point
from server.simulation_objects.junctions.i_junction import IJunction
from server.simulation_objects.junctions.junction import Junction
from server.simulation_objects.roadsections.i_road_section import IRoadSection
from server.simulation_objects.roadsections.road_section import RoadSection
from server.simulation_objects.trafficlights.i_traffic_light import ITrafficLight
from server.simulation_objects.trafficlights.traffic_light import TrafficLight


def create_map(x_border, y_border, path: str):
    roads, traffic_lights, junctions = __create_objects_from_data(path)
    __normalize_map(roads, traffic_lights, junctions, x_border, y_border)
    return roads, traffic_lights, junctions


def __create_objects_from_data(path: str):
    """
    order of operations:
    1. get and store all data about junction:
        which roads connect to each junction, roads/lanes movements, and traffic light for each lane (if exists)
    2. get all data about roads, and create all roads (with their lanes):
        enter all needed data for roads and lanes creation,
        and enter the data about traffic lights - just whether the lane should listen to a traffic light or not.
    this is because we have mututal aggregation between the traffic lights and the notified lanes.
    we chose the option of first creating notified lanes without the traffic light,
    and then create the traffic light that receives all its lanes in the constructor and updates them to have itself,
    which will be possible only once for each notified lane, and that keeps the simulation secure.
    the other option was creating empty traffic lights and inserting them to lanes by creation, but that could lead
    to troubles since the traffic ligths will all be the same object.
    3. create the traffic lights:
        for each group of lanes that should listen to the same traffic light, insert them as a list to the
        traffic light's constructor, which sets them to have the light as theirs.
    4. create the lane movements, based on the data from part 1, and now that all lanes have been created.
    5. create all junctions, they need the traffic lights and road section in their constructor.
    """
    # part 1
    from_roads, all_traffic_lights, junctions_data = __get_junctions_data(path)
    # part 2
    notified_lanes_dict: Dict[int, Set[int]] = __get_notified_lanes_dict(set(from_roads), all_traffic_lights)
    roads: Dict[int, IRoadSection] = __get_roads(notified_lanes_dict, path)
    # part 3
    traffic_lights = __get_traffic_lights(all_traffic_lights, roads)
    # part 4
    __set_lane_movements(roads, from_roads)
    # part 5
    all_junctions = __get_all_junctions(junctions_data, roads)
    roads_list = list(roads.values())
    return roads_list, traffic_lights, all_junctions


def __normalize_map(roads: List[IRoadSection], traffic_lights: List[ITrafficLight], junctions: List[IJunction],
                    x_border, y_border):
    """
    get min and max x,y values of the whole map and normalize all points accordingly
    :param x_border: max x value to convert to
    :param y_border: max y value to convert to
    """
    all_points: List[Point] = list()
    # get all points of the simulation
    for road in roads:
        all_points += [point for pair in road.coordinates for point in pair]
        for lane in road.lanes:
            all_points += [point for line in lane.coordinates for point in line]
    for light in traffic_lights:
        all_points.append(light.coordinate)
    for junc in junctions:
        all_points += junc.coordinates
    # get min and max x,y values of the whole map
    x_values = [p.x for p in all_points]
    y_values = [p.y for p in all_points]
    min_x = min(x_values)
    min_y = min(y_values)
    max_x = max(x_values)
    max_y = max(y_values)
    # create the normalization function:
    norm_x = lambda x: (x - min_x) * (x_border / (max_x - min_x))
    norm_y = lambda y: (y - min_y) * (y_border / (max_y - min_y))
    for point in all_points:
        point.normalize(norm_x, norm_y)


def __get_junctions_data(path: str):
    # from_roads: a dictionary from road id to a list of all road movements that are from the road.
    #   they are of form: (from: (road_id,lane_num), to: (road_id,lane_num)). all ints
    from_roads: Dict[int, List[Tuple[RoadLane, RoadLane]]] = defaultdict(list)
    # all_traffic_lights: a list of traffic lights, each one is represented as a list of (road_id,lane_num),
    #   which listen to the traffic light.
    all_traffic_lights: List[TrafficLightData] = list()
    # roads_movements: a list of (from: (road_id,lane_num), to: (road_id,lane_num)). all ints
    # traffic_lights: a list of lists of (road_id,lane_num), which are all ints.
    #   each sub list is a traffic light, and its list contains lanes listening to it.
    #   if the junction has no traffic lights, traffic_lights is an empty list.
    junctions_data: List[JunctionData] = list()
    for junction_data in get_db_junctions(path):
        junction_data: JunctionData
        # add to list of total data
        junctions_data.append(junction_data)
        # add the road movement
        for single_roads_movement in junction_data.goes_to:
            from_roads[single_roads_movement[0].road_id].append(single_roads_movement)
        # add the traffic lights. there are two lists: the RoadLane list of each traffic light,
        # and coordinates list of the traffic light. list should have the same length!
        if len(junction_data.traffic_lights) != len(junction_data.traffic_lights_coords):
            raise Exception("traffic lights lists are not the same length!")
        all_traffic_lights += [TrafficLightData(roadlane, coor) for roadlane, coor in
                               zip(junction_data.traffic_lights, junction_data.traffic_lights_coords)]
    return from_roads, all_traffic_lights, junctions_data


def __get_notified_lanes_dict(all_road_ids: Set[int], all_traffic_lights: List[TrafficLightData]) \
        -> Dict[int, Set[int]]:
    """
    create a dict from each road_id to the lanes that should be notified lanes
    :param all_road_ids: set of all read_id in the database
    :param all_traffic_lights: all traffic lights data
    :return: the dict
    """
    # for each road section that has any traffic light, create the set of lanes that have it
    notified_lanes_dict: Dict[int, Set[int]] = defaultdict(set)
    for traffic_light_data in all_traffic_lights:
        for pair in traffic_light_data.lanes:
            notified_lanes_dict[pair.road_id].add(pair.lane_num)
    # add all other roads that do not have any traffic lights, with an empty set
    for road_id in all_road_ids.difference(notified_lanes_dict.keys()):
        notified_lanes_dict[road_id] = set()
    return notified_lanes_dict


def __get_roads(notified_lanes_dict: Dict[int, Set[int]], path: str) -> Dict[int, IRoadSection]:
    roads: Dict[int, IRoadSection] = dict()
    # create all roads
    for road_data in get_db_road_sections(path):
        road_data: RoadData
        # create the road section
        roads[road_data.idnum] = RoadSection(road_data, notified_lanes_dict[road_data.idnum])
    # make sure there are no errors in the db
    if len(set(notified_lanes_dict).difference(set(roads))) != 0:
        raise Exception(f"there is data for movements but no for the roads:"
                        f"{set(notified_lanes_dict).difference(set(roads))}")
    return roads


def __get_traffic_lights(all_traffic_lights: List[TrafficLightData], roads: Dict[int, IRoadSection]) \
        -> List[ITrafficLight]:
    traffic_lights: List[ITrafficLight] = list()
    for tl_data in all_traffic_lights:
        # create a traffic light for the list, that controls the lanes in the list
        lanes_list = [roads[road_lane.road_id].get_lane(road_lane.lane_num) for road_lane in tl_data.lanes]
        # lanes_list should contain only notified lanes
        traffic_lights.append(TrafficLight(lanes_list, tl_data.coordinate))
    return traffic_lights


def __set_lane_movements(roads: Dict[int, IRoadSection], from_roads: Dict[int, List[Tuple[RoadLane, RoadLane]]]):
    for road_id, movements in from_roads.items():
        for movement in movements:
            from_lane = roads[road_id].get_lane(movement[0].lane_num)
            to_lane = roads[movement[1].road_id].get_lane(movement[1].lane_num)
            from_lane.add_movement_out(to_lane)
            to_lane.add_movement_in(from_lane)


def __get_all_junctions(junctions_data: List[JunctionData], roads: Dict[int, IRoadSection]) -> List[IJunction]:
    all_junctions: List[IJunction] = list()
    for junction_data in junctions_data:
        # get the in and out roads of the junction
        in_roads_ids = {movement[0].road_id for movement in junction_data.goes_to}
        out_roads_ids = {movement[1].road_id for movement in junction_data.goes_to}
        in_roads = [roads[road_id] for road_id in in_roads_ids]
        out_roads = [roads[road_id] for road_id in out_roads_ids]
        # get the the traffic lights of the junction: for each list of lanes (which represents a traffic light),
        # take the traffic light of the first item of the list (which is the traffic light of all of the lanes).
        # all lanes in the list are notified lanes
        first_lane_of_light = [roads[light_list[0].road_id].get_lane(light_list[0].lane_num) for light_list in
                               junction_data.traffic_lights]
        junction_lights = [lane.traffic_light for lane in first_lane_of_light]
        all_junctions.append(Junction(junction_data, in_roads, out_roads, junction_lights))
    return all_junctions
