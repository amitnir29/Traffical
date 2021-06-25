from typing import Tuple, List
from dataclasses import dataclass

from db.map_generation.graphs.node import Node
from server.geometry.point import Point


@dataclass(init=True, eq=True, frozen=True, unsafe_hash=True, repr=True)
class JuncIndices:
    row: int
    col: int


@dataclass(init=True, eq=True, frozen=True, unsafe_hash=True, repr=True)
class JuncRoadConnection:
    source: JuncIndices
    target: JuncIndices


@dataclass
class JuncNode:
    location: Point
    up: Node
    down: Node
    right: Node
    left: Node
    all_nodes: Tuple[Node, Node, Node, Node]
    indices: JuncIndices

    def __init__(self, loc: Point, nodes: List[Node], indices: Tuple[int, int]):
        self.location = loc
        self.up = nodes[0]
        self.down = nodes[1]
        self.right = nodes[2]
        self.left = nodes[3]
        self.all_nodes = (self.up, self.down, self.right, self.left)
        self.indices = JuncIndices(indices[0], indices[1])

    def __repr__(self):
        return f"JuncNode: [up:{self.up}, down:{self.down}, right:{self.right}, left:{self.left}]"

    def connections_count(self):
        return sum(n.connections_count() for n in self.all_nodes)
