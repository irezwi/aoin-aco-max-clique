from dataclasses import dataclass
from functools import lru_cache, cached_property
from itertools import starmap
from typing import Iterable, List, Optional, Set

import numpy as np
from scipy.io import mmread


class NoSuchNodeException(Exception):
    """Raised when requested node does not exist"""

    pass


Node = int


@dataclass(frozen=True, unsafe_hash=True)
class Edge:
    node_a: Node
    node_b: Node
    pheromone: float

    @property
    def nodes(self):
        return {self.node_a, self.node_b}


NO_EDGE = -1


class GraphBase:
    def __init__(self):
        self._edges: Set[Edge] = set()
        self._nodes: Set[Node] = set()
        self._structure = None

    @property
    def edges(self):
        return self._edges

    @property
    def nodes(self):
        return self._nodes

    def has_edge_between(self, node_a: Node, node_b: Node) -> bool:
        return self._structure[node_a][node_b] != NO_EDGE

    def get_edge_by_nodes(self, node_a: Node, node_b: Node) -> Optional[Edge]:
        return Edge(node_a, node_b, self._structure[node_a][node_b])


class Graph(GraphBase):
    def __init__(self, filepath):
        """
        Instantiates new Graph object initializes it with data provided in `filepath` file.

        :param filepath: File containing graph data
        :type filepath: str
        :return: New Graph instance
        :rtype: Graph
        """
        super().__init__()

        if filepath:
            g = mmread(filepath)
            self._structure = np.ones(shape=g.shape) * -1

            for node_a, node_b in zip(g.row, g.col):
                edge = Edge(node_a, node_b, 0)
                self.add_edge(edge)

        self.enable_cache()

    @property
    def edges(self):
        indexes = np.where(self._structure != NO_EDGE)
        return set(starmap(Edge, zip(*indexes, self._structure[indexes])))

    def _modify_structure(self, node_a, node_b, value):
        self._structure[node_a, node_b] = value
        self._structure[node_b, node_a] = value

    def add_edge(self, edge: Edge) -> None:
        """
        Adds edge to the graph

        :param edge: Edge to be added
        """
        self.add_nodes(edge.nodes)
        self._modify_structure(edge.node_a, edge.node_b, edge.pheromone)

    def add_node(self, node: Node) -> None:
        """
        Adds node to the graph

        :param node: Node to be added
        """
        self.nodes.add(node)

    def add_nodes(self, nodes: Iterable[Node]) -> None:
        """
        Adds nodes to the graph

        :param nodes: Collection of nodes to be added
        """
        self.nodes.update(nodes)

    def __repr__(self) -> str:
        return f"Graph({len(self.nodes)}, {len(self.edges)})"

    def get_node_edges(self, node: Node) -> Set[Edge]:
        """
        :param node: Node which edges set should be returned
        :returns: Set of edges connected to `node`
        """
        return {edge for edge in self.edges if node in edge.nodes}

    def get_node_neighbours(self, node: Node) -> Set[Node]:
        """
        :param node: Node which neighbours should be returned
        :returns: Set of nodes directly connected to `node`
        """
        neighbours = set()
        node_edges = self.get_node_edges(node)
        for edge in node_edges:
            for edge_node in edge.nodes:
                if edge_node != node:
                    neighbours.add(edge_node)
        return neighbours

    def set_pheromone(self, node_a, node_b, value):
        self._modify_structure(node_a, node_b, value)

    def enable_cache(self):
        """
        Hacky, but it's dumb to calculate it over and over if graph structure never changes after initialization
        """
        self.get_node_edges = lru_cache(maxsize=None)(self.get_node_edges)
        self.get_node_neighbours = lru_cache(maxsize=None)(self.get_node_neighbours)

        # import time
        # start = time.time()
        # for node in self.nodes:
        #     self.get_node_edges(node)
        #     self.get_node_neighbours(node)
        # print(f'Preprocessing time: {time.time() - start}')


class CliqueConstraintViolationError(Exception):
    """Raised when any clique constraint is violated"""

    pass


class Clique(GraphBase):
    def __init__(self, graph):
        super().__init__()
        self.graph: Graph = graph

    def __is_connected_with_all_nodes(self, node: Node) -> bool:
        """
        Checks if all nodes that belongs to clique are connected by any edge to `node`

        :param node: Node for which check should be executed
        :return: True if all clique nodes are connected to `node`, False otherwise
        """
        return all(
            self.graph.has_edge_between(node, existing_node)
            for existing_node in self.nodes
        )

    def add_node(self, node: Node, unsafe=True):
        """
        Adds `node` to clique. Also adds edges between `node` and existing clique nodes.

        :param node: Node to be added to clique
        :raises CliqueConstraintViolationError: if node given as argument cannot be added to clique
        """
        if unsafe or self.__is_connected_with_all_nodes(node):
            self.edges.update(
                {
                    self.graph.get_edge_by_nodes(node, existing_node)
                    for existing_node in self.nodes
                }
            )
            self.nodes.add(node)
        else:
            raise CliqueConstraintViolationError(
                f"Cannot add node {node} because it's not connected to all existing nodes: {self.nodes}"
            )

    def get_candidates(self) -> List[Node]:
        possible_candidates = [
            node
            for node in self.graph.nodes
            if self.__is_connected_with_all_nodes(node)
        ]

        # Slower alternative:
        # possible_candidates = [neighbour for node in self.nodes for neighbour in self.graph.get_node_neighbours(node) if self.__is_connected_with_all_nodes(neighbour)]

        return possible_candidates

    def get_edge_candidates(self) -> List[Edge]:
        node_candidates = self.get_candidates()
        edge_candidates = []
        for node_candidate in node_candidates:
            for clique_node in self.nodes:
                edge_candidates.append(
                    self.graph.get_edge_by_nodes(node_candidate, clique_node)
                )

        return edge_candidates

    def get_pheromone_factor(self, node: Node) -> float:
        """
        Returns pheromone factor for (Node, Clique) pair.
        Pheromone factor is a sum of pheromones on all edges connecting `node` and clique's nodes.
        """
        return sum(
            self.graph.get_edge_by_nodes(clique_node, node).pheromone
            for clique_node in self.nodes
        )
