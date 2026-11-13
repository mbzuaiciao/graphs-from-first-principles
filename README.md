# Graphs from First Principles

> An original, accessible, from-first-principles educational curriculum and tested Python implementation of graph data structures, traversals, and asymptotic complexity analysis.
>
> **Inspiration & Attribution**: This repository is inspired by the topic progression in Paaras Chand's course presentation on [Graphs](https://paaras.github.io/python_ds/graphs#1). All explanations, code implementations, diagrams, worked examples, and tests in this repository are original instructional materials designed for students learning Python data structures.

---

## Learning Goals

By completing this curriculum, you will understand:
1. **The Mental Shift from Trees to Graphs**: How general graphs generalize binary trees by dropping the root constraint, permitting arbitrary node degrees, and introducing cycles.
2. **Directed vs. Undirected Graphs**: Modeling symmetric relationships (friendships, two-way roads) versus asymmetric relationships (social follows, hyperlinks, prerequisites).
3. **Graph Storage Representations**: Why the **Adjacency List** ($O(V + E)$) is the standard for real-world sparse graphs, and how it contrasts with the **Adjacency Matrix** ($O(V^2)$).
4. **Depth-First Search (DFS)**: Both recursive and stack-based iterative DFS, why cycles necessitate a `visited` set with $O(1)$ lookup, and how DFS detects cycles.
5. **Breadth-First Search (BFS)**: Level-by-level exploration using `collections.deque`, why marking visited at enqueue time is critical, and why BFS guarantees the **shortest path in unweighted graphs**.
6. **Disconnected Graphs**: Overcoming the single-source traversal blindspot by using an outer component loop to discover every disconnected piece.
7. **Complexity from First Principles**: Mathematical derivations of $O(V + E)$ time (Handshaking Lemma and degree sum) and $O(V)$ auxiliary space.

---

## Tutorial Curriculum

The tutorial series is designed to be read in order without missing prerequisites:

| Chapter | Title | Key Topics Covered |
| :--- | :--- | :--- |
| **01** | [Foundations: From Trees to Graphs](tutorials/01-foundations-trees-to-graphs.md) | Trees vs graphs, vertices, edges, neighbors, degree, directed vs undirected, walks, paths, cycles, Handshaking Lemma. |
| **02** | [Graph Representations](tutorials/02-representations-adjacency-list-and-matrix.md) | Adjacency list ($O(V+E)$) vs adjacency matrix ($O(V^2)$), sparse vs dense networks, trade-off matrix. |
| **03** | [Building Graphs in Python](tutorials/03-building-a-graph-in-python.md) | Clean `Graph` class implementation, adding vertices/edges, deterministic neighbor ordering, degrees, matrix export. |
| **04** | [Depth-First Search (DFS)](tutorials/04-depth-first-search.md) | The maze intuition, cycle traps, `visited` set, recursive DFS, iterative DFS with explicit stack, cycle detection. |
| **05** | [Breadth-First Search & Shortest Paths](tutorials/05-breadth-first-search-and-shortest-paths.md) | Ripple intuition, FIFO queue, `collections.deque` ($O(1)$ vs $O(n)$), mark-at-enqueue rule, unweighted shortest paths. |
| **06** | [Disconnected Graphs & Components](tutorials/06-disconnected-graphs-and-components.md) | The single-source blindspot, connected components, outer-loop pattern, discovering isolated vertices. |
| **07** | [Complexity Analysis from First Principles](tutorials/07-complexity-analysis-first-principles.md) | Why $O(V + E)$, Handshaking Lemma proof, vertex vs edge work breakdown, space complexity (stack vs queue bounds). |

---

## Repository Structure

```
graphs-from-first-principles/
├── README.md                                   # Curriculum guide & quickstart
├── pyproject.toml                              # Minimal package configuration with pytest
├── src/
│   └── graphs_from_first_principles/
│       ├── __init__.py                         # Public API exports
│       ├── graph.py                            # Graph class (adjacency list, matrix export)
│       └── traversals.py                       # DFS, BFS, shortest path, components, cycles
├── tutorials/                                  # 7 step-by-step Markdown tutorials
│   ├── 01-foundations-trees-to-graphs.md
│   ├── 02-representations-adjacency-list-and-matrix.md
│   ├── 03-building-a-graph-in-python.md
│   ├── 04-depth-first-search.md
│   ├── 05-breadth-first-search-and-shortest-paths.md
│   ├── 06-disconnected-graphs-and-components.md
│   └── 07-complexity-analysis-first-principles.md
├── tests/
│   ├── __init__.py
│   ├── test_graph.py                           # Tests for Graph class, edges, and matrix
│   └── test_traversals.py                      # Tests for DFS, BFS, shortest path, cycles
└── examples/
    └── demo.py                                 # Interactive terminal walkthrough script
```

---

## Getting Started

### Prerequisites
- Python 3.10+ (tested on Python 3.12, 3.13, and 3.15)
- [`uv`](https://github.com/astral-sh/uv) (recommended) or standard Python `venv` + `pip`

### 1. Installation

Using `uv` (automatic environment management):
```bash
# Clone the repository
git clone https://github.com/mbzuaiciao/graphs-from-first-principles.git
cd graphs-from-first-principles

# Sync dependencies and development tools
uv sync
```

Alternatively, using standard Python `venv`:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

---

## Running the Examples and Tests

### Run the Interactive Terminal Demo
To see the graph data structure, adjacency matrix, DFS, BFS, unweighted shortest paths, and disconnected component discovery in action:

```bash
uv run python -m examples.demo
```
*(Or `python -m examples.demo` if inside an activated virtual environment).*

### Run the Test Suite
The repository includes 24 focused tests covering directed/undirected edges, isolated vertices, cycles, disconnected graphs, DFS/BFS ordering, and error states:

```bash
uv run pytest
```
*(Or `pytest` if inside an activated virtual environment).*

Expected output:
```text
============================== test session starts ==============================
collected 24 items

tests/test_graph.py ............                                         [ 50%]
tests/test_traversals.py ............                                    [100%]

============================== 24 passed in 0.02s ===============================
```

---

## Quick Code Examples

### 1. Building a Graph
```python
from graphs_from_first_principles import Graph

# Create an undirected graph
g = Graph[str](directed=False)

# Add edges (vertices are automatically registered)
g.add_edge("A", "B")
g.add_edge("A", "C")
g.add_edge("B", "D")

# Add an isolated vertex
g.add_vertex("E")

print(g.vertices())  # ['A', 'B', 'C', 'D', 'E']
print(g.neighbors("A"))  # ['B', 'C']
print(g.degree("A"))  # 2
```

### 2. Depth-First Search vs. Breadth-First Search
```python
from graphs_from_first_principles import dfs_recursive, bfs

# DFS dives deep first:
print(dfs_recursive(g, "A"))  # ['A', 'B', 'D', 'C']

# BFS expands level by level:
print(bfs(g, "A"))  # ['A', 'B', 'C', 'D']
```

### 3. Finding the Shortest Unweighted Path
```python
from graphs_from_first_principles import bfs_shortest_path

# Add an alternative path to D
g.add_edge("A", "D")

# BFS finds the path with the minimum number of edges
path = bfs_shortest_path(g, "A", "D")
print(path)  # ['A', 'D'] (1 edge instead of A -> B -> D with 2 edges)
```

### 4. Discovering All Disconnected Components
```python
from graphs_from_first_principles import find_connected_components

# Returns all components, including isolated vertex 'E'
components = find_connected_components(g)
print(components)
# [['A', 'B', 'D', 'C'], ['E']]
```

---

## Pedagogical Highlights

- **Deterministic Neighbor Ordering**: To ensure reproducible traversals and reliable testing, adjacency lists preserve edge insertion order.
- **Mark-at-Enqueue in BFS**: Explicitly documents and enforces marking vertices as visited upon enqueue rather than dequeue, preventing exponential queue duplicate explosions.
- **Traversal vs. Shortest Path**: Highlights the conceptual boundary between systematically traversing a graph and finding optimal paths.
- **Zero Production Dependencies**: Clean, pure-Python implementation using standard library `collections.deque` and type annotations.

---

## Remaining Scope & Limitations

In accordance with the project scope:
- **Unweighted Graphs Only**: Algorithms in this repository minimize edge count (hops). Weighted shortest paths (e.g., Dijkstra's algorithm, Bellman-Ford) and Minimum Spanning Trees (Prim's, Kruskal's) are out of scope.
- **Simple Graphs**: Multigraphs with parallel edges between the same vertex pair are deduplicated.
- **No GUI / Web Frontend**: This repository focuses purely on the algorithmic and data structure core. An interactive frontend is tracked separately in a future milestone.
