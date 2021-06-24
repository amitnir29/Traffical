from __future__ import annotations

from typing import Dict, List, Tuple, Optional
from random import randint, sample, choice

from db.map_generation.graphs.junction_node import JuncNode
from db.map_generation.graphs.node import Node
from server.geometry.point import Point


class Graph:
    def __init__(self, width, height, with_prints=False):
        self.__nodes: Dict[int, Node] = dict()  # the graph
        self.__juncs: List[List[Optional[JuncNode]]] = list()
        self.__next_id: int = 0  # the next id to add
        self.sizes = {"w": width, "h": height}
        self.__create_graph(width, height)
        if with_prints:
            print(self)
        self.__remove_connections()
        if with_prints:
            print(self)
        removed = self.__remove_01_connected_juncs()
        if with_prints:
            print("removed:", removed)
            print(self)
        self.test()

    def test(self):
        for row in self.__juncs:
            for junc in row:
                if junc is not None:
                    if junc.connections_count() <= 1:
                        print(junc.indices)
                        raise Exception("bad")

    def __create_graph(self, width, height):
        """
        create all nodes and connections
        :param width: number of nodes in each row
        :param height: number of nodes in each column
        """
        # create the nodes
        for h in range(height):
            row: List[JuncNode] = list()
            for w in range(width):
                jnodes: List[Node] = [self.add_node() for _ in range(4)]
                jn = JuncNode(Point(100 * w, 100 * h), jnodes, (h, w))
                row.append(jn)
            self.__juncs.append(row)
        # create all connections
        self.__create_connections()

    def __create_connections(self):
        """
        create all connections between nodes
        """
        ws, hs = self.sizes["w"], self.sizes["h"]
        # top left corner:
        self.add_connection(self.__juncs[0][0].right, self.__juncs[0][1].left)
        self.add_connection(self.__juncs[0][0].down, self.__juncs[1][0].up)
        # top row:
        for wi in range(1, ws - 1):
            self.add_connection(self.__juncs[0][wi].right, self.__juncs[0][wi + 1].left)
            self.add_connection(self.__juncs[0][wi].left, self.__juncs[0][wi - 1].right)
            self.add_connection(self.__juncs[0][wi].down, self.__juncs[1][wi].up)
        # top right corner:
        self.add_connection(self.__juncs[0][-1].left, self.__juncs[0][-2].right)
        self.add_connection(self.__juncs[0][-1].down, self.__juncs[1][-1].up)
        # middle rows:
        for hi in range(1, hs - 1):
            for wi in range(1, ws - 1):
                self.add_connection(self.__juncs[hi][wi].right, self.__juncs[hi][wi + 1].left)
                self.add_connection(self.__juncs[hi][wi].left, self.__juncs[hi][wi - 1].right)
                self.add_connection(self.__juncs[hi][wi].down, self.__juncs[hi + 1][wi].up)
                self.add_connection(self.__juncs[hi][wi].up, self.__juncs[hi - 1][wi].down)
                # diagonal to up left
                if randint(0, 1) == 0:
                    self.add_connection(self.__juncs[hi][wi].up, self.__juncs[hi - 1][wi - 1].right)
                else:
                    self.add_connection(self.__juncs[hi][wi].left, self.__juncs[hi - 1][wi - 1].down)
                # diagonal to up right
                if randint(0, 1) == 0:
                    self.add_connection(self.__juncs[hi][wi].up, self.__juncs[hi - 1][wi + 1].left)
                else:
                    self.add_connection(self.__juncs[hi][wi].right, self.__juncs[hi - 1][wi + 1].down)
                # diagonal to down left
                if randint(0, 1) == 0:
                    self.add_connection(self.__juncs[hi][wi].left, self.__juncs[hi + 1][wi - 1].up)
                else:
                    self.add_connection(self.__juncs[hi][wi].down, self.__juncs[hi + 1][wi - 1].right)
                # diagonal to down right
                if randint(0, 1) == 0:
                    self.add_connection(self.__juncs[hi][wi].right, self.__juncs[hi + 1][wi + 1].up)
                else:
                    self.add_connection(self.__juncs[hi][wi].down, self.__juncs[hi + 1][wi + 1].left)
        # bottom left corner:
        self.add_connection(self.__juncs[-1][0].right, self.__juncs[-1][1].left)
        self.add_connection(self.__juncs[-1][0].up, self.__juncs[-2][0].down)
        # bottom row
        for wi in range(1, ws - 1):
            self.add_connection(self.__juncs[-1][wi].right, self.__juncs[-1][wi + 1].left)
            self.add_connection(self.__juncs[-1][wi].left, self.__juncs[-1][wi - 1].right)
            self.add_connection(self.__juncs[-1][wi].up, self.__juncs[-2][wi].down)
        # bottom right corner:
        self.add_connection(self.__juncs[-1][-1].left, self.__juncs[-1][-2].right)
        self.add_connection(self.__juncs[-1][-1].up, self.__juncs[-2][-1].down)
        # diagonals remaining:
        if randint(0, 1) == 0:
            self.add_connection(self.__juncs[0][1].left, self.__juncs[1][0].up)
        else:
            self.add_connection(self.__juncs[0][1].down, self.__juncs[1][0].right)
        if randint(0, 1) == 0:
            self.add_connection(self.__juncs[0][-2].right, self.__juncs[1][-1].up)
        else:
            self.add_connection(self.__juncs[0][-2].down, self.__juncs[1][-1].left)
        if randint(0, 1) == 0:
            self.add_connection(self.__juncs[-1][1].left, self.__juncs[-2][0].down)
        else:
            self.add_connection(self.__juncs[-1][1].up, self.__juncs[-2][0].right)
        if randint(0, 1) == 0:
            self.add_connection(self.__juncs[-1][-2].right, self.__juncs[-2][-1].down)
        else:
            self.add_connection(self.__juncs[-1][-2].up, self.__juncs[-2][-1].left)

    def __remove_connections(self):
        nodes_left = {i for i in range(len(self.get_all_nodes()))}
        while len(nodes_left) != 0:
            curr_node_id = sample(nodes_left, 1)[0]
            nodes_left.remove(curr_node_id)
            curr_node = self.get_node(curr_node_id)
            if curr_node.connections_count() <= 1:
                # 0 with no connection to begin with,
                # 1 if already been taken care of through another node
                continue
            chosen_connection = choice(curr_node.get_connections())
            # now we should set this to be the only connection of this node
            curr_node.keep_only_connection(chosen_connection, apply_for_other=True)

    def __remove_01_connected_juncs(self) -> int:
        """
        remove all junctions that have 0/1 connections to all other junctions.
        notice that in case that removing a junction results in another junction with 0/1 connections,
        we should remove it too
        :return: number of junctions removed
        """
        total_removed = 0
        while True:
            removed = 0
            for row in self.__juncs:
                for junc in row:
                    if junc is not None and junc.connections_count() <= 1:
                        self.remove_junction(junc)
                        removed += 1
            if removed == 0:
                break
            total_removed += removed
        return total_removed

    def add_node(self) -> Node:
        """
        create a new node, add it to the dict with the current id, increment the id, and return the new nod
        :return: the new node
        """
        new_node = Node(self.__next_id)
        self.__nodes[self.__next_id] = new_node
        self.__next_id += 1
        return new_node

    def get_node(self, node_id: int) -> Node:
        """
        :param node_id: id of a wanted node
        :return: the node with the input id
        """
        return self.__nodes[node_id]

    def remove_node(self, node: Node):
        node.clear_connections()
        self.__nodes.pop(node.node_id, None)

    def remove_junction(self, junc: JuncNode):
        # remove inner nodes from graph
        for node in junc.all_nodes:
            self.remove_node(node)
        # remove junc from graph
        hi, wi = junc.indices
        self.__juncs[hi][wi] = None

    def add_connection(self, n1: Node, n2: Node):
        """
        add a connection between n1 and n2
        :param n1: source id
        :param n2: target id
        """
        if n2.node_id in n1.get_connections_ids() or n1.node_id in n2.get_connections_ids():
            return
        n1.add_child(n2)
        n2.add_child(n1)

    def get_all_nodes(self) -> List[Node]:
        """
        :return: a list of all nodes in graph
        """
        return list(self.__nodes.values())

    def __len__(self):
        return len(self.__nodes)

    def __repr__(self):
        s = "Graph:\n"
        for ri, jnr in enumerate(self.__juncs):
            for i, jn in enumerate(jnr):
                s += f"({ri},{i}): {jn}\n"
        return s
