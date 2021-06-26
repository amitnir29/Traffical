from typing import Tuple, List
from dataclasses import dataclass

from db.map_generation.graphs.node import Node
from server.geometry.point import Point


@dataclass(init=True, eq=True, frozen=True, unsafe_hash=True, repr=True)
class JuncIndices:
    row: int
    col: int


@dataclass(init=True, eq=True, frozen=True, unsafe_hash=True, repr=True)
class JuncRoadSingleConnection:
    source: JuncIndices
    target: JuncIndices

    @property
    def is_diagonal(self):
        return self.source.row != self.target.row and self.source.col != self.target.col


@dataclass(init=True, repr=True)
class JuncRoadChainConnection:
    parts: List[JuncRoadSingleConnection]


class JuncNode:
    def __init__(self, nodes: List[Node], indices: Tuple[int, int]):
        self.up = nodes[0]
        self.down = nodes[1]
        self.right = nodes[2]
        self.left = nodes[3]
        self.all_nodes = (self.up, self.down, self.right, self.left)
        self.indices = JuncIndices(indices[0], indices[1])

    def __repr__(self):
        return f"JuncNode: [up:{self.up}, down:{self.down}, right:{self.right}, left:{self.left}]"

    def __eq__(self, other):
        return self.indices == other.indices

    def connections_count(self):
        return sum(n.connections_count() for n in self.all_nodes)
