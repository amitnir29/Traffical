from typing import List, Tuple
import pandas as pd
import ast

from db.dataclasses.junction_data import JunctionData
from db.dataclasses.road_data import RoadData
from db.dataclasses.road_lane import RoadLane
from server.geometry.point import Point


def get_db_road_sections(path) -> List[RoadData]:
    df = pd.read_csv(path+"/RoadSections.csv")
    roads_data = []
    for index, row in df.iterrows():
        idnum: int = row["Id"]

        # coords parser
        coords = ast.literal_eval(row["Coordinates"].replace('{', '[').replace('}', ']'))
        coordinates: List[Tuple[Point, Point]] = []
        for i, _ in enumerate(coords):
            if i % 2:
                continue
            coordinates += [(Point(coords[i][0], coords[i][1]), Point(coords[i + 1][0], coords[i + 1][1]))]

        num_lanes: int = row['Number of lanes']
        max_speed: float = float(row['Max Speed'])

        road_data: RoadData = RoadData(idnum=idnum, coordinates=coordinates, num_lanes=num_lanes, max_speed=max_speed)

        roads_data += [road_data]

    return roads_data


def get_db_junctions(path):
    df = pd.read_csv(path+"/Junctions.csv")
    junctions_data: List[JunctionData] = []
    for index, row in df.iterrows():
        idnum: int = row['Id']

        # coords parser
        coordinates: List[Point] = []
        coords = ast.literal_eval(row["Coordinates"].replace('{', '[').replace('}', ']'))
        for i, _ in enumerate(coords):
            coordinates += [Point(coords[i][0], coords[i][1])]

        # goes to parser
        goes_to: List[Tuple[RoadLane, RoadLane]] = []
        goes_list = ast.literal_eval("[" + row["GoesTo"].replace('{', '[').replace('}', ']') + "]")
        for road_goes in goes_list:
            road_id = road_goes[0]
            for lane_index, lanes_to in enumerate(road_goes[1:]):
                if "(" not in str(lanes_to):
                    lanes_to = [lanes_to]
                else:
                    lanes_to = list(lanes_to)
                for lane_to in lanes_to:
                    road_to, lane_to = str(lane_to).split(sep='.')
                    road_to = int(road_to)
                    lane_to = int(lane_to)
                    goes_to += [(RoadLane(road_id=road_id, lane_num=lane_index),
                                 RoadLane(road_id=road_to, lane_num=lane_to))]

        # traffic lights parser
        traffic_lights_coords: List[Point] = []
        traffic_lights: List[List[RoadLane]] = []
        if ast.literal_eval(row["TrafficLights"].replace('{', '[').replace('}', ']')):
            traffic_lights_data = ast.literal_eval("[" + row["TrafficLights"].replace('{', '[').replace('}', ']') + "]")
            for traffic_light_data in traffic_lights_data:
                traffic_lights_coords += [Point(traffic_light_data[0][0], traffic_light_data[0][1])]
                lanes: List[RoadLane] = []
                if "(" not in str(traffic_light_data[1]):
                    lanes_traffic = [traffic_light_data[1]]
                else:
                    lanes_traffic = list(traffic_light_data[1])
                for lane in lanes_traffic:
                    r, ll = str(lane).split(sep='.')
                    r = int(r)
                    ll = int(ll)
                    lanes += [RoadLane(road_id=r, lane_num=ll)]
                traffic_lights += [lanes]

        num_traffic_lights: int = row["NumOfTrafficLights"]

        junction_data: JunctionData = JunctionData(idnum=idnum, coordinates=coordinates,
                                                   goes_to=goes_to, traffic_lights=traffic_lights,
                                                   traffic_lights_coords=traffic_lights_coords,
                                                   num_traffic_lights=num_traffic_lights)

        junctions_data += [junction_data]

    return junctions_data
