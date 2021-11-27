from dataclasses import dataclass
from functools import total_ordering
from typing import Set

from scipy.io import mmread


@total_ordering
@dataclass(eq=True, frozen=True, unsafe_hash=True)
class Node:
    idx: int

    def __lt__(self, other) -> bool:
        return self.idx < other.idx


@dataclass(frozen=True)
class Edge:
    node_a: Node
    node_b: Node

    @property
    def nodes(self) -> Set[Node]:
        return {self.node_a, self.node_b}

    def __eq__(self, other) -> bool:
        return {self.node_a, self.node_b} == {other.node_a, other.node_b}

    def __hash__(self):
        return hash(tuple(sorted(self.nodes)))


class Graph:
    def __init__(self):
        self.edges: Set[Edge] = set()
        self.nodes: Set[Node] = set()

    def add_edge(self, edge: Edge) -> None:
        if edge not in self.edges:
            self.edges.add(edge)
            self.nodes.update(edge.nodes)

    def __repr__(self) -> str:
        return f'Graph({len(self.nodes)}, {len(self.edges)})'

    @classmethod
    def read_from_file(cls, filepath):
        g = mmread(filepath)
        instance = cls()

        for g_edge in zip(g.row, g.col):
            start_node, end_node = map(Node, g_edge)
            edge = Edge(start_node, end_node)
            instance.add_edge(edge)

        return instance
