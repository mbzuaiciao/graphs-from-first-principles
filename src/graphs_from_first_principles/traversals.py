"""Graph traversals and search algorithms from first principles.

This module provides clear, educational implementations of:
- Depth-First Search (DFS), both recursive and iterative
- Breadth-First Search (BFS) using collections.deque
- Shortest-path finding in unweighted graphs using BFS
- Disconnected graph traversal and connected component detection
- Cycle detection for both undirected and directed graphs
"""

from __future__ import annotations

from collections import deque
from collections.abc import Hashable
from typing import TypeVar

from graphs_from_first_principles.graph import Graph

T = TypeVar("T", bound=Hashable)


def dfs_recursive(
    graph: Graph[T],
    start: T,
    visited: set[T] | None = None,
    order: list[T] | None = None,
) -> list[T]:
    """Perform recursive Depth-First Search (DFS) starting from a vertex.

    DFS explores as deep as possible along each branch before backtracking.
    A visited set is maintained to prevent infinite recursion caused by cycles.

    Parameters
    ----------
    graph : Graph[T]
        The graph to traverse.
    start : T
        The starting vertex.
    visited : set[T] | None, default=None
        Set of already-visited vertices across recursive calls.
    order : list[T] | None, default=None
        Accumulator list recording vertices in the order they are visited.

    Returns
    -------
    list[T]
        List of vertices in the order they were visited.

    Raises
    ------
    KeyError
        If the starting vertex does not exist in the graph.
    """
    if not graph.has_vertex(start):
        raise KeyError(f"Start vertex {start!r} does not exist in graph")

    if visited is None:
        visited = set()
    if order is None:
        order = []

    visited.add(start)
    order.append(start)

    for neighbor in graph.neighbors(start):
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited, order)

    return order


def dfs_iterative(graph: Graph[T], start: T) -> list[T]:
    """Perform iterative Depth-First Search (DFS) using an explicit stack.

    Instead of relying on the Python call stack, this implementation uses a
    standard list as a Last-In, First-Out (LIFO) stack.

    To match the deterministic left-to-right neighbor exploration of recursive DFS,
    neighbors are pushed onto the stack in reverse order so that the first neighbor
    is popped and processed first.

    Parameters
    ----------
    graph : Graph[T]
        The graph to traverse.
    start : T
        The starting vertex.

    Returns
    -------
    list[T]
        List of vertices in the order they were visited.

    Raises
    ------
    KeyError
        If the starting vertex does not exist in the graph.
    """
    if not graph.has_vertex(start):
        raise KeyError(f"Start vertex {start!r} does not exist in graph")

    visited: set[T] = {start}
    stack: list[T] = [start]
    order: list[T] = []

    while stack:
        curr = stack.pop()
        order.append(curr)

        # Push unvisited neighbors in reverse order so the first neighbor is on top
        for neighbor in reversed(graph.neighbors(curr)):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return order


def bfs(graph: Graph[T], start: T) -> list[T]:
    """Perform Breadth-First Search (BFS) using a double-ended queue.

    BFS visits vertices level-by-level, starting at distance 0, then distance 1,
    then distance 2, and so forth.

    We use `collections.deque` because `deque.popleft()` runs in O(1) time,
    unlike `list.pop(0)` which shifts all elements and takes O(V) time.

    Crucial efficiency note:
    Vertices are added to `visited` at the moment they are ENQUEUED, not when
    dequeued. This prevents the same node from being enqueued multiple times if
    it is reachable via multiple neighbors at the same level.

    Parameters
    ----------
    graph : Graph[T]
        The graph to traverse.
    start : T
        The starting vertex.

    Returns
    -------
    list[T]
        List of vertices in breadth-first level order.

    Raises
    ------
    KeyError
        If the starting vertex does not exist in the graph.
    """
    if not graph.has_vertex(start):
        raise KeyError(f"Start vertex {start!r} does not exist in graph")

    visited: set[T] = {start}
    queue: deque[T] = deque([start])
    order: list[T] = []

    while queue:
        curr = queue.popleft()
        order.append(curr)

        for neighbor in graph.neighbors(curr):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def bfs_shortest_path(graph: Graph[T], start: T, target: T) -> list[T] | None:
    """Find the shortest path (minimum edge count) between start and target in an unweighted graph.

    Important Distinction:
    Traversal visits every reachable node in a systematic order.
    Shortest-path finding asks: "What is the minimum-length sequence of edges
    connecting vertex A to vertex B?"

    Because BFS explores nodes level-by-level in order of their edge distance from
    `start`, the first time BFS encounters `target`, it has found an edge-minimal path.
    We reconstruct the path by tracking parent (predecessor) pointers.

    Parameters
    ----------
    graph : Graph[T]
        The graph to search.
    start : T
        The source vertex.
    target : T
        The destination vertex.

    Returns
    -------
    list[T] | None
        A list of vertices representing the path from start to target,
        or None if target is unreachable from start.

    Raises
    ------
    KeyError
        If either start or target does not exist in the graph.
    """
    if not graph.has_vertex(start):
        raise KeyError(f"Start vertex {start!r} does not exist in graph")
    if not graph.has_vertex(target):
        raise KeyError(f"Target vertex {target!r} does not exist in graph")

    if start == target:
        return [start]

    visited: set[T] = {start}
    queue: deque[T] = deque([start])
    parent: dict[T, T | None] = {start: None}

    found = False
    while queue:
        curr = queue.popleft()
        if curr == target:
            found = True
            break

        for neighbor in graph.neighbors(curr):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = curr
                queue.append(neighbor)
                if neighbor == target:
                    found = True
                    break
        if found:
            break

    if target not in parent:
        return None

    # Reconstruct path by following parent pointers backward from target
    path: list[T] = []
    step: T | None = target
    while step is not None:
        path.append(step)
        step = parent[step]
    path.reverse()
    return path


def find_connected_components(graph: Graph[T]) -> list[list[T]]:
    """Discover all connected components in the graph.

    A single-source BFS or DFS cannot reach vertices in disconnected components.
    To inspect every component, we loop over all vertices in the graph; whenever
    we encounter an unvisited vertex, we run a search from it to discover all
    vertices in its component.

    Parameters
    ----------
    graph : Graph[T]
        The graph to analyze.

    Returns
    -------
    list[list[T]]
        A list of components, where each component is a list of vertices.
    """
    visited: set[T] = set()
    components: list[list[T]] = []

    for vertex in graph.vertices():
        if vertex not in visited:
            # Collect all vertices in this component using DFS
            component_order: list[T] = []
            component_visited: set[T] = set()
            dfs_recursive(
                graph, vertex, visited=component_visited, order=component_order
            )

            visited.update(component_visited)
            components.append(component_order)

    return components


# Alias for component traversal
dfs_all_components = find_connected_components


def has_cycle(graph: Graph[T]) -> bool:
    """Detect whether the graph contains any cycle.

    Cycle definition:
    A cycle is a path that starts and ends at the same vertex with no repeated
    vertices other than the start/end.

    Algorithm:
    - In an undirected graph: a cycle exists if DFS encounters a visited neighbor
      that is NOT the immediate parent vertex that we just came from.
    - In a directed graph: a cycle exists if DFS encounters a vertex that is
      currently being explored on the active recursion stack (a back-edge).

    Handles disconnected graphs by checking every component.

    Parameters
    ----------
    graph : Graph[T]
        The graph to test for cycles.

    Returns
    -------
    bool
        True if the graph contains at least one cycle, False otherwise.
    """
    if graph.order() == 0:
        return False

    if not graph.is_directed:
        # Undirected cycle detection using parent tracking
        visited: set[T] = set()

        def _has_cycle_undirected(u: T, p: T | None) -> bool:
            visited.add(u)
            for v in graph.neighbors(u):
                if v not in visited:
                    if _has_cycle_undirected(v, u):
                        return True
                elif v != p:
                    # Neighbor is already visited and is NOT the direct parent: cycle!
                    return True
            return False

        for node in graph.vertices():
            if node not in visited and _has_cycle_undirected(node, None):
                return True
        return False

    else:
        # Directed cycle detection using 3-state coloring
        # State 0: unvisited
        # State 1: currently visiting (on active recursion stack)
        # State 2: finished visiting
        state: dict[T, int] = {v: 0 for v in graph.vertices()}

        def _has_cycle_directed(u: T) -> bool:
            state[u] = 1  # Mark as visiting
            for v in graph.neighbors(u):
                if state[v] == 1:
                    # Found a back-edge to an active ancestor on the recursion stack!
                    return True
                if state[v] == 0 and _has_cycle_directed(v):
                    return True
            state[u] = 2  # Mark as finished
            return False

        for node in graph.vertices():
            if state[node] == 0 and _has_cycle_directed(node):
                return True
        return False
