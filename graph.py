from dataclasses import dataclass
from functools import total_ordering, lru_cache
from typing import Set, Iterable, Optional, List

from scipy.io import mmread


class NoSuchNodeException(Exception):
    """ Raised when requested node does not exist """
    pass


@total_ordering
@dataclass()
class Node:
    idx: int

    def __lt__(self, other) -> bool:
        return self.idx < other.idx

    def __eq__(self, other):
        return self.idx == other.idx

    def __hash__(self):
        return hash(self.idx)


class Edge:
    def __init__(self, node_a: Node, node_b: Node, pheromone: float = 0.0):
        self.node_a = node_a
        self.node_b = node_b
        self.pheromone = pheromone

    @property
    def nodes(self) -> Set[Node]:
        """
        :return: Set of two nodes that create the edge
        """
        return {self.node_a, self.node_b}

    def __eq__(self, other) -> bool:
        return self.nodes == other.nodes

    def __hash__(self):
        return hash(tuple(sorted(self.nodes)))

    def __str__(self):
        return f'Edge({self.node_a.idx}, {self.node_b.idx}, {self.pheromone})'

    __repr__ = __str__


class Graph:
    def __init__(self):
        self.edges: Set[Edge] = set()
        self.nodes: Set[Node] = set()

    def add_edge(self, edge: Edge) -> None:
        """
        Adds edge to the graph

        :param edge: Edge to be added
        """
        if edge not in self.edges:
            self.edges.add(edge)
            self.add_nodes(edge.nodes)
        self.get_node_edges.cache_clear()
        self.get_node_neighbours.cache_clear()

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
        return f'Graph({len(self.nodes)}, {len(self.edges)})'

    @classmethod
    def read_from_file(cls, filepath):
        """
        Instantiates new Graph object initializes it with data provided in `filepath` file.

        :param filepath: File containing graph data
        :type filepath: str
        :return: New Graph instance
        :rtype: Graph
        """
        g = mmread(filepath)
        instance = cls()

        for g_edge in zip(g.row, g.col):
            start_node, end_node = map(Node, g_edge)
            edge = Edge(start_node, end_node)
            instance.add_edge(edge)

        return instance

    @lru_cache
    def get_node_edges(self, node: Node) -> Set[Edge]:
        """
        :param node: Node which edges set should be returned
        :returns: Set of edges connected to `node`
        """
        return {edge for edge in self.edges if node in edge.nodes}

    @lru_cache
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

    def get_node_by_index(self, index: int) -> Node:
        """
        :param index: Index of the requested node
        :return: Node instance with given `index` that belongs to graph
        :raises NoSuchNodeException: if node with requested index doesnt belong to graph
        """
        try:
            return next((node for node in self.nodes if node.idx == index))
        except StopIteration:
            raise NoSuchNodeException(f'Cannot find node with index {index}')

    def has_edge_between(self, node_a: Node, node_b: Node) -> bool:
        for edge in self.edges:
            if {node_a, node_b} == edge.nodes:
                return True
        else:
            return False

    def get_edge_by_nodes(self, node_a: Node, node_b: Node) -> Optional[Edge]:
        for edge in self.edges:
            if {node_a, node_b} == edge.nodes:
                return edge
        else:
            return None


class CliqueConstraintViolationError(Exception):
    """ Raised when any clique constraint is violated """
    pass


class Clique:
    def __init__(self, graph):
        self.edges: Set[Edge] = set()
        self.nodes: Set[Node] = set()
        self.graph: Graph = graph

    def __is_connected_with_all_nodes(self, node: Node) -> bool:
        """
        Checks if all nodes that belongs to clique are connected by any edge to `node`

        :param node: Node for which check should be executed
        :return: True if all clique nodes are connected to `node`, False otherwise
        """
        return all(
            self.graph.has_edge_between(node, existing_node) for existing_node in self.nodes
        )

    def add_node(self, node: Node, unsafe=True):
        """
        Adds `node` to clique. Also adds edges between `node` and existing clique nodes.

        :param node: Node to be added to clique
        :raises CliqueConstraintViolationError: if node given as argument cannot be added to clique
        """
        if unsafe or self.__is_connected_with_all_nodes(node):
            self.edges.update(
                {self.graph.get_edge_by_nodes(node, existing_node) for existing_node in self.nodes}
            )
            self.nodes.add(node)
        else:
            raise CliqueConstraintViolationError(
                f"Cannot add node {node} because it's not connected to all existing nodes: {self.nodes}")

    def get_candidates(self) -> List[Node]:
        possible_candidates = [node for node in self.graph.nodes if self.__is_connected_with_all_nodes(node)]

        # Slower alternative:
        # possible_candidates = [neighbour for node in self.nodes for neighbour in self.graph.get_node_neighbours(node) if self.__is_connected_with_all_nodes(neighbour)]

        return possible_candidates

    def get_edge_candidates(self) -> List[Edge]:
        node_candidates = self.get_candidates()
        edge_candidates = []
        for node_candidate in node_candidates:
            for clique_node in self.nodes:
                edge_candidates.append(self.graph.get_edge_by_nodes(node_candidate, clique_node))

        return edge_candidates

    def get_pheromone_factor(self, node: Node) -> float:
        """
        Returns pheromone factor for (Node, Clique) pair.
        Pheromone factor is a sum of pheromones on all edges connecting `node` and clique's nodes.
        """
        return sum(self.graph.get_edge_by_nodes(clique_node, node).pheromone for clique_node in self.nodes)
