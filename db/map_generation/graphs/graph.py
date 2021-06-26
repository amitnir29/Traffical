from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set, Union
from random import randint, sample, choice

from db.map_generation.graphs.junction_node import JuncNode, JuncIndices, JuncRoadSingleConnection, \
    JuncRoadChainConnection
from db.map_generation.graphs.node import Node, Connection
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
        self.__test([1, 2])
        single_roads = self.__dfs_roads_directions(with_prints)
        if with_prints:
            print("single roads:", *single_roads, sep="\n")
        self.__test([3], others={"single_roads": single_roads})
        connected2_count = len(self.__get_2_connected_juncs(single_roads))
        roads_chains, loop_removed = self.__create_chain_roads(single_roads, with_removed=True)
        if with_prints:
            print("roads chains:", *roads_chains, sep="\n")
            print(self)
        self.__test([4], others={"roads_chains": roads_chains, "prev_2_counts": connected2_count - loop_removed})

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

    def is_connection_diagonal(self, conn: Connection):
        j1 = self.get_junc_from_node(conn.me)
        j2 = self.get_junc_from_node(conn.other)
        # now check if they are diagonal: if they do not match both coordinates
        return JuncRoadSingleConnection(j1.indices, j2.indices).is_diagonal

    def is_conncetion_diagonals_crossing(self, conn: Connection):
        """
        return True if the connceetion is diagonal,
        and there is also a diagonal conncetion between the other 2 junctions in the 2x2 junctions square
        :param conn: the connection to check
        """
        if not self.is_connection_diagonal(conn):
            return False
        j1 = self.get_junc_from_node(conn.me)
        j2 = self.get_junc_from_node(conn.other)
        # check if top-left to bottom-right diagonal of top-right to bottom-left diagonal
        indices_diff = (j1.indices.row - j2.indices.row, j1.indices.col - j2.indices.col)
        if indices_diff[0] == indices_diff[1]:
            # top-left to bottom-right
            top_left = j1 if indices_diff[0] == -1 else j2  # else diff is 1
            top_right = self.get_junc((top_left.indices.row, top_left.indices.col + 1))
            bottom_left = self.get_junc((top_left.indices.row + 1, top_left.indices.col))
            return self.are_juncs_connected(top_right, bottom_left)
        else:
            # top-right to bottom-left
            top_right = j1 if indices_diff[0] == -1 else j2  # else diff is 1
            top_left = self.get_junc((top_right.indices.row, top_right.indices.col - 1))
            bottom_right = self.get_junc((top_right.indices.row + 1, top_right.indices.col))
            return self.are_juncs_connected(top_left, bottom_right)

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

    def are_juncs_connected(self, j1: JuncNode, j2: JuncNode) -> bool:
        """
        :return: True if there is a connection between any node of each of them
        """
        return j2 in self.get_connected_juncs(j1)

    def get_all_nodes(self) -> List[Node]:
        """
        :return: a list of all nodes in graph
        """
        return list(self.__nodes.values())

    def get_all_juncs(self) -> List[JuncNode]:
        """
        :return: a list of all not-None juncs
        """
        return [junc for row in self.__juncs for junc in row if junc is not None]

    def location_of_junc_indices(self, indices: JuncIndices) -> Point:
        """
        :param indices: indices of junc in 2d array of junctions.
        :return: location on the map of the junction indices
        """
        return Point(100 * indices.col, 100 * indices.row)

    def __len__(self):
        return len(self.__nodes)

    def __repr__(self):
        s = "Graph:\n"
        for ri, jnr in enumerate(self.__juncs):
            for i, jn in enumerate(jnr):
                s += f"({ri},{i}): {jn}\n"
        return s

    # map building
    def __test(self, test_levels: List[int], others: Dict = None):
        def test1():
            connections_counts = set()
            # test juncs removal
            for junc in self.get_all_juncs():
                connections_counts.add(junc.connections_count())
                if junc.connections_count() <= 1:
                    print(junc.indices)
                    raise Exception(f"bad juncs removal: {junc.indices}")
            # test number of connections for each junc
            if len(connections_counts.difference({2, 3, 4})) != 0:
                print(connections_counts)
                raise Exception(f"bad connections counts: {connections_counts}")

        def test2():
            # test no diagonals crossing
            for hi in range(self.height - 1):
                for wi in range(self.width - 1):
                    top_left = self.get_junc((hi, wi))
                    top_right = self.get_junc((hi, wi + 1))
                    bottom_left = self.get_junc((hi + 1, wi))
                    bottom_right = self.get_junc((hi + 1, wi + 1))
                    if top_left is None or top_right is None or bottom_left is None or bottom_right is None:
                        continue
                    if self.are_juncs_connected(top_left, bottom_right) \
                            and self.are_juncs_connected(top_right, bottom_left):
                        raise Exception(f"diagonals crossing: {top_left.indices},{bottom_right.indices}")

        def test3():
            if others is None or "single_roads" not in others:
                raise Exception("test3 must have single_roads in others dict")
            single_roads: Set[JuncRoadSingleConnection] = others["single_roads"]
            # test all connections have a road
            for node in self.get_all_nodes():
                for conn in node.get_connections():
                    source_junc = self.get_junc_from_node(conn.me)
                    target_junc = self.get_junc_from_node(conn.other)
                    if JuncRoadSingleConnection(source_junc.indices, target_junc.indices) not in single_roads \
                            and JuncRoadSingleConnection(target_junc.indices, source_junc.indices) not in single_roads:
                        raise Exception(f"connection has no road direction: {conn},"
                                        f" for juncs: {source_junc.indices}, {target_junc.indices}")
            for junc_road_conn in single_roads:
                if not self.are_juncs_connected(self.get_junc(junc_road_conn.source),
                                                self.get_junc(junc_road_conn.target)):
                    raise Exception(f"road exists but no connection: {junc_road_conn}")

        def test4():
            if others is None or "roads_chains" not in others:
                raise Exception("test4 must have roads_chains in others dict")
            roads_chains: List[JuncRoadChainConnection] = others["roads_chains"]
            if "prev_2_counts" not in others:
                raise Exception("test4 must have prev_2_counts in others dict")
            prev_2_counts: int = others["prev_2_counts"]
            all_left_singles: Set[JuncRoadSingleConnection] = {single for chain in roads_chains for single in
                                                               chain.parts}
            # test there are no more 2-connections juncs
            connected2 = self.__get_2_connected_juncs(all_left_singles)
            if len(connected2) != 0:
                raise Exception(f"juncs have 2 connections: {connected2}")
            # test all connections have a road
            for node in self.get_all_nodes():
                for conn in node.get_connections():
                    source_junc = self.get_junc_from_node(conn.me)
                    target_junc = self.get_junc_from_node(conn.other)
                    if JuncRoadSingleConnection(source_junc.indices, target_junc.indices) not in all_left_singles \
                            and JuncRoadSingleConnection(target_junc.indices,
                                                         source_junc.indices) not in all_left_singles:
                        raise Exception(f"connection has no road direction: {conn},"
                                        f" for juncs: {source_junc.indices}, {target_junc.indices}")
            # test all 2-connected are gone
            if prev_2_counts != sum([len(chain.parts) - 1 for chain in roads_chains if len(chain.parts) > 1]):
                raise Exception("no match between 2-connected juncs and juncs removed")

        tests = {
            1: test1, 2: test2, 3: test3, 4: test4
        }
        for test_level in test_levels:
            tests[test_level]()

    def __create_graph(self):
        """
        create all nodes and connections
        """
        # create the nodes
        for h in range(self.height):
            row: List[JuncNode] = list()
            for w in range(self.width):
                jnodes: List[Node] = [self.add_node() for _ in range(4)]
                jn = JuncNode(jnodes, (h, w))
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
            conncetions = curr_node.get_connections().copy()
            chosen_connection = choice(conncetions)
            # make sure that it is not a diagonal that crosses an established diagonal connection
            # between the other 2 nodes in the 2x2 juncs square
            no_choice = False
            while self.is_conncetion_diagonals_crossing(chosen_connection):
                conncetions.remove(chosen_connection)
                if len(conncetions) == 0:
                    # we have no connections left to choose from
                    no_choice = True
                    break
                chosen_connection = choice(conncetions)
            if no_choice:
                # if after cancelling the diagonals crossing conncetions we have no possible conncetions left
                continue
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
            for junc in self.get_all_juncs():
                if junc.connections_count() <= 1:
                    self.remove_junction(junc)
                    removed += 1
            if removed == 0:
                break
            total_removed += removed
        return total_removed

    def __dfs_roads_directions(self, with_prints=False) -> Set[JuncRoadSingleConnection]:
        """
        perform DFS of the graph to set road direction for each junctions connection.
        :return: the road directions
        """

        roads: Set[JuncRoadSingleConnection] = set()
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
                # go over unvisited juncs and add roads to them from current
                if neighbor.indices not in visited_indices:
                    if with_prints:
                        print(junc.indices, neighbor.indices)
                    roads.add(JuncRoadSingleConnection(junc.indices, neighbor.indices))
                    dfs_rec(neighbor)
                """
                there is a case where we are currently at junc 1, which has neighbors 2,3.
                from junc 1 wwe move to 2, that moves to 3 from it.
                3 will not go to 1 because 1 is visited, so the road 3->1 will not be created.
                when returning to 1, it will not go to 3, because 3 is visited, so the road 1->3 will not be created.
                so we result in a conncetion with no road, fix it:
                """
                if neighbor.indices in visited_indices \
                        and JuncRoadSingleConnection(junc.indices, neighbor.indices) not in roads \
                        and JuncRoadSingleConnection(neighbor.indices, junc.indices) not in roads:
                    roads.add(JuncRoadSingleConnection(junc.indices, neighbor.indices))
                    # do not call dfs recursivly

        def first_node(junc: JuncNode):
            """
            run specifically for a group-start junction
            :param junc: a junction that is the first in a connected group
            """
            # add to visited
            visited_indices.add(junc.indices)
            # choose a random road to be in-road
            neighbors = self.get_connected_juncs(junc).copy()
            in_road_junc = choice(neighbors)
            if with_prints:
                print("first in-road", in_road_junc.indices, junc.indices)
            roads.add(JuncRoadSingleConnection(in_road_junc.indices, junc.indices))
            # run for the rest of the neighbors
            neighbors.remove(in_road_junc)
            for neighbor in neighbors:
                if with_prints:
                    print("first", junc.indices, neighbor.indices)
                roads.add(JuncRoadSingleConnection(junc.indices, neighbor.indices))
                dfs_rec(neighbor)

        all_juncs_indices: Set[JuncIndices] = {junc.indices for junc in self.get_all_juncs()}
        # the graph may not be connected, should run until all connected parts are visited
        while len(all_juncs_indices) != len(visited_indices):
            # now choose a junc and run on it.
            start_junc = self.get_junc(sample(all_juncs_indices.difference(visited_indices), 1)[0])
            first_node(start_junc)
        return roads

    def __get_in_out_roads_dicts(self, roads: Set[JuncRoadSingleConnection]) \
            -> Tuple[Dict[JuncIndices, Set[JuncRoadSingleConnection]],
                     Dict[JuncIndices, Set[JuncRoadSingleConnection]]]:
        """
        :param roads: a set of all roads
        :return: in_roads dict and out_roads dict
        """
        # a dict of all roads that the key is their taget
        in_roads: Dict[JuncIndices, Set[JuncRoadSingleConnection]] = defaultdict(set)
        # a dict of all roads that the key is their source
        out_roads: Dict[JuncIndices, Set[JuncRoadSingleConnection]] = defaultdict(set)
        for road in roads:
            in_roads[road.target].add(road)
            out_roads[road.source].add(road)
        return in_roads, out_roads

    def __get_2_connected_juncs(self, roads: Set[JuncRoadSingleConnection], in_out_dicts=None) -> Set[JuncIndices]:
        """
        :param roads: all roads between juncs
        :param in_out_dicts: pre-calculated in_roads and out_roads dicts
        :return: a set of all (i,j) in the 2d juncs array where the junc has exactly
        one in-road connection and exactly one out-road connection.
        """
        # get number of in-roads and out-roads for each junction
        if in_out_dicts is None:
            in_roads, out_roads = self.__get_in_out_roads_dicts(roads)
        else:
            in_roads, out_roads = in_out_dicts
        return {junc.indices for junc in self.get_all_juncs()
                if len(in_roads[junc.indices]) == len(out_roads[junc.indices]) == 1}

    def __create_chain_roads(self, roads: Set[JuncRoadSingleConnection], with_removed=False) \
            -> Union[List[JuncRoadChainConnection], Tuple[List[JuncRoadChainConnection], int]]:
        """
        create chain connection in a way that handles 2-connected roads.
        a single conncetion that does not belong to a chain, is a chain of length 1.
        :param roads: all single connections between junctions
        :return: a list of the all chain conncetions if with_removed is False.
            else, a pair of the chain connections, and number of removed loop junctions
        """
        chain_connections: List[JuncRoadChainConnection] = list()
        handled: Set[JuncRoadSingleConnection] = set()
        in_roads, out_roads = self.__get_in_out_roads_dicts(roads)
        loop_removed = 0
        # now run over all roads
        connected2: Set[JuncIndices] = self.__get_2_connected_juncs(roads, (in_roads, out_roads))
        while len(handled) != len(roads):
            # init a chain road connection
            chain: List[JuncRoadSingleConnection] = list()
            # get a random road
            curr_road: JuncRoadSingleConnection = sample(roads.difference(handled), 1)[0]
            handled.add(curr_road)
            chain.append(curr_road)
            """
            now we have to be careful. there are 4 case:
            1. both sides of the road are not 2-connected juncs, just add the chain.
            2. the target is a 2-connected junc, loop forward until reaching a non 2-connected junc
            3. the source is a 2-connected junc, loop backwards until reaching a non 2-connected junc
            4. both sides of the road are 2-connected juncs, we should loop both forwars and backwards,
                but also notice that it is possible that we are in a loop of N juncs that are all 2-connected,
                in that case we should remove all of them. to check that we should have a set of visited juncs.
            """
            # case 1
            if curr_road.source not in connected2 and curr_road.target not in connected2:
                chain_connections.append(JuncRoadChainConnection(chain))
            # case 2
            elif curr_road.source not in connected2 and curr_road.target in connected2:
                while curr_road.target in connected2:
                    curr_road = list(out_roads[curr_road.target])[0]  # the length of the set is 1. get its element.
                    handled.add(curr_road)
                    chain.append(curr_road)
                # reached False, so we should not skip over the next target, we are done.
                chain_connections.append(JuncRoadChainConnection(chain))
                # remove the 2-connected junctions
                for road in chain[:-1]:
                    self.remove_junction(self.get_junc(road.target))
            # case 3
            elif curr_road.source in connected2 and curr_road.target not in connected2:
                while curr_road.source in connected2:
                    curr_road = list(in_roads[curr_road.source])[0]  # the length of the set is 1. get its element.
                    handled.add(curr_road)
                    chain.insert(0, curr_road)
                # reached False, so we should not skip over the next target, we are done.
                chain_connections.append(JuncRoadChainConnection(chain))
                # remove the 2-connected junctions
                for road in chain[:-1]:
                    self.remove_junction(self.get_junc(road.target))
            # case 4
            elif curr_road.source in connected2 and curr_road.target in connected2:
                """
                save the prev of the current road, to know if there is a loop.
                we dont save just the current road becuase this creates troubles in the while condition.
                """
                loop_start_road = list(in_roads[curr_road.source])[0]
                original_road = curr_road
                while curr_road.target in connected2 and curr_road != loop_start_road:
                    curr_road = list(out_roads[curr_road.target])[0]  # the length of the set is 1. get its element.
                    handled.add(curr_road)
                    chain.append(curr_road)
                # we finished going forwards, for 1 of 2 reasons:
                if loop_start_road != curr_road:
                    # regular operations. now go backwards:
                    curr_road = original_road
                    while curr_road.source in connected2:
                        curr_road = list(in_roads[curr_road.source])[0]  # the length of the set is 1. get its element.
                        handled.add(curr_road)
                        chain.insert(0, curr_road)
                    # in the end, add the chain
                    chain_connections.append(JuncRoadChainConnection(chain))
                    # remove the 2-connected junctions
                    for road in chain[:-1]:
                        self.remove_junction(self.get_junc(road.target))
                else:
                    """
                    we have a loop. handle the removing of all these junctions.
                    do the following:
                    1. find all junctions and roads that take part in the loop.
                    2. remove all of the roads from the roads set,
                        and also from the handled set to keep the while loop stop condition.
                    *. no need to remove them from them from in_roads/out_roads/connceted2 since they are
                        irrelevent to the other roads and junctions.
                    3. then, just apply the junc removing function on all junctions.
                    """
                    # step 1: we already have exactly them in the chain list!
                    # step 2:
                    for road in chain:
                        roads.remove(road)
                        handled.remove(road)
                    # step 3:
                    juncs_indices: List[JuncIndices] = [road.source for road in chain]
                    loop_removed += len(juncs_indices)
                    for junc_indices in juncs_indices:
                        self.remove_junction(self.get_junc(junc_indices))
            # just error checking
            else:
                raise Exception("error in if chain, in graph.__create_chain_roads")
        if with_removed:
            return chain_connections, loop_removed
        return chain_connections
