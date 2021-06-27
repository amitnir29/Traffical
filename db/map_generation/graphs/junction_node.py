from typing import Tuple, List
from dataclasses import dataclass
from enum import Enum

from db.dataclasses.road_lane import RoadLane
from db.map_generation.graphs.node import Node
from server.geometry.point import Point


@dataclass(init=True, eq=True, frozen=True, unsafe_hash=True)
class JuncIndices:
    row: int
    col: int

    def __repr__(self):
        return f"({self.row},{self.col})"


class JuncConnDirection(Enum):
    UP = "u"
    DOWN = "d"
    RIGHT = "r"
    LEFT = "l"
    UNKNOWN = "x"


@dataclass(init=True, repr=True, frozen=True)
class JuncRoadSingleConnection:
    source: JuncIndices
    target: JuncIndices
    source_dir: JuncConnDirection = JuncConnDirection.UNKNOWN
    target_dir: JuncConnDirection = JuncConnDirection.UNKNOWN

    @property
    def is_diagonal(self):
        return self.source.row != self.target.row and self.source.col != self.target.col

    def __eq__(self, other):
        return self.source == other.source and self.target == other.target

    def __hash__(self):
        return (self.source, self.target).__hash__()


class JuncRoadChainConnection:
    def __init__(self, road_id: int, parts: List[JuncRoadSingleConnection]):
        self.road_id: int = road_id
        self.parts: List[JuncRoadSingleConnection] = parts
        self.lanes_num: int = None
        self.lanes: List[RoadLane] = None
        self.first_junc: JuncIndices = parts[0].source
        self.last_junc: JuncIndices = parts[-1].target

    def set_lanes(self, lanes_num: int):
        self.lanes_num = lanes_num
        self.lanes = [RoadLane(self.road_id, i) for i in range(lanes_num)]

    def __repr__(self):
        return f"JuncRoadChainConnection, id:{self.road_id}, parts:{self.parts}, " \
               f"lanes_num:{self.lanes_num}, lanes:{self.lanes}"


class JuncNode:
    def __init__(self, nodes: List[Node], indices: Tuple[int, int]):
        self.up = nodes[0]
        self.down = nodes[1]
        self.right = nodes[2]
        self.left = nodes[3]
        self.all_nodes = (self.up, self.down, self.right, self.left)
        self.indices = JuncIndices(indices[0], indices[1])

    def __repr__(self):
        return f"JuncNode {self.indices}: [up:{self.up}, down:{self.down}, right:{self.right}, left:{self.left}]"

    def __eq__(self, other):
        return self.indices == other.indices

    def connections_count(self):
        return sum(n.connections_count() for n in self.all_nodes)

    def side_of_node(self, node: Node):
        if self.up == node:
            return JuncConnDirection.UP
        elif self.down == node:
            return JuncConnDirection.DOWN
        elif self.right == node:
            return JuncConnDirection.RIGHT
        elif self.left == node:
            return JuncConnDirection.LEFT
        raise Exception("node not in this junction")
