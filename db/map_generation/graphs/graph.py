from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set, Union
from random import randint, sample, choice

from db.dataclasses.road_lane import RoadLane
from db.map_generation.graphs.junction_node import JuncNode, JuncIndices, JuncRoadSingleConnection, \
    JuncRoadChainConnection, JuncConnDirection
from db.map_generation.graphs.node import Node, Connection
from server.geometry.point import Point


class Graph:
    def __init__(self, width, height):
        self.__nodes: Dict[int, Node] = dict()  # the graph
        self.__juncs: List[List[Optional[JuncNode]]] = list()
        self.__next_id: int = 0  # the next id to add
        self.width = width
        self.height = height

    def build_map(self, with_tests=True, with_prints=False):
        # steps 1,2
        self.__create_graph()
        if with_prints:
            print("initial:", self)
        # step 3
        self.__remove_connections()
        if with_prints:
            print("after connections removal:", self)
        # step 4
        removed = self.__remove_01_connected_juncs()
        if with_prints:
            print("after 0/1 connected removed:", self)
            print("count removed:", removed)
        if with_tests:
            self.__test(1)
        # step 5
        single_roads = self.__dfs_roads_directions(with_prints)
        if with_prints:
            print("single roads:", *single_roads, sep="\n")
        if with_tests:
            self.__test(2, others={"single_roads": single_roads})
        connected2_count = len(self.__get_2_connected_juncs(single_roads))
        # step 6
        roads_chains, loop_removed = self.__create_chain_roads(single_roads, with_removed=True)
        if with_prints:
            print("roads chains:", *roads_chains, sep="\n")
            print("after roads chains calc:", self)
        if with_tests:
            self.__test(3, others={"roads_chains": roads_chains, "prev_2_counts": connected2_count - loop_removed})
        # step 7
        self.__set_roads_lanes(roads_chains)
        if with_tests:
            self.__test(4, others={"roads_chains": roads_chains})
        # step 8
        juncs_movements = self.__set_junction_movement(roads_chains)
        if with_tests:
            self.__test(5, others={"roads_chains": roads_chains, "juncs_moves": juncs_movements})
        if with_prints:
            print(juncs_movements)

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

    def handle_diagonals_crossing_connections(self, conn: Connection):
        """
        check if the connection is diagonal and if there is also a diagonal connection between the other 2 junctions
        in the 2x2 square of junctions, which cross each other. in that case, remove the other connection.
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
            if self.are_juncs_connected(top_right, bottom_left):
                # print(conn, top_right, bottom_left, sep="\n")
                # we should remove the connection.
                if bottom_left.right.node_id in top_right.down.get_connections_ids():
                    top_right.down.remove_connection_by_id(bottom_left.right.node_id)
                if bottom_left.up.node_id in top_right.left.get_connections_ids():
                    top_right.left.remove_connection_by_id(bottom_left.up.node_id)
        else:
            # top-right to bottom-left
            top_right = j1 if indices_diff[0] == -1 else j2  # else diff is 1
            top_left = self.get_junc((top_right.indices.row, top_right.indices.col - 1))
            bottom_right = self.get_junc((top_right.indices.row + 1, top_right.indices.col))
            if self.are_juncs_connected(top_left, bottom_right):
                # print(conn, top_left, bottom_right, sep="\n")
                # we should remove the connection.
                if bottom_right.left.node_id in top_left.down.get_connections_ids():
                    top_left.down.remove_connection_by_id(bottom_right.left.node_id)
                if bottom_right.up.node_id in top_left.right.get_connections_ids():
                    top_left.right.remove_connection_by_id(bottom_right.up.node_id)

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
                other_junc_indices = self.get_junc_from_node(other).indices
                if other_junc_indices in indices_set:
                    raise Exception(f"junc {junc.indices} is connected more than once to junc {other_junc_indices}\n"
                                    f"{junc}\n{self.get_junc_from_node(other)}\n")
                indices_set.add(other_junc_indices)
        return [self.get_junc(indices) for indices in indices_set]

    def are_juncs_connected(self, j1: JuncNode, j2: JuncNode) -> bool:
        """
        :return: True if there is a connection between any node of each of them
        """
        return j2 in self.get_connected_juncs(j1)

    def get_connection_directions(self, source: JuncNode, target: JuncNode) \
            -> Tuple[JuncConnDirection, JuncConnDirection]:
        """
        source and target should be connected. find the connections sides
        :param source: first junc
        :param target: second junc
        :return: a pair of (source conn side, target conn side)
        """
        for node in source.all_nodes:
            for conn in node.get_connections():
                other_node = conn.other
                other_junc = self.get_junc_from_node(other_node)
                if other_junc == target:
                    return source.side_of_node(node), target.side_of_node(other_node)
        raise Exception(f"these juncs are not connected.\n{source}\n{target}")

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
                s += f"{jn}\n"
        return s

    # map building
    def __test(self, test_level: int, others: Dict = None):
        # after step 4.
        # test juncs removal, test number of connections for each junc,
        # test no 2 nodes have more than 1 connection, test no diagonals crossing
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
            # test no 2 nodes have more than 1 connection
            for node in self.get_all_nodes():
                if len(node.get_connections_ids()) != len(node.get_connections()):
                    raise Exception(f"node has 2 connection with another node\n {node}")
            # test no 2 juncs have more than 1 connection
            for junc in self.get_all_juncs():
                if junc.connections_count() != len(self.get_connected_juncs(junc)):
                    raise Exception(f"junc has 2 connection with another junc\n {junc}")
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
                        raise Exception(
                            f"diagonals crossing: {top_left.indices},{bottom_right.indices}\n {self}")

        # after step 5.
        # test all connections have a road, test all roads have directions set, test no two roads of opposite directions
        def test2():
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
            # test all roads have directions set
            for road in single_roads:
                if road.source_dir == JuncConnDirection.UNKNOWN or road.target_dir == JuncConnDirection.UNKNOWN:
                    raise Exception("test3 road has no connection directions set")
            # test no two roads of opposite directions
            for road in single_roads:
                if JuncRoadSingleConnection(road.target, road.source) in single_roads:
                    raise Exception(f"test3 roads of opposite direction exist\n\n"
                                    f"{road}\n\n{single_roads}\n\n{self}")

        # after step 6.
        # test all road chains have a unique id, test there are no more 2-connections juncs,
        # test all connections have a road,test all 2-connected are gone
        def test3():
            if others is None or "roads_chains" not in others:
                raise Exception("test4 must have roads_chains in others dict")
            roads_chains: List[JuncRoadChainConnection] = others["roads_chains"]
            if len(roads_chains) != len({r.road_id for r in roads_chains}):
                raise Exception("test4 roads dont have a unique id")
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

        # after step 7.
        # test if all road chains have a lanes number
        def test4():
            if others is None or "roads_chains" not in others:
                raise Exception("test5 must have roads_chains in others dict")
            roads_chains: List[JuncRoadChainConnection] = others["roads_chains"]
            for chain in roads_chains:
                if chain.lanes_num is None:
                    raise Exception(f"test5 road_chain has no lanes_count\n {chain}")

        # after step 8.
        # test if all roads have the correct number of lanes, test lanes mapping order,
        # test no lane number higher than max lane number for road
        def test5():
            if others is None or "roads_chains" not in others:
                raise Exception("test6 must have roads_chains in others dict")
            roads_chains: List[JuncRoadChainConnection] = others["roads_chains"]
            roads_chains_dict: Dict[int, JuncRoadChainConnection] = {r.road_id: r for r in roads_chains}
            if others is None or "juncs_moves" not in others:
                raise Exception("test6 must have juncs_moves in others dict")
            juncs_moves: Dict[JuncIndices, List[Tuple[RoadLane, RoadLane]]] = others["juncs_moves"]
            # test if all roads have the correct number of lanes
            for junc_indices, moves in juncs_moves.items():
                roads_moves: Dict[int, List[int]] = defaultdict(list)
                for move in moves:
                    roads_moves[move[0].road_id].append(move[1].road_id)
                for in_road in roads_moves:
                    if len(roads_moves[in_road]) != roads_chains_dict[in_road].lanes_num:
                        raise Exception(f"road movements do not match the number of lanes\n\n"
                                        f"{roads_chains_dict[in_road]}\n\n{junc_indices},moves:\n{moves}\n\n"
                                        f"{self}\n\n{roads_chains}")
            # test lanes mapping order
            order: List[JuncConnDirection] \
                = [JuncConnDirection.UP, JuncConnDirection.RIGHT, JuncConnDirection.DOWN, JuncConnDirection.LEFT]
            for junc_indices, moves in juncs_moves.items():
                # value tuple is (source lane num,target road num)
                roads_moves: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
                for move in moves:
                    roads_moves[move[0].road_id].append((move[0].lane_num, move[1].road_id))
                for in_road in roads_moves:
                    if len(roads_moves[in_road]) == 1:
                        continue
                    in_road_dir_index = order.index(roads_chains_dict[in_road].parts[-1].target_dir)
                    for i, first_move in enumerate(roads_moves[in_road]):
                        first_road_dir_index = order.index(roads_chains_dict[first_move[1]].parts[0].source_dir)
                        for j, second_move in enumerate(roads_moves[in_road][i + 1:]):
                            second_road_dir_index = order.index(roads_chains_dict[second_move[1]].parts[0].source_dir)
                            # if source lane if second > source lane of first
                            # and target road of second is more left than target road of first
                            if second_move[0] > first_move[0] and (4 + first_road_dir_index - in_road_dir_index) % 4 > \
                                    (4 + second_road_dir_index - in_road_dir_index) % 4:
                                raise Exception(f"wrong order of lanes\n{first_move},{second_move}\n"
                                                f"in:{roads_chains[in_road]}\nfirst:{roads_chains[first_move[1]]}\n"
                                                f"second:{roads_chains[second_move[1]]}\n")
            # test no lane number higher than max lane number for road
            all_road_lanes: Set[RoadLane] = {rl for l in juncs_moves.values() for pair in l for rl in pair}
            all_lanes_for_road: Dict[int, List[int]] = defaultdict(list)
            for rl in all_road_lanes:
                all_lanes_for_road[rl.road_id].append(rl.lane_num)
            for r_id in all_lanes_for_road:
                max_lane_for_r = max(all_lanes_for_road[r_id])
                if max_lane_for_r > roads_chains_dict[r_id].lanes_num - 1:
                    raise Exception(f"too many lanes in juncs_moves: {max_lane_for_r} "
                                    f"vs {roads_chains_dict[r_id].lanes_num - 1}\n{roads_chains_dict[r_id]}")

        tests = {
            1: test1, 2: test2, 3: test3, 4: test4, 5: test5
        }
        tests[test_level]()

    #step 1
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

    #step 2
    def __create_connections(self):
        """
        create all connections between nodes.
        """
        """
        When adding diagonals, each node adds only diagonals to nodes below it.
        This prevents a case where two nodes add diagonals with each other, s.t. both diagonals are added.
        """
        # top left corner:
        self.add_connection(self.get_junc((0, 0)).right, self.get_junc((0, 1)).left)
        self.add_connection(self.get_junc((0, 0)).down, self.get_junc((1, 0)).up)
        # diagonal to down right
        if randint(0, 1) == 0:
            self.add_connection(self.get_junc((0, 0)).right, self.get_junc((1, 1)).up)
        else:
            self.add_connection(self.get_junc((0, 0)).down, self.get_junc((1, 1)).left)
        # top row:
        for wi in range(1, self.width - 1):
            self.add_connection(self.get_junc((0, wi)).right, self.get_junc((0, wi + 1)).left)
            self.add_connection(self.get_junc((0, wi)).left, self.get_junc((0, wi - 1)).right)
            self.add_connection(self.get_junc((0, wi)).down, self.get_junc((1, wi)).up)
            # diagonal to down left
            if randint(0, 1) == 0:
                self.add_connection(self.get_junc((0, wi)).left, self.get_junc((1, wi - 1)).up)
            else:
                self.add_connection(self.get_junc((0, wi)).down, self.get_junc((1, wi - 1)).right)
            # diagonal to down right
            if randint(0, 1) == 0:
                self.add_connection(self.get_junc((0, wi)).right, self.get_junc((1, wi + 1)).up)
            else:
                self.add_connection(self.get_junc((0, wi)).down, self.get_junc((1, wi + 1)).left)
        # top right corner:
        self.add_connection(self.get_junc((0, -1)).left, self.get_junc((0, -2)).right)
        self.add_connection(self.get_junc((0, -1)).down, self.get_junc((1, -1)).up)
        # diagonal to down left
        if randint(0, 1) == 0:
            self.add_connection(self.get_junc((0, -1)).left, self.get_junc((1, -2)).up)
        else:
            self.add_connection(self.get_junc((0, -1)).down, self.get_junc((1, -2)).right)
        # middle rows:
        for hi in range(1, self.height - 1):
            # left node
            self.add_connection(self.get_junc((hi, 0)).right, self.get_junc((hi, 1)).left)
            self.add_connection(self.get_junc((hi, 0)).down, self.get_junc((hi + 1, 0)).up)
            self.add_connection(self.get_junc((hi, 0)).up, self.get_junc((hi - 1, 0)).down)
            # diagonal to down right
            if randint(0, 1) == 0:
                self.add_connection(self.get_junc((hi, 0)).right, self.get_junc((hi + 1, 1)).up)
            else:
                self.add_connection(self.get_junc((hi, 0)).down, self.get_junc((hi + 1, 1)).left)
            # middle nodes
            for wi in range(1, self.width - 1):
                self.add_connection(self.get_junc((hi, wi)).right, self.get_junc((hi, wi + 1)).left)
                self.add_connection(self.get_junc((hi, wi)).left, self.get_junc((hi, wi - 1)).right)
                self.add_connection(self.get_junc((hi, wi)).down, self.get_junc((hi + 1, wi)).up)
                self.add_connection(self.get_junc((hi, wi)).up, self.get_junc((hi - 1, wi)).down)
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
            # right node:
            self.add_connection(self.get_junc((hi, -1)).left, self.get_junc((hi, -2)).right)
            self.add_connection(self.get_junc((hi, -1)).down, self.get_junc((hi + 1, -1)).up)
            self.add_connection(self.get_junc((hi, -1)).up, self.get_junc((hi - 1, -1)).down)
            # diagonal to down left
            if randint(0, 1) == 0:
                self.add_connection(self.get_junc((hi, -1)).left, self.get_junc((hi + 1, -2)).up)
            else:
                self.add_connection(self.get_junc((hi, -1)).down, self.get_junc((hi + 1, -2)).right)
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

    #step 3
    def __remove_connections(self):
        nodes_left = set(self.__nodes.keys()).copy()
        while len(nodes_left) != 0:
            curr_node_id = sample(nodes_left, 1)[0]
            nodes_left.remove(curr_node_id)
            curr_node = self.get_node(curr_node_id)
            if curr_node.connections_count() <= 1:
                # 0 with no connection to begin with,
                # 1 if already been taken care of through another node
                continue
            connections = curr_node.get_connections().copy()
            chosen_connection = choice(connections)
            # if it is a diagonal connection that crosses another diagonal connection of the other 2 juncs
            # in the 2x2 square of juncs, cancel the other diagonal connection.
            # the call will change anything only if chosen_connection is diagonal and crosses the other diagonal.
            self.handle_diagonals_crossing_connections(chosen_connection)
            # now we should set this to be the only connection of this node
            curr_node.keep_only_connection(chosen_connection, apply_for_other=True)

    #step 4
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

    #step 5
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
                    directions = self.get_connection_directions(junc, neighbor)
                    roads.add(JuncRoadSingleConnection(junc.indices, neighbor.indices, directions[0], directions[1]))
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
                    if with_prints:
                        print(junc.indices, neighbor.indices)
                    directions = self.get_connection_directions(junc, neighbor)
                    roads.add(JuncRoadSingleConnection(junc.indices, neighbor.indices, directions[0], directions[1]))
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
            directions = self.get_connection_directions(in_road_junc, junc)
            roads.add(JuncRoadSingleConnection(in_road_junc.indices, junc.indices, directions[0], directions[1]))
            # run for the rest of the neighbors
            neighbors.remove(in_road_junc)
            for neighbor in neighbors:
                if with_prints:
                    print("first", junc.indices, neighbor.indices)
                directions = self.get_connection_directions(junc, neighbor)
                roads.add(JuncRoadSingleConnection(junc.indices, neighbor.indices, directions[0], directions[1]))
                dfs_rec(neighbor)

        all_juncs_indices: Set[JuncIndices] = {junc.indices for junc in self.get_all_juncs()}
        # the graph may not be connected, should run until all connected parts are visited
        while len(all_juncs_indices) != len(visited_indices):
            # now choose a junc and run on it.
            start_junc = self.get_junc(sample(all_juncs_indices.difference(visited_indices), 1)[0])
            first_node(start_junc)
        return roads

    #step 6
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
        in_roads, out_roads = self.__get_in_out_roads_dicts_by_single(roads)
        loop_removed = 0
        # the id of chain, will be the id of the future road
        curr_chain_id = 0
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
                chain_connections.append(JuncRoadChainConnection(curr_chain_id, chain))
                curr_chain_id += 1
            # case 2
            elif curr_road.source not in connected2 and curr_road.target in connected2:
                while curr_road.target in connected2:
                    curr_road = list(out_roads[curr_road.target])[0]  # the length of the set is 1. get its element.
                    handled.add(curr_road)
                    chain.append(curr_road)
                # reached False, so we should not skip over the next target, we are done.
                chain_connections.append(JuncRoadChainConnection(curr_chain_id, chain))
                curr_chain_id += 1
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
                chain_connections.append(JuncRoadChainConnection(curr_chain_id, chain))
                curr_chain_id += 1
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
                    chain_connections.append(JuncRoadChainConnection(curr_chain_id, chain))
                    curr_chain_id += 1
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

    def __get_in_out_roads_dicts_by_single(self, roads: Set[JuncRoadSingleConnection]) \
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
            in_roads, out_roads = self.__get_in_out_roads_dicts_by_single(roads)
        else:
            in_roads, out_roads = in_out_dicts
        return {junc.indices for junc in self.get_all_juncs()
                if len(in_roads[junc.indices]) == len(out_roads[junc.indices]) == 1}

    #step 7
    def __set_roads_lanes(self, roads_chains: List[JuncRoadChainConnection]):
        """
        set lanes for each road chain, based on number of in-roads and out-roads of the junctions.
        number of lanes in a road is the number of out-roads of the junction that it is an in-road of.
        :param roads_chains: the road chains
        """
        in_roads, out_roads = self.__get_in_out_roads_dicts_by_chains(roads_chains)
        for junc in self.get_all_juncs():
            out_roads_count = len(out_roads[junc.indices])
            for in_road in in_roads[junc.indices]:
                in_road.set_lanes(out_roads_count)

    def __get_in_out_roads_dicts_by_chains(self, roads_chains: List[JuncRoadChainConnection]) \
            -> Tuple[Dict[JuncIndices, List[JuncRoadChainConnection]],
                     Dict[JuncIndices, List[JuncRoadChainConnection]]]:
        """
        :param roads: a set of all road chains
        :return: in_roads dict and out_roads dict of chains
        """
        # a dict of all roads that the key is their taget
        in_roads: Dict[JuncIndices, List[JuncRoadChainConnection]] = defaultdict(list)
        # a dict of all roads that the key is their source
        out_roads: Dict[JuncIndices, List[JuncRoadChainConnection]] = defaultdict(list)
        for road_chain in roads_chains:
            in_roads[road_chain.parts[-1].target].append(road_chain)
            out_roads[road_chain.parts[0].source].append(road_chain)
        return in_roads, out_roads

    #step 8
    def __set_junction_movement(self, roads_chains: List[JuncRoadChainConnection]) \
            -> Dict[JuncIndices, List[Tuple[RoadLane, RoadLane]]]:
        """
        generate data of goes_to for each junction
        :param roads_chains: all road chains
        :return: a dict that maps a junction to a list of all movements
        """
        goes_to_dict: Dict[JuncIndices, List[Tuple[RoadLane, RoadLane]]] = defaultdict(list)
        in_roads, out_roads = self.__get_in_out_roads_dicts_by_chains(roads_chains)
        for junc in self.get_all_juncs():
            junc_in_roads = in_roads[junc.indices]
            junc_out_roads = out_roads[junc.indices]
            """
            split to cases:
            1. if the junction has only out_roads, raise an error
            2. if the junction has only in_roads, do nothing.
            3. if the junction has 1-3 in_roads, then for each in_road, 
                send each of its lanes to the matching out_road, in its right-most lane.
            """
            # case 1
            if len(junc_in_roads) == 0:
                raise Exception(f"a junction must have an in_road. {junc}")
            # case 2
            if len(junc_out_roads) == 0:
                continue
            # case 3, the "else"
            for in_road in junc_in_roads:
                left_to_right_out_roads = self.__get_sorted_out_roads_by_in_road(in_road, junc_out_roads)
                # add the pair of (this_in_road,lane_number_from_left_to_right),(out_road,right_lane) to the dict
                for i, out_road in enumerate(left_to_right_out_roads):
                    goes_to_dict[junc.indices].append((
                        RoadLane(in_road.road_id, i),
                        RoadLane(out_road.road_id, out_road.lanes_num - 1)
                    ))
        return goes_to_dict

    def __get_sorted_out_roads_by_in_road(self, in_road: JuncRoadChainConnection,
                                          junc_out_roads: List[JuncRoadChainConnection]) \
            -> List[JuncRoadChainConnection]:
        """
        :param in_road: the road to sort by
        :param junc_out_roads: the out_roads of the junc
        :return: the out_roads list but ordered from left to right.
        """
        ordered_out_roads = list()
        in_road_single: JuncRoadSingleConnection = in_road.parts[-1]
        order: List[JuncConnDirection] \
            = [JuncConnDirection.UP, JuncConnDirection.RIGHT, JuncConnDirection.DOWN, JuncConnDirection.LEFT]
        in_direction_index = order.index(in_road_single.target_dir)
        # go from left to right relative to the in_road.
        for i in range(in_direction_index + 1, in_direction_index + 4):
            direction = order[i % 4]
            for out_road_chain in junc_out_roads:
                if out_road_chain.parts[0].source_dir == direction:
                    ordered_out_roads.append(out_road_chain)
                    break
        return ordered_out_roads
