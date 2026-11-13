"""Graph data structures from first principles.

This module provides a simple, clean, and educational implementation of a Graph
using an adjacency list as the primary internal representation.
"""

from __future__ import annotations

from collections.abc import Hashable
from typing import Generic, TypeVar

T = TypeVar("T", bound=Hashable)


class Graph(Generic[T]):
    """A graph represented using an adjacency list.

    An adjacency list stores the graph as a dictionary where every vertex
    is a key, and its associated value is a list of neighboring vertices.

    Parameters
    ----------
    directed : bool, default=False
        If True, edges are directed (u -> v does not imply v -> u).
        If False, edges are undirected (an edge connects u and v symmetrically).
    """

    def __init__(self, directed: bool = False) -> None:
        self._directed: bool = directed
        # Internal adjacency list: maps vertex -> list of neighbors.
        # Python 3.7+ dictionaries preserve insertion order.
        self._adj: dict[T, list[T]] = {}

    @property
    def is_directed(self) -> bool:
        """Return True if the graph is directed, False otherwise."""
        return self._directed

    def add_vertex(self, vertex: T) -> None:
        """Add a vertex to the graph if it does not already exist.

        Parameters
        ----------
        vertex : T
            The vertex identifier (e.g., string, integer).
        """
        if vertex not in self._adj:
            self._adj[vertex] = []

    def add_edge(self, u: T, v: T) -> None:
        """Add an edge between vertex u and vertex v.

        If either vertex does not exist in the graph, it is automatically added.
        For undirected graphs, the connection is bidirectional (u <-> v).
        For directed graphs, the connection is one-way (u -> v).

        Duplicate edges are ignored to maintain a simple graph.

        Parameters
        ----------
        u : T
            The starting vertex (source).
        v : T
            The ending vertex (destination for directed; partner for undirected).
        """
        self.add_vertex(u)
        self.add_vertex(v)

        if v not in self._adj[u]:
            self._adj[u].append(v)

        if not self._directed and u not in self._adj[v]:
            self._adj[v].append(u)

    def neighbors(self, vertex: T) -> list[T]:
        """Return a copy of the list of neighbors adjacent to the given vertex.

        For directed graphs, this returns outgoing neighbors (vertices v such that u -> v).

        Parameters
        ----------
        vertex : T
            The vertex whose neighbors to retrieve.

        Returns
        -------
        list[T]
            List of neighboring vertices in deterministic insertion order.

        Raises
        ------
        KeyError
            If the vertex does not exist in the graph.
        """
        if vertex not in self._adj:
            raise KeyError(f"Vertex {vertex!r} not in graph")
        return list(self._adj[vertex])

    def has_vertex(self, vertex: T) -> bool:
        """Check if a vertex exists in the graph."""
        return vertex in self._adj

    def has_edge(self, u: T, v: T) -> bool:
        """Check if an edge exists from u to v.

        Parameters
        ----------
        u : T
            Source vertex.
        v : T
            Destination vertex.

        Returns
        -------
        bool
            True if edge (u, v) exists, False otherwise.
        """
        if u not in self._adj or v not in self._adj:
            return False
        return v in self._adj[u]

    def vertices(self) -> list[T]:
        """Return all vertices in the graph in insertion order."""
        return list(self._adj.keys())

    def edges(self) -> list[tuple[T, T]]:
        """Return a list of all edges in the graph.

        For directed graphs, returns each directed edge (u, v).
        For undirected graphs, each undirected edge is returned once as (u, v).
        """
        edge_list: list[tuple[T, T]] = []
        seen_undirected: set[frozenset[T]] = set()

        for u, nbrs in self._adj.items():
            for v in nbrs:
                if self._directed:
                    edge_list.append((u, v))
                else:
                    edge_key = frozenset({u, v})
                    if edge_key not in seen_undirected:
                        seen_undirected.add(edge_key)
                        edge_list.append((u, v))
        return edge_list

    def order(self) -> int:
        """Return the number of vertices in the graph (|V|)."""
        return len(self._adj)

    def size(self) -> int:
        """Return the number of edges in the graph (|E|)."""
        return len(self.edges())

    def degree(self, vertex: T) -> int:
        """Return the degree (number of incident edges) of a vertex.

        For directed graphs, this returns the out-degree (number of outgoing edges).
        """
        return len(self.neighbors(vertex))

    def in_degree(self, vertex: T) -> int:
        """Return the in-degree (number of incoming edges) of a vertex.

        Parameters
        ----------
        vertex : T
            The target vertex.

        Raises
        ------
        KeyError
            If the vertex does not exist in the graph.
        """
        if vertex not in self._adj:
            raise KeyError(f"Vertex {vertex!r} not in graph")
        return sum(1 for u in self._adj if vertex in self._adj[u])

    def out_degree(self, vertex: T) -> int:
        """Return the out-degree (number of outgoing edges) of a vertex.

        Parameters
        ----------
        vertex : T
            The source vertex.

        Raises
        ------
        KeyError
            If the vertex does not exist in the graph.
        """
        return self.degree(vertex)

    def to_adjacency_matrix(self) -> tuple[list[list[int]], list[T]]:
        """Convert the adjacency list to an adjacency matrix representation.

        Returns
        -------
        matrix : list[list[int]]
            A 2D square matrix where matrix[i][j] == 1 if edge vertex_labels[i] -> vertex_labels[j]
            exists, and 0 otherwise.
        vertex_labels : list[T]
            The ordered list of vertices corresponding to matrix indices.
        """
        labels = self.vertices()
        index_map = {label: i for i, label in enumerate(labels)}
        n = len(labels)
        matrix = [[0] * n for _ in range(n)]

        for u, nbrs in self._adj.items():
            i = index_map[u]
            for v in nbrs:
                j = index_map[v]
                matrix[i][j] = 1

        return matrix, labels

    def __contains__(self, vertex: T) -> bool:
        return self.has_vertex(vertex)

    def __len__(self) -> int:
        return self.order()

    def __iter__(self):
        return iter(self._adj)

    def __repr__(self) -> str:
        kind = "Directed" if self._directed else "Undirected"
        return f"<{kind} Graph with {self.order()} vertices and {self.size()} edges>"
