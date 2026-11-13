"""Tests for DFS, BFS, shortest paths, components, and cycles."""

import pytest

from graphs_from_first_principles.graph import Graph
from graphs_from_first_principles.traversals import (
    bfs,
    bfs_shortest_path,
    dfs_all_components,
    dfs_iterative,
    dfs_recursive,
    find_connected_components,
    has_cycle,
)


def build_sample_tree() -> Graph[str]:
    """Build a simple undirected tree:
          A
         / \
        B   C
       / \
      D   E
    """
    g = Graph[str](directed=False)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("B", "E")
    return g


def build_sample_graph_with_cycle() -> Graph[str]:
    r"""Build a graph with a triangle cycle and branching:
    A --- B
     \   /
       C --- D
    """
    g = Graph[str](directed=False)
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")
    g.add_edge("C", "D")
    return g


def test_dfs_recursive_on_tree():
    g = build_sample_tree()
    # With deterministic insertion order: A -> B -> D, backtrack to B -> E, backtrack to A -> C
    order = dfs_recursive(g, "A")
    assert order == ["A", "B", "D", "E", "C"]


def test_dfs_iterative_matches_recursive_order():
    g = build_sample_tree()
    rec_order = dfs_recursive(g, "A")
    it_order = dfs_iterative(g, "A")
    assert rec_order == it_order


def test_dfs_on_cyclic_graph_terminates():
    g = build_sample_graph_with_cycle()
    # Should visit all 4 nodes without infinite loop
    order = dfs_recursive(g, "A")
    assert set(order) == {"A", "B", "C", "D"}
    assert len(order) == 4

    it_order = dfs_iterative(g, "A")
    assert set(it_order) == {"A", "B", "C", "D"}
    assert len(it_order) == 4


def test_bfs_level_order():
    g = build_sample_tree()
    # Tree:
    # Level 0: A
    # Level 1: B, C
    # Level 2: D, E
    order = bfs(g, "A")
    assert order == ["A", "B", "C", "D", "E"]


def test_dfs_vs_bfs_order_contrast():
    """Demonstrate how DFS and BFS explore different orders on the same graph."""
    g = build_sample_tree()
    dfs_order = dfs_recursive(g, "A")
    bfs_order = bfs(g, "A")

    # In DFS, D and E are visited BEFORE C because DFS goes deep first
    assert dfs_order.index("D") < dfs_order.index("C")
    # In BFS, C is visited BEFORE D and E because C is closer (distance 1 vs distance 2)
    assert bfs_order.index("C") < bfs_order.index("D")


def test_traversal_errors_on_missing_start():
    g = Graph()
    g.add_edge("A", "B")

    with pytest.raises(KeyError):
        dfs_recursive(g, "MISSING")
    with pytest.raises(KeyError):
        dfs_iterative(g, "MISSING")
    with pytest.raises(KeyError):
        bfs(g, "MISSING")
    with pytest.raises(KeyError):
        bfs_shortest_path(g, "MISSING", "A")
    with pytest.raises(KeyError):
        bfs_shortest_path(g, "A", "MISSING")


def test_bfs_shortest_path_unweighted():
    # Graph with a shortcut vs a long path:
    # S -- A -- B -- C -- T  (path of length 4)
    # S ------- D ------- T  (path of length 2)
    g = Graph[str](directed=False)
    g.add_edge("S", "A")
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "T")

    g.add_edge("S", "D")
    g.add_edge("D", "T")

    path = bfs_shortest_path(g, "S", "T")
    assert path == ["S", "D", "T"]


def test_bfs_shortest_path_same_start_and_target():
    g = Graph[str]()
    g.add_vertex("A")
    assert bfs_shortest_path(g, "A", "A") == ["A"]


def test_bfs_shortest_path_unreachable():
    # Disconnected graph: A-B and C-D
    g = Graph[str](directed=False)
    g.add_edge("A", "B")
    g.add_edge("C", "D")

    assert bfs_shortest_path(g, "A", "C") is None


def test_disconnected_components():
    g = Graph[str](directed=False)
    # Component 1
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    # Component 2
    g.add_edge("X", "Y")
    # Component 3 (isolated node)
    g.add_vertex("Z")

    # Starting BFS from A only visits Component 1
    reachable_from_a = bfs(g, "A")
    assert set(reachable_from_a) == {"A", "B", "C"}
    assert "X" not in reachable_from_a
    assert "Z" not in reachable_from_a

    # Full component detection visits all 3 components
    components = find_connected_components(g)
    assert len(components) == 3

    comp_sets = [set(c) for c in components]
    assert {"A", "B", "C"} in comp_sets
    assert {"X", "Y"} in comp_sets
    assert {"Z"} in comp_sets

    # Alias check
    assert dfs_all_components(g) == components


def test_has_cycle_undirected():
    # Tree (acyclic)
    tree = build_sample_tree()
    assert not has_cycle(tree)

    # Triangle cycle
    cyclic_g = build_sample_graph_with_cycle()
    assert has_cycle(cyclic_g)

    # Empty graph
    empty = Graph()
    assert not has_cycle(empty)

    # Single isolated vertex
    single = Graph()
    single.add_vertex("A")
    assert not has_cycle(single)

    # Disconnected graph where component 2 has a cycle
    disc = Graph(directed=False)
    disc.add_edge("A", "B")  # Component 1 (acyclic)
    disc.add_edge("C", "D")  # Component 2 (cyclic: C-D, D-E, E-C)
    disc.add_edge("D", "E")
    disc.add_edge("E", "C")
    assert has_cycle(disc)


def test_has_cycle_directed():
    # Directed Acyclic Graph (DAG)
    # A -> B -> D
    # A -> C -> D
    dag = Graph[str](directed=True)
    dag.add_edge("A", "B")
    dag.add_edge("A", "C")
    dag.add_edge("B", "D")
    dag.add_edge("C", "D")
    assert not has_cycle(dag)

    # Directed Cycle: A -> B -> C -> A
    d_cycle = Graph[str](directed=True)
    d_cycle.add_edge("A", "B")
    d_cycle.add_edge("B", "C")
    d_cycle.add_edge("C", "A")
    assert has_cycle(d_cycle)

    # Directed graph with self-loop: X -> X
    self_loop = Graph[str](directed=True)
    self_loop.add_edge("X", "X")
    assert has_cycle(self_loop)
