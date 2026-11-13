"""Tests for the Graph class and graph representations."""

import pytest

from graphs_from_first_principles.graph import Graph


def test_empty_graph_initialization():
    g = Graph()
    assert not g.is_directed
    assert g.order() == 0
    assert g.size() == 0
    assert len(g) == 0
    assert g.vertices() == []
    assert g.edges() == []


def test_add_vertex_and_membership():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    # Adding duplicate vertex should not duplicate or erase neighbors
    g.add_vertex("A")

    assert g.order() == 2
    assert "A" in g
    assert "B" in g
    assert "C" not in g
    assert g.has_vertex("A")
    assert not g.has_vertex("C")
    assert g.neighbors("A") == []


def test_undirected_edge_symmetry():
    g = Graph(directed=False)
    g.add_edge("A", "B")

    assert g.has_edge("A", "B")
    assert g.has_edge("B", "A")
    assert "B" in g.neighbors("A")
    assert "A" in g.neighbors("B")
    assert g.degree("A") == 1
    assert g.degree("B") == 1
    assert g.order() == 2
    assert g.size() == 1


def test_directed_edge_asymmetry():
    g = Graph(directed=True)
    g.add_edge("A", "B")

    assert g.has_edge("A", "B")
    assert not g.has_edge("B", "A")
    assert g.neighbors("A") == ["B"]
    assert g.neighbors("B") == []
    assert g.out_degree("A") == 1
    assert g.in_degree("A") == 0
    assert g.out_degree("B") == 0
    assert g.in_degree("B") == 1
    assert g.order() == 2
    assert g.size() == 1


def test_idempotent_edges():
    g = Graph(directed=False)
    g.add_edge("A", "B")
    g.add_edge("A", "B")

    assert g.neighbors("A") == ["B"]
    assert g.neighbors("B") == ["A"]
    assert g.size() == 1


def test_neighbors_returns_defensive_copy():
    g = Graph()
    g.add_edge("A", "B")
    nbrs = g.neighbors("A")
    nbrs.append("FAKE")

    assert "FAKE" not in g.neighbors("A")


def test_nonexistent_vertex_error():
    g = Graph()
    with pytest.raises(KeyError):
        g.neighbors("Z")
    with pytest.raises(KeyError):
        g.in_degree("Z")
    with pytest.raises(KeyError):
        g.out_degree("Z")


def test_isolated_vertices():
    g = Graph()
    g.add_vertex("ISO_1")
    g.add_vertex("ISO_2")
    g.add_edge("A", "B")

    assert g.order() == 4
    assert g.size() == 1
    assert g.neighbors("ISO_1") == []
    assert g.degree("ISO_1") == 0
    assert g.neighbors("ISO_2") == []


def test_self_loop():
    g = Graph(directed=False)
    g.add_edge("A", "A")
    assert g.has_edge("A", "A")
    assert g.neighbors("A") == ["A"]


def test_to_adjacency_matrix_undirected():
    g = Graph(directed=False)
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_vertex("D")  # isolated

    matrix, labels = g.to_adjacency_matrix()
    assert labels == ["A", "B", "C", "D"]
    assert len(matrix) == 4

    # Row A: connected to B
    assert matrix[0] == [0, 1, 0, 0]
    # Row B: connected to A and C
    assert matrix[1] == [1, 0, 1, 0]
    # Row C: connected to B
    assert matrix[2] == [0, 1, 0, 0]
    # Row D: isolated
    assert matrix[3] == [0, 0, 0, 0]

    # Symmetric matrix for undirected graph
    for i in range(4):
        for j in range(4):
            assert matrix[i][j] == matrix[j][i]


def test_to_adjacency_matrix_directed():
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("B", "C")

    matrix, labels = g.to_adjacency_matrix()
    assert labels == ["A", "B", "C"]
    # A -> B
    assert matrix[0] == [0, 1, 0]
    # B -> C
    assert matrix[1] == [0, 0, 1]
    # C has no outgoing edges
    assert matrix[2] == [0, 0, 0]


def test_repr_string():
    g = Graph(directed=False)
    g.add_edge("A", "B")
    assert repr(g) == "<Undirected Graph with 2 vertices and 1 edges>"

    dg = Graph(directed=True)
    dg.add_edge("X", "Y")
    assert repr(dg) == "<Directed Graph with 2 vertices and 1 edges>"
