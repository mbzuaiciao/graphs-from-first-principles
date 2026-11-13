# Tutorial 3: Building a Graph in Python

> **Inspiration & Attribution**: This tutorial expands on the `Graph` class construction presented in Paaras Chand's course presentation on [Graphs](https://paaras.github.io/python_ds/graphs#1).

---

## 1. Class Design Choices

When implementing a graph in Python, learners often wonder: *Should I create a `Node` class with pointers, just like a binary tree?*

In a binary tree, a `TreeNode` class is helpful because each node holds exactly two named pointers: `left` and `right`. But in a graph:
- A node has no fixed number of pointers.
- Nodes are frequently identified simply by names, IDs, strings, or numbers (e.g., `"New York"`, `42`, `"user_102"`).

Therefore, a cleaner and more Pythonic approach is to store the graph in a single `Graph` class backed by an internal **adjacency dictionary**:

```python
self._adj: dict[T, list[T]] = {}
```

Every vertex is a dictionary key, and its associated value is a list of its neighboring vertices.

---

## 2. Implementing the Core Graph Class

Let us examine the architecture of the `Graph` class from [`src/graphs_from_first_principles/graph.py`](file:///Users/xq/Documents/GitHub/_first-principles/graphs-from-first-principles/src/graphs_from_first_principles/graph.py).

### 2.1 Initialization
The class supports both undirected (default) and directed modes:

```python
from typing import Generic, Hashable, TypeVar

T = TypeVar("T", bound=Hashable)


class Graph(Generic[T]):
    def __init__(self, directed: bool = False) -> None:
        self._directed: bool = directed
        self._adj: dict[T, list[T]] = {}
```

### 2.2 Adding Vertices
An isolated vertex can exist in a graph without any edges incident to it. `add_vertex` ensures the vertex is registered as a key with an empty list:

```python
def add_vertex(self, vertex: T) -> None:
    if vertex not in self._adj:
        self._adj[vertex] = []
```

### 2.3 Adding Edges
When adding an edge between `u` and `v`:
1. We ensure both `u` and `v` exist in the graph (auto-creating them if needed).
2. We append `v` to `u`'s neighbor list.
3. If the graph is **undirected**, we also append `u` to `v`'s neighbor list!

```python
def add_edge(self, u: T, v: T) -> None:
    self.add_vertex(u)
    self.add_vertex(v)

    # Avoid duplicate edges to maintain a simple graph
    if v not in self._adj[u]:
        self._adj[u].append(v)

    # If undirected, the connection is bidirectional
    if not self._directed:
        if u not in self._adj[v]:
            self._adj[v].append(u)
```

> [!TIP]
> **Deterministic Neighbor Ordering**:
> Python 3.7+ guarantees that dictionary keys and list appends preserve insertion order. By appending neighbors in the order edges are added, neighbor lookups and subsequent traversals are completely deterministic. This makes tests reproducible and algorithm traces predictable.

### 2.4 Querying Neighbors and Degree
To examine neighbors safely, we return a defensive copy so external callers cannot mutate internal state:

```python
def neighbors(self, vertex: T) -> list[T]:
    if vertex not in self._adj:
        raise KeyError(f"Vertex {vertex!r} not in graph")
    return list(self._adj[vertex])


def degree(self, vertex: T) -> int:
    return len(self.neighbors(vertex))
```

### 2.5 Converting to an Adjacency Matrix
For visual inspection or linear-algebraic analysis, our class can export the adjacency matrix:

```python
def to_adjacency_matrix(self) -> tuple[list[list[int]], list[T]]:
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
```

---

## 3. Step-by-Step Code Walkthrough

Let us build and inspect a graph of four friends: Alice, Bob, Charlie, and Diana, plus an isolated user Evan.

```python
from graphs_from_first_principles import Graph

# 1. Create an undirected graph
social_graph = Graph[str](directed=False)

# 2. Add friendships
social_graph.add_edge("Alice", "Bob")
social_graph.add_edge("Alice", "Charlie")
social_graph.add_edge("Bob", "Diana")
social_graph.add_edge("Charlie", "Diana")

# 3. Add an isolated user (no friendships yet)
social_graph.add_vertex("Evan")

# 4. Verify properties
print("Vertices:", social_graph.vertices())
# Output: ['Alice', 'Bob', 'Charlie', 'Diana', 'Evan']

print("Alice's friends:", social_graph.neighbors("Alice"))
# Output: ['Bob', 'Charlie']

print("Bob's degree:", social_graph.degree("Bob"))
# Output: 2

print("Evan's degree:", social_graph.degree("Evan"))
# Output: 0

# 5. Adjacency Matrix
matrix, labels = social_graph.to_adjacency_matrix()
print("Labels:", labels)
for row in matrix:
    print(row)
```

Output matrix:
```
Labels: ['Alice', 'Bob', 'Charlie', 'Diana', 'Evan']
[0, 1, 1, 0, 0]  # Alice
[1, 0, 0, 1, 0]  # Bob
[1, 0, 0, 1, 0]  # Charlie
[0, 1, 1, 0, 0]  # Diana
[0, 0, 0, 0, 0]  # Evan
```

Notice that the matrix is symmetric and Evan's row and column are completely zeros.

---

## 4. Directed Mode in Action

Now let us see what happens when `directed=True`:

```python
web = Graph[str](directed=True)
web.add_edge("PageA", "PageB")  # Link from PageA to PageB

print("Outgoing from PageA:", web.neighbors("PageA"))
# Output: ['PageB']

print("Outgoing from PageB:", web.neighbors("PageB"))
# Output: []

print("PageB in-degree:", web.in_degree("PageB"))
# Output: 1

print("PageB out-degree:", web.out_degree("PageB"))
# Output: 0
```

Because this is a directed graph, adding `(PageA, PageB)` only registers `PageB` as a neighbor of `PageA`.

---

## 5. Check Your Understanding: Exercises

### Exercise 1: Edge Addition
In an undirected graph, how many times is a list append executed when `add_edge("X", "Y")` is called for the first time? What about in a directed graph?

<details>
<summary>View Solution</summary>

- **Undirected graph**: 2 appends occur (appending `"Y"` to `_adj["X"]` and `"X"` to `_adj["Y"]`).
- **Directed graph**: 1 append occurs (appending `"Y"` to `_adj["X"]`).
</details>

### Exercise 2: Self-Loops
What happens when you call `add_edge("A", "A")` in this implementation?
1. Does it create a self-loop?
2. What will `neighbors("A")` contain?

<details>
<summary>View Solution</summary>

1. Yes, it creates a self-loop edge from vertex `"A"` to itself.
2. In our implementation, `add_edge("A", "A")` adds `"A"` to `_adj["A"]`. The second check `if u not in self._adj[v]` sees that `"A"` is already in `_adj["A"]`, so `neighbors("A")` returns `["A"]` without duplicating the entry.
</details>

---

## Next Steps
Now that we have a fully functional graph data structure, proceed to **[Tutorial 4: Depth-First Search (DFS)](file:///Users/xq/Documents/GitHub/_first-principles/graphs-from-first-principles/tutorials/04-depth-first-search.md)** to learn how to traverse graph connections systematically.
