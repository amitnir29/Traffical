from typing import Tuple, List
from dataclasses import dataclass, field

from db.map_generation.graphs.node import Node
from server.geometry.point import Point


@dataclass
class JuncNode:
    location: Point
    up: Node
    down: Node
    right: Node
    left: Node
    all_nodes: Tuple[Node, Node, Node, Node]

    def __init__(self, loc: Point, nodes: List[Node]):
        self.location = loc
        self.up = nodes[0]
        self.down = nodes[1]
        self.right = nodes[2]
        self.left = nodes[3]
        self.all_nodes = (self.up, self.down, self.right, self.left)

    def __repr__(self):
        return f"JuncNode: [up:{self.up}, down:{self.down}, right:{self.right}, left:{self.left}]\n"

    def connections_count(self):
        return sum(len(n.get_connections()) for n in self.all_nodes)
