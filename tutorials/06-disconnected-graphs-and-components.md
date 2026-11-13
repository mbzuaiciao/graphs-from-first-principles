# Tutorial 6: Disconnected Graphs and Connected Components

> **Inspiration & Attribution**: This tutorial expands on the "Graphs in more than one piece" concept presented in Paaras Chand's course presentation on [Graphs](https://paaras.github.io/python_ds/graphs#1).

---

## 1. The Single-Source Traversal Blindspot

In Tutorials 4 and 5, our DFS and BFS functions were **single-source traversals**: they accepted a single `start` vertex and followed edges outward.

Now consider the following graph:

```
        Component 1               Component 2         Component 3 (Isolated)
     (A) ---------- (B)            (X) --- (Y)                 (Z)
      |              |
     (C) ---------- (D)
```

What happens if you run `bfs(graph, "A")` or `dfs_recursive(graph, "A")`?
- The traversal visits `A`, `B`, `C`, and `D`.
- But it **never visits `X`, `Y`, or `Z`**!

Why? Because there is no sequence of edges connecting component 1 to component 2 or vertex 3. A single-source traversal is blind to disconnected parts of a graph.

---

## 2. Connected Components Defined

In an undirected graph, a **connected component** (or simply **component**) is a maximal subgraph in which any two vertices are connected to each other by a path, and no vertex in the subgraph is connected to any vertex outside the subgraph.

In the diagram above:
- **Component 1**: $\{A, B, C, D\}$
- **Component 2**: $\{X, Y\}$
- **Component 3**: $\{Z\}$ (an isolated vertex of degree 0 forms its own component of size 1)

If a graph has only 1 connected component, it is called a **connected graph**.
If a graph has 2 or more connected components, it is a **disconnected graph**.

---

## 3. The Outer Loop Pattern: Visiting Every Piece

To guarantee that we visit every vertex in a disconnected graph, we wrap our traversal in an **outer loop** that iterates through every vertex registered in the graph:

1. Maintain a global `visited` set across all components.
2. For each vertex $v \in V$:
   - If $v$ is already in `visited`, skip it (it belongs to a component we already explored).
   - If $v$ is not in `visited`, $v$ is the start of a **new, unexplored component**!
   - Run DFS or BFS starting from $v$ to discover all vertices belonging to this component.
   - Add all discovered vertices to `visited`.

```
                    Iterate all vertices in graph
                                 |
                     Is vertex in visited set?
                                / \
                         Yes   /   \   No
                              /     \
                           Skip     Start new traversal (DFS/BFS)
                                    Collect all reachable nodes
                                    Add component to results
```

---

## 4. Implementation

Here is the implementation from [`src/graphs_from_first_principles/traversals.py`](file:///Users/xq/Documents/GitHub/_first-principles/graphs-from-first-principles/src/graphs_from_first_principles/traversals.py):

```python
def find_connected_components(graph: Graph[T]) -> list[list[T]]:
    """Discover all connected components in an undirected graph."""
    visited: set[T] = set()
    components: list[list[T]] = []

    for vertex in graph.vertices():
        if vertex not in visited:
            component_order: list[T] = []
            component_visited: set[T] = set()

            # Explore all nodes reachable from this vertex
            dfs_recursive(
                graph, vertex, visited=component_visited, order=component_order
            )

            # Record this component and update global visited set
            visited.update(component_visited)
            components.append(component_order)

    return components
```

---

## 5. Walkthrough of a Multi-Component Graph

Let us build the 3-component graph shown in Section 1 and run `find_connected_components`:

```python
from graphs_from_first_principles import Graph, find_connected_components

g = Graph[str](directed=False)

# Component 1
g.add_edge("A", "B")
g.add_edge("B", "D")
g.add_edge("D", "C")
g.add_edge("C", "A")

# Component 2
g.add_edge("X", "Y")

# Component 3: Isolated vertex
g.add_vertex("Z")

components = find_connected_components(g)
print(f"Total components: {len(components)}")
for i, comp in enumerate(components, 1):
    print(f"Component {i}: {comp}")
```

### Execution Trace:
1. `graph.vertices()` returns `['A', 'B', 'D', 'C', 'X', 'Y', 'Z']`.
2. `vertex = 'A'`: Not in `visited`.
   - Run DFS from `'A'`. Discovers `['A', 'B', 'D', 'C']`.
   - Add to `components`. `visited = {'A', 'B', 'D', 'C'}`.
3. `vertex = 'B'`: In `visited` $\to$ skip.
4. `vertex = 'D'`: In `visited` $\to$ skip.
5. `vertex = 'C'`: In `visited` $\to$ skip.
6. `vertex = 'X'`: Not in `visited`.
   - Run DFS from `'X'`. Discovers `['X', 'Y']`.
   - Add to `components`. `visited = {'A', 'B', 'D', 'C', 'X', 'Y'}`.
7. `vertex = 'Y'`: In `visited` $\to$ skip.
8. `vertex = 'Z'`: Not in `visited`.
   - Run DFS from `'Z'`. Neighbors are `[]`. Discovers `['Z']`.
   - Add to `components`. `visited = {'A', 'B', 'D', 'C', 'X', 'Y', 'Z'}`.

Output:
```
Total components: 3
Component 1: ['A', 'B', 'D', 'C']
Component 2: ['X', 'Y']
Component 3: ['Z']
```

Every single vertex, isolated or connected, is visited exactly once!

---

## 6. Time and Space Complexity

Even with the outer loop, the overall time complexity remains **$O(V + E)$**:
- The outer loop executes $|V|$ iterations.
- Each vertex is explored by DFS at most once across all components.
- Each edge is inspected at most twice (undirected).
- Space complexity is **$O(V)$** to store the global `visited` set and the returned components.

---

## 7. Check Your Understanding: Exercises

### Exercise 1: Edge Bound in Connected Graphs
What is the minimum number of edges an undirected graph with $V$ vertices must have to be connected?

<details>
<summary>View Solution</summary>

A connected undirected graph with $V$ vertices must have at least **$V - 1$ edges**. An undirected acyclic connected graph with $V - 1$ edges is a tree. If $|E| < V - 1$, the graph is guaranteed to be disconnected with at least 2 components.
</details>

### Exercise 2: Isolated Nodes
If a graph has $V = 10$ vertices and $E = 0$ edges, how many connected components does it have?

<details>
<summary>View Solution</summary>

It has **10 connected components**. Each isolated vertex is its own connected component of size 1.
</details>

---

## Next Steps
Now that you have traversed both single components and disconnected graphs, conclude with **[Tutorial 7: Complexity Analysis from First Principles](file:///Users/xq/Documents/GitHub/_first-principles/graphs-from-first-principles/tutorials/07-complexity-analysis-first-principles.md)** for a rigorous mathematical derivation of graph algorithm time and space bounds.
