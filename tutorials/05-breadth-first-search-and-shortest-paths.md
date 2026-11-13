# Tutorial 5: Breadth-First Search (BFS) and Shortest Paths

> **Inspiration & Attribution**: This tutorial expands on the BFS queue mechanics, level ordering, and comparisons introduced in Paaras Chand's course presentation on [Graphs](https://paaras.github.io/python_ds/graphs#1).

---

## 1. The Intuition Behind Breadth-First Search

If Depth-First Search is like exploring a maze by venturing as deep as possible into one corridor, **Breadth-First Search (BFS)** is like dropping a pebble into water: ripples expand outward equally in all directions.

BFS explores vertices in order of their **distance (edge count)** from the starting vertex:
- First, it visits the starting vertex (distance 0).
- Next, it visits all immediate neighbors of the start (distance 1, Level 1).
- Next, it visits all neighbors of those neighbors (distance 2, Level 2).
- And so on, layer by layer.

```
                     Level 0:       ( Start )
                                     /     \
                     Level 1:      (A)     (B)
                                   / \     / \
                     Level 2:    (C) (D) (E) (F)
```

---

## 2. Why a Queue? The FIFO Principle

To visit nodes level-by-level, we must process nodes in the exact order they were discovered:
- The first nodes discovered must be the first nodes explored.
- This is the **First-In, First-Out (FIFO)** property.
- The fundamental data structure providing FIFO behavior is the **Queue**.

### The Python Pitfall: Why `collections.deque` Matters
In Python, beginners often try to use a standard `list` as a queue:

```python
# AVOID THIS FOR QUEUES:
queue = [start]
curr = queue.pop(0)  # WARNING: O(n) operation!
```

In a Python `list`, elements are stored contiguously in memory. Calling `pop(0)` removes the first element and **shifts every remaining element one index to the left**, which takes **$O(V)$ time**. Doing this $V$ times causes an unintentional $O(V^2)$ slowdown!

Instead, we use `collections.deque` (double-ended queue), implemented as a doubly-linked block list:
- `deque.append(item)` takes **$O(1)$** time.
- `deque.popleft()` takes **$O(1)$** time.

---

## 3. The Critical Enqueue Rule: Mark Visited at Enqueue Time!

One of the most common bugs when implementing BFS is *when* to add a node to the `visited` set.

> [!CAUTION]
> **Common Bug**: Marking visited when popping from the queue.
> If you only mark a node as visited when you **pop** it, two different nodes currently in the queue can both see the same unvisited neighbor and **both enqueue it**.
> On dense graphs, this causes duplicate entries in the queue to blow up exponentially, wasting memory and breaking the $O(V)$ space guarantee!

**The Golden Rule of BFS**:
Add a vertex to `visited` **immediately at the moment it is pushed to the queue**.

---

## 4. BFS Implementation

Here is the BFS implementation from [`src/graphs_from_first_principles/traversals.py`](file:///Users/xq/Documents/GitHub/_first-principles/graphs-from-first-principles/src/graphs_from_first_principles/traversals.py):

```python
from collections import deque


def bfs(graph: Graph[T], start: T) -> list[T]:
    if not graph.has_vertex(start):
        raise KeyError(f"Start vertex {start!r} does not exist in graph")

    # Mark start as visited immediately upon enqueuing
    visited: set[T] = {start}
    queue: deque[T] = deque([start])
    order: list[T] = []

    while queue:
        curr = queue.popleft()
        order.append(curr)

        for neighbor in graph.neighbors(curr):
            if neighbor not in visited:
                visited.add(neighbor)  # Mark immediately!
                queue.append(neighbor)

    return order
```

### Trace Walkthrough
Let us trace BFS on this graph, starting from `A`:

```
        (A) -------- (B)
         |            |
         |            |
        (C) -------- (D)
                      |
                     (E)
```

Neighbors in insertion order:
- `A`: `['B', 'C']`
- `B`: `['A', 'D']`
- `C`: `['A', 'D']`
- `D`: `['B', 'C', 'E']`
- `E`: `['D']`

| Step | Pop `curr` | `queue` State | `visited` Set | `order` List | Action |
| :---: | :---: | :--- | :--- | :--- | :--- |
| Init | — | `['A']` | `{'A'}` | `[]` | Start enqueued |
| 1 | `A` | `[]` | `{'A'}` | `['A']` | Enqueue unvisited neighbors `B`, `C` |
| — | — | `['B', 'C']` | `{'A', 'B', 'C'}` | `['A']` | `B` and `C` marked visited |
| 2 | `B` | `['C']` | `{'A', 'B', 'C'}` | `['A', 'B']` | Enqueue unvisited neighbor `D` |
| — | — | `['C', 'D']` | `{'A', 'B', 'C', 'D'}` | `['A', 'B']` | `D` marked visited |
| 3 | `C` | `['D']` | `{'A', 'B', 'C', 'D'}` | `['A', 'B', 'C']` | Neighbors `A` and `D` already visited |
| 4 | `D` | `[]` | `{'A', 'B', 'C', 'D'}` | `['A', 'B', 'C', 'D']` | Enqueue unvisited neighbor `E` |
| — | — | `['E']` | `{'A', 'B', 'C', 'D', 'E'}`| `['A', 'B', 'C', 'D']` | `E` marked visited |
| 5 | `E` | `[]` | `{'A', 'B', 'C', 'D', 'E'}`| `['A', 'B', 'C', 'D', 'E']` | Neighbor `D` already visited |

Final BFS order: `['A', 'B', 'C', 'D', 'E']`.

Notice how:
- Distance 0 (`A`) was visited first.
- Distance 1 (`B`, `C`) were visited next.
- Distance 2 (`D`) was visited next.
- Distance 3 (`E`) was visited last.

---

## 5. DFS vs. BFS: Side-by-Side Comparison

```
        DFS (Dives Deep)                   BFS (Expands Wide)
               (1)                                (1)
              /   \                              /   \
            (2)   (5)                          (2)   (3)
            /                                  / \
          (3)                                (4) (5)
          /
        (4)
```

| Dimension | Depth-First Search (DFS) | Breadth-First Search (BFS) |
| :--- | :--- | :--- |
| **Exploration Style** | Deep dive down branches; backtrack when stuck | Layer-by-layer wavefront expanding outward |
| **Data Structure** | Stack (Call stack or explicit LIFO list) | Queue (`collections.deque` FIFO) |
| **Shortest Paths?** | No guarantee of shortest path | Guarantees **shortest path in unweighted graphs** |
| **Memory Profile** | Proportional to graph depth (branch length) | Proportional to graph width (level size) |
| **Typical Use Cases** | Topological sorting, maze solving, cycle detection | Fewest-hop routing, social distance (degrees of separation) |

---

## 6. Finding Shortest Paths in Unweighted Graphs

### Traversal vs. Shortest Path: An Essential Distinction
It is critical to distinguish between two different problems:
1. **Graph Traversal**: "Systematically visit every reachable vertex in the graph."
2. **Shortest Path**: "Find the minimum-length sequence of edges from a specific source $S$ to a specific destination $T$."

In an **unweighted graph** (where every edge counts as 1 step), **BFS is guaranteed to find the shortest path**.
Why? Because BFS visits all nodes at distance $k$ before visiting any node at distance $k+1$. Therefore, the very first time BFS encounters target $T$, the path taken to reach $T$ must have the minimum possible number of edges!

### Path Reconstruction Using Parent Pointers
To reconstruct the path, we maintain a `parent` dictionary mapping each node to the predecessor node that discovered it:

```python
def bfs_shortest_path(graph: Graph[T], start: T, target: T) -> list[T] | None:
    if not graph.has_vertex(start) or not graph.has_vertex(target):
        raise KeyError("Start or target vertex not in graph")

    if start == target:
        return [start]

    visited = {start}
    queue = deque([start])
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
        return None  # Unreachable

    # Reconstruct path by following parent pointers backward from target
    path = []
    step = target
    while step is not None:
        path.append(step)
        step = parent[step]
    path.reverse()
    return path
```

### Example
Suppose we have two routes from `S` to `T`:
1. `S -> A -> B -> C -> T` (4 hops)
2. `S -> D -> T` (2 hops)

BFS checks distance 1 (`A`, `D`), then distance 2 (`B`, `T`). Since `T` is found at distance 2 via `D`, BFS terminates immediately and returns `['S', 'D', 'T']`!

---

## 7. Time and Space Complexity Summary

- **Time Complexity**: **$O(V + E)$**.
  - Every vertex is enqueued and dequeued exactly once: $O(V)$.
  - Every edge is checked once (directed) or twice (undirected) across neighbor iterations: $O(E)$.
- **Auxiliary Space Complexity**: **$O(V)$**.
  - The `visited` set holds at most $|V|$ vertices.
  - The `queue` holds at most $|V|$ vertices.

---

## 8. Check Your Understanding: Exercises

### Exercise 1: Why BFS Fails on Weighted Graphs
If an edge from $S$ to $A$ has weight 10, but the path $S \to B \to C \to A$ has weights $1 + 1 + 1 = 3$, which path will unweighted BFS choose? Why?

<details>
<summary>View Solution</summary>

Unweighted BFS will choose the direct edge $S \to A$ because it has only 1 hop, compared to 3 hops for $S \to B \to C \to A$. BFS only minimizes **edge count** (hops), not edge weights. For weighted graphs, Dijkstra's algorithm is required.
</details>

### Exercise 2: Queue Size
In a complete binary tree of depth $h$ with $N$ vertices, what is the maximum number of vertices held in the BFS queue at one time?

<details>
<summary>View Solution</summary>

The leaves at the bottom level make up approximately half of all nodes in the tree: $\approx N / 2$ nodes. Therefore, the BFS queue holds $O(V)$ nodes at its peak.
</details>

---

## Next Steps
Now that you understand both fundamental graph traversals, proceed to **[Tutorial 6: Disconnected Graphs and Components](file:///Users/xq/Documents/GitHub/_first-principles/graphs-from-first-principles/tutorials/06-disconnected-graphs-and-components.md)** to see what happens when a graph is split into separate pieces.
