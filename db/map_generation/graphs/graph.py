from __future__ import annotations

from typing import Dict, List, Tuple, Optional, Set, Union
from random import randint, sample, choice

from db.map_generation.graphs.junction_node import JuncNode, JuncIndices, JuncRoadConnection
from db.map_generation.graphs.node import Node
from server.geometry.point import Point


class Graph:
    def __init__(self, width, height):
        self.__nodes: Dict[int, Node] = dict()  # the graph
        self.__juncs: List[List[Optional[JuncNode]]] = list()
        self.__next_id: int = 0  # the next id to add
        self.width = width
        self.height = height

    def build_map(self, with_prints=False):
        self.__create_graph()
        if with_prints:
            print(self)
        self.__remove_connections()
        if with_prints:
            print(self)
        removed = self.__remove_01_connected_juncs()
        if with_prints:
            print("removed:", removed)
            print(self)
        roads = self.__dfs_roads_directions()
        if with_prints:
            print("roads:",*roads,sep="\n")


        # connected2 = self.__get_2_connected_juncs()
        # if with_prints:
        #     print("number of 2 connected:", len(connected2))
        # self.__test()

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

    def get_junc(self, indices: Union[JuncIndices, Tuple[int, int]]) -> JuncNode:
        """
        :param indices: indices in the 2d junc array
        :return: the JuncNode in those indices
        """
        if isinstance(indices, JuncIndices):
            return self.__juncs[indices.row][indices.col]
        return self.__juncs[indices[0]][indices[1]]

    def remove_node(self, node: Node):
        node.clear_connections()
        self.__nodes.pop(node.node_id, None)

    def remove_junction(self, junc: JuncNode):
        # remove inner nodes from graph
        for node in junc.all_nodes:
            self.remove_node(node)
        # remove junc from graph
        self.__juncs[junc.indices.row][junc.indices.col] = None

    def get_junc_from_node(self, node: Node) -> JuncNode:
        """
        :param node: input node of the graph
        :return: the junction that contains the node
        """
        junc_num = node.node_id // 4
        return self.get_junc((junc_num // self.width, junc_num % self.width))

    def get_connected_juncs(self, junc: JuncNode) -> List[JuncNode]:
        indices_set: Set[JuncIndices] = set()
        for node in junc.all_nodes:
            for connection in node.get_connections():
                other = connection.other
                indices_set.add(self.get_junc_from_node(other).indices)
        return [self.get_junc(indices) for indices in indices_set]

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

    # map building
    def __test(self):
        connections_counts = set()
        for row in self.__juncs:
            for junc in row:
                if junc is not None:
                    connections_counts.add(junc.connections_count())
                    if junc.connections_count() <= 1:
                        print(junc.indices)
                        raise Exception("bad juncs removal")
        if len(connections_counts.difference({2, 3, 4})) != 0:
            print(connections_counts)
            raise Exception("bad connections counts")

    def __create_graph(self):
        """
        create all nodes and connections
        """
        # create the nodes
        for h in range(self.height):
            row: List[JuncNode] = list()
            for w in range(self.width):
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
        # top left corner:
        self.add_connection(self.get_junc((0, 0)).right, self.get_junc((0, 1)).left)
        self.add_connection(self.get_junc((0, 0)).down, self.get_junc((1, 0)).up)
        # top row:
        for wi in range(1, self.width - 1):
            self.add_connection(self.get_junc((0, wi)).right, self.get_junc((0, wi + 1)).left)
            self.add_connection(self.get_junc((0, wi)).left, self.get_junc((0, wi - 1)).right)
            self.add_connection(self.get_junc((0, wi)).down, self.get_junc((1, wi)).up)
        # top right corner:
        self.add_connection(self.get_junc((0, -1)).left, self.get_junc((0, -2)).right)
        self.add_connection(self.get_junc((0, -1)).down, self.get_junc((1, -1)).up)
        # middle rows:
        for hi in range(1, self.height - 1):
            for wi in range(1, self.width - 1):
                self.add_connection(self.get_junc((hi, wi)).right, self.get_junc((hi, wi + 1)).left)
                self.add_connection(self.get_junc((hi, wi)).left, self.get_junc((hi, wi - 1)).right)
                self.add_connection(self.get_junc((hi, wi)).down, self.get_junc((hi + 1, wi)).up)
                self.add_connection(self.get_junc((hi, wi)).up, self.get_junc((hi - 1, wi)).down)
                # diagonal to up left
                if randint(0, 1) == 0:
                    self.add_connection(self.get_junc((hi, wi)).up, self.get_junc((hi - 1, wi - 1)).right)
                else:
                    self.add_connection(self.get_junc((hi, wi)).left, self.get_junc((hi - 1, wi - 1)).down)
                # diagonal to up right
                if randint(0, 1) == 0:
                    self.add_connection(self.get_junc((hi, wi)).up, self.get_junc((hi - 1, wi + 1)).left)
                else:
                    self.add_connection(self.get_junc((hi, wi)).right, self.get_junc((hi - 1, wi + 1)).down)
                # diagonal to down left
                if randint(0, 1) == 0:
                    self.add_connection(self.get_junc((hi, wi)).left, self.get_junc((hi + 1, wi - 1)).up)
                else:
                    self.add_connection(self.get_junc((hi, wi)).down, self.get_junc((hi + 1, wi - 1)).right)
                # diagonal to down right
                if randint(0, 1) == 0:
                    self.add_connection(self.get_junc((hi, wi)).right, self.get_junc((hi + 1, wi + 1)).up)
                else:
                    self.add_connection(self.get_junc((hi, wi)).down, self.get_junc((hi + 1, wi + 1)).left)
        # bottom left corner:
        self.add_connection(self.get_junc((-1, 0)).right, self.get_junc((-1, 1)).left)
        self.add_connection(self.get_junc((-1, 0)).up, self.get_junc((-2, 0)).down)
        # bottom row
        for wi in range(1, self.width - 1):
            self.add_connection(self.get_junc((-1, wi)).right, self.get_junc((-1, wi + 1)).left)
            self.add_connection(self.get_junc((-1, wi)).left, self.get_junc((-1, wi - 1)).right)
            self.add_connection(self.get_junc((-1, wi)).up, self.get_junc((-2, wi)).down)
        # bottom right corner:
        self.add_connection(self.get_junc((-1, -1)).left, self.get_junc((-1, -2)).right)
        self.add_connection(self.get_junc((-1, -1)).up, self.get_junc((-2, -1)).down)
        # diagonals remaining:
        if randint(0, 1) == 0:
            self.add_connection(self.get_junc((0, 1)).left, self.get_junc((1, 0)).up)
        else:
            self.add_connection(self.get_junc((0, 1)).down, self.get_junc((1, 0)).right)
        if randint(0, 1) == 0:
            self.add_connection(self.get_junc((0, -2)).right, self.get_junc((1, -1)).up)
        else:
            self.add_connection(self.get_junc((0, -2)).down, self.get_junc((1, -1)).left)
        if randint(0, 1) == 0:
            self.add_connection(self.get_junc((-1, 1)).left, self.get_junc((-2, 0)).down)
        else:
            self.add_connection(self.get_junc((-1, 1)).up, self.get_junc((-2, 0)).right)
        if randint(0, 1) == 0:
            self.add_connection(self.get_junc((-1, -2)).right, self.get_junc((-2, -1)).down)
        else:
            self.add_connection(self.get_junc((-1, -2)).up, self.get_junc((-2, -1)).left)

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

    def __get_2_connected_juncs(self) -> Set[JuncIndices]:
        """
        :return: a set of all (i,j) in the 2d juncs array where the junc has exactly 2 connections
        """
        result = set()
        for ri, row in enumerate(self.__juncs):
            for i, junc in enumerate(row):
                if junc is not None and junc.connections_count() == 2:
                    result.add(JuncIndices(ri, i))
        return result

    def __dfs_roads_directions(self) -> Set[JuncRoadConnection]:
        """
        perform DFS of the graph to set road direction for each junctions connection.
        :return: the road directions
        """

        roads: Set[JuncRoadConnection] = set()
        visited_indices: Set[JuncIndices] = set()

        def dfs_rec(junc: JuncNode):
            """
            recursively run from the input junction
            :param junc: the junction to run from
            """
            # add to visited
            visited_indices.add(junc.indices)
            # run on neighbors
            for neighbor in self.get_connected_juncs(junc):
                if neighbor.indices not in visited_indices:
                    roads.add(JuncRoadConnection(junc.indices, neighbor.indices))
                    dfs_rec(neighbor)

        def first_node(junc: JuncNode):
            """
            run specifically for a group-start junction
            :param junc: a junction that is the first in a connected group
            """
            # add to visited
            visited_indices.add(junc.indices)
            # choose a random road to be in-road
            neighbors = self.get_connected_juncs(junc)
            in_road_junc = choice(neighbors)
            roads.add(JuncRoadConnection(in_road_junc.indices, junc.indices))
            # run for the rest of the neighbors
            neighbors.remove(in_road_junc)
            for neighbor in neighbors:
                roads.add(JuncRoadConnection(junc.indices, neighbor.indices))
                dfs_rec(neighbor)

        all_juncs_indices: Set[JuncIndices] = {junc.indices for row in self.__juncs for junc in row if junc is not None}
        # the graph may not be connected, should run until all connected parts are visited
        while len(all_juncs_indices) != len(visited_indices):
            # now choose a junc and run on it.
            start_junc = self.get_junc(sample(all_juncs_indices.difference(visited_indices), 1)[0])
            first_node(start_junc)
        return roads
