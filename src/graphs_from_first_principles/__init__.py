"""Graphs from First Principles.

A clear, educational, and tested Python package exploring graph representations,
depth-first search, breadth-first search, component traversal, and complexity analysis.
"""

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

__all__ = [
    "Graph",
    "bfs",
    "bfs_shortest_path",
    "dfs_all_components",
    "dfs_iterative",
    "dfs_recursive",
    "find_connected_components",
    "has_cycle",
]
