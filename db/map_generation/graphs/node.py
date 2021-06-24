from __future__ import annotations
from typing import List, Set
from dataclasses import dataclass


@dataclass(init=True)
class Connection:
    me: Node
    other: Node

    def __repr__(self):
        return f"({self.me.node_id}<->{self.other.node_id})"


class Node:
    def __init__(self, node_id: int):
        self.node_id: int = node_id
        self.__connections: List[Connection] = list()

    def add_child(self, child: Node):
        self.__connections.append(Connection(self, child))

    def get_connections(self) -> List[Connection]:
        return self.__connections

    def get_connections_ids(self) -> Set[int]:
        return {c.other.node_id for c in self.__connections}

    def remove_connection(self, conn: Connection):
        """
        remove a connection from the node
        :param conn: the connection to remove
        """
        self.__connections.remove(conn)
        # now from other:
        for others_conn in conn.other.get_connections():
            if others_conn.other.node_id == self.node_id:
                conn.other.__connections.remove(others_conn)
                break

    def keep_only_connection(self, conn_to_keep: Connection, apply_for_other=False):
        """
        remove all connection but the input one
        :param apply_for_other: do the same for the other node
        :param conn_to_keep: the only connection to keep
        """
        for conn in self.get_connections().copy():
            if conn.other.node_id != conn_to_keep.other.node_id:
                self.remove_connection(conn)
        if not apply_for_other:
            return
        other_node = conn_to_keep.other
        for other_conn in other_node.get_connections().copy():
            if other_conn.other.node_id != self.node_id:
                other_node.remove_connection(other_conn)

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
            s += f"{con.__repr__()} "
        s += "]"
        return s
