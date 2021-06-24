from __future__ import annotations
from typing import List, Set
from dataclasses import dataclass


@dataclass(init=True)
class Connection:
    other: Node

    def __repr__(self):
        return str(self.other.node_id)


class Node:
    def __init__(self, node_id: int):
        self.node_id: int = node_id
        self.__connections: List[Connection] = list()

    def add_child(self, child: Node):
        self.__connections.append(Connection(child))

    def get_connections(self) -> List[Connection]:
        return self.__connections

    def get_connections_ids(self) -> Set[int]:
        return {c.other.node_id for c in self.__connections}

    def clear_connections(self):
        """
        empty connections list
        """
        self.__connections = list()

    def __eq__(self, other: Node):
        return self.node_id == other.node_id

    def __hash__(self):
        return hash(self.node_id)

    def __repr__(self):
        s = f"{self.node_id}, connections: [ "
        for con in self.__connections:
            s += f"({con.__repr__()}) "
        s += "]"
        return s
