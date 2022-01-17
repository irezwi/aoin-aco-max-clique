from pathlib import Path

import pytest

from maxclique.config import INPUT_DIR
from src.maxclique.graph import (
    Clique,
    CliqueConstraintViolationError,
    Edge,
    Graph,
    Node,
)

TEST_PATH = Path(__file__) / ".."


@pytest.fixture(scope="function")
def k5_graph():
    """
    Graph:
        1 - 2
        | X |
        3 - 4
    """
    k5_path = (TEST_PATH / "k5.mtx").resolve()
    graph = Graph(str(k5_path))
    yield graph


@pytest.fixture(scope="function")
def k5_plus_one():
    """
    Graph:
        1 - 2
        | X |
        3 - 4 - 5
    """
    k5_plus_one_path = (TEST_PATH / "k5_plus_one.mtx").resolve()
    graph = Graph(str(k5_plus_one_path))
    yield graph


@pytest.mark.parametrize(
    "node, outgoing_edges",
    [
        (0, [(0, 1), (0, 2), (0, 3), (0, 4)]),
        (1, [(1, 0), (1, 2), (1, 3), (1, 4)]),
        (2, [(2, 0), (2, 1), (2, 3), (2, 4)]),
        (3, [(3, 0), (3, 1), (3, 2), (3, 4)]),
        (4, [(4, 0), (4, 1), (4, 2), (4, 3)]),
    ],
)
def test_get_node_edges(k5_graph, node, outgoing_edges):
    graph = k5_graph

    expected_edges = set()
    for a, b in outgoing_edges:
        expected_edges.add(Edge(a, b, 0.0))
        expected_edges.add(Edge(b, a, 0.0))

    assert graph.get_node_edges(node) == expected_edges


def test_graph_repr(k5_graph):
    assert repr(k5_graph) == "Graph(5, 20)"


@pytest.mark.parametrize(
    "file, expected_nodes, expected_edges",
    [
        ("C250-9.mtx", 250, 27984),
        ("C500-9.mtx", 500, 112332),
        ("keller4.mtx", 171, 9435),
        ("keller5.mtx", 776, 225990),
    ],
)
def test_read_from_file(file, expected_nodes, expected_edges):
    filepath = INPUT_DIR / file
    graph = Graph(filepath)

    assert len(graph.nodes) == expected_nodes
    assert len(graph.edges) == expected_edges * 2


def test_clique(k5_graph):
    clique = Clique(graph=k5_graph)

    for node in clique.graph.nodes:
        clique.add_node(node)

    assert len(clique.nodes) == 5
    assert len(clique.edges) == 10


@pytest.mark.parametrize("unsafe", [True, False])
def test_error_on_invalid_add(k5_plus_one, unsafe):
    graph = k5_plus_one
    clique = Clique(graph=graph)
    correct_nodes = [Node(i) for i in range(5)]
    invalid_node = Node(5)

    for node in correct_nodes:
        clique.add_node(node)

    assert len(clique.nodes) == len(correct_nodes)

    if unsafe:
        clique.add_node(invalid_node, unsafe=unsafe)
        assert len(clique.nodes) == len(correct_nodes) + 1
    else:
        with pytest.raises(CliqueConstraintViolationError) as exception:
            clique.add_node(invalid_node, unsafe=unsafe)
        assert len(clique.nodes) == len(correct_nodes)
        assert isinstance(exception.value, CliqueConstraintViolationError)


def test_get_candidates(k5_graph):
    clique = Clique(graph=k5_graph)

    for node in clique.graph.nodes:
        clique.add_node(node)
        assert set(clique.get_candidates()) == clique.graph.nodes.difference(
            clique.nodes
        )


def test_node_neighbors(k5_graph, k5_plus_one):
    assert k5_graph.get_node_neighbours(0) == {1, 2, 3, 4}
    assert k5_plus_one.get_node_neighbours(5) == {4}
