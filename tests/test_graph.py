from itertools import combinations
from os.path import join
import pytest
from graph import Graph, Node, Edge, Clique, CliqueConstraintViolationError


@pytest.fixture(scope='function')
def default_graph():
    """ Empty graph """
    graph = Graph()
    return graph


@pytest.fixture(scope='function')
def k5_graph():
    """
    Graph:
        1 - 2
        | X |
        3 - 4
    """
    graph = Graph()
    nodes = [Node(i) for i in range(5)]
    graph.add_nodes(nodes)
    for start_node, end_node in combinations(range(5), 2):
        edge = Edge(Node(start_node), Node(end_node))
        graph.add_edge(edge)
    yield graph


@pytest.fixture(scope='function')
def k5_plus_one(k5_graph):
    """
    Graph:
        1 - 2
        | X |
        3 - 4 - 5
    """
    graph = k5_graph
    graph.add_node(Node(5))
    graph.add_edge(
        Edge(Node(4), Node(5))
    )
    yield graph


def test_indirect_edges(default_graph):
    graph = default_graph
    n1, n2 = Node(1), Node(2)
    from_n1_to_n2 = Edge(n1, n2)
    from_n2_to_n1 = Edge(n2, n1)

    graph.add_edge(from_n1_to_n2)
    graph.add_edge(from_n2_to_n1)

    assert len(graph.edges) == 1
    assert len(graph.nodes) == 2
    assert n1 in graph.nodes
    assert n2 in graph.nodes
    assert from_n1_to_n2 in graph.edges
    assert from_n2_to_n1 in graph.edges


def test_get_node_edges(k5_graph):
    graph = k5_graph

    expected_edges = {Edge(Node(0), Node(i)) for i in range(1, 5)}
    assert graph.get_node_edges(Node(0)) == expected_edges


@pytest.mark.parametrize(
    "file, expected_nodes, expected_edges",
    [
        ('soc-dolphins.mtx', 62, 159),
        ('keller5.mtx', 776, 225990),
    ]
)
def test_read_from_file(file, expected_nodes, expected_edges):
    filepath = join('..', 'input', file)
    graph = Graph.read_from_file(filepath)

    assert len(graph.nodes) == expected_nodes
    assert len(graph.edges) == expected_edges


def test_clique(k5_graph):
    clique = Clique(graph=k5_graph)

    for node in clique.graph.nodes:
        clique.add_node(node)

    assert len(clique.nodes) == 5
    assert len(clique.edges) == 10


def test_error_on_invalid_add(k5_plus_one):
    graph = k5_plus_one
    clique = Clique(graph=graph)
    correct_nodes = [Node(i) for i in range(5)]
    invalid_node = Node(5)

    for node in correct_nodes:
        clique.add_node(node)

    with pytest.raises(CliqueConstraintViolationError):
        clique.add_node(invalid_node)


def test_get_candidates(k5_graph):
    clique = Clique(graph=k5_graph)

    for node in clique.graph.nodes:
        clique.add_node(node)
        assert set(clique.get_candidates()) == clique.graph.nodes.difference(clique.nodes)