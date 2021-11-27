import pytest
from graph import Graph, Node, Edge


@pytest.fixture(scope='function')
def default_graph():
    graph = Graph()
    return graph


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
