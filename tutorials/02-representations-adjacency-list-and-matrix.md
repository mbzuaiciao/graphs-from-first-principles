# Tutorial 2: Graph Representations — Adjacency Lists and Adjacency Matrices

> **Inspiration & Attribution**: This tutorial is inspired by the discussion on storing graphs in Paaras Chand's course presentation on [Graphs](https://paaras.github.io/python_ds/graphs#1).

---

## 1. How Should We Store a Graph in Memory?

When working with a binary tree, storage is straightforward: we define a `TreeNode` class with two explicit pointer attributes, `self.left` and `self.right`.

In a general graph, however:
- A vertex may be connected to $0, 1, 2, \dots,$ or thousands of other vertices.
- The number of connections varies drastically from vertex to vertex.

To store an arbitrary graph, two primary representations have emerged in computer science:
1. **Adjacency List** (the primary, modern standard representation)
2. **Adjacency Matrix** (a 2D grid representation)

Let us examine both from first principles.

---

## 2. Representation 1: The Adjacency List

An **Adjacency List** associates every vertex in the graph with a list (or collection) of its direct neighbors.

In Python, we naturally implement this as a dictionary where:
- Each **key** is a vertex identifier (e.g., `"A"`, `"B"`, or an integer `0`, `1`).
- Each **value** is a sequence of neighboring vertex identifiers.

### Concrete Example
Consider this undirected graph:

```
        (A) --------- (B)
         |             |
         |             |
        (C) --------- (D)
                       |
                      (E)
```

In an adjacency list, we represent this as:

```python
graph = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C", "E"],
    "E": ["D"],
}
```

```
 Vertex (Key)         Neighbors (Value List)
+------------+       +----------------------+
|    "A"     | ----> | ["B", "C"]           |
|    "B"     | ----> | ["A", "D"]           |
|    "C"     | ----> | ["A", "D"]           |
|    "D"     | ----> | ["B", "C", "E"]      |
|    "E"     | ----> | ["D"]                |
+------------+       +----------------------+
```

### Properties of the Adjacency List
- **Space Complexity**: $O(V + E)$.
  - The dictionary stores $V$ keys.
  - For a directed graph, the neighbor lists contain a total of $E$ entries.
  - For an undirected graph, each edge $\{u, v\}$ is stored twice (once in $u$'s list and once in $v$'s list), giving $2E$ total entries.
  - Thus, total memory is proportional to $V + E$.
- **Finding Neighbors of $u$**: Takes $O(\deg(u))$ time (simply return or iterate the list for key $u$).
- **Checking if Edge $(u, v)$ Exists**: Takes $O(\deg(u))$ time using a list, or $O(1)$ average time if neighbor lists are stored as sets or hash tables.
- **Adding a Vertex**: Takes $O(1)$ amortized time (insert key into dictionary).
- **Adding an Edge**: Takes $O(1)$ amortized time (append to the end of the list).

---

## 3. Representation 2: The Adjacency Matrix

An **Adjacency Matrix** represents a graph with $V$ vertices as a 2D square grid $M$ of size $|V| \times |V|$:
- The rows represent source vertices.
- The columns represent destination vertices.
- The cell $M[i][j] = 1$ if there is an edge from vertex $i$ to vertex $j$; otherwise, $M[i][j] = 0$.

### Concrete Example
Using the exact same graph above, ordering vertices alphabetically `["A", "B", "C", "D", "E"]`:

```
        A   B   C   D   E
      +---+---+---+---+---+
    A | 0 | 1 | 1 | 0 | 0 |
      +---+---+---+---+---+
    B | 1 | 0 | 0 | 1 | 0 |
      +---+---+---+---+---+
    C | 1 | 0 | 0 | 1 | 0 |
      +---+---+---+---+---+
    D | 0 | 1 | 1 | 0 | 1 |
      +---+---+---+---+---+
    E | 0 | 0 | 0 | 1 | 0 |
      +---+---+---+---+---+
```

In Python, this is stored as a list of lists:

```python
labels = ["A", "B", "C", "D", "E"]
matrix = [
    [0, 1, 1, 0, 0],  # A
    [1, 0, 0, 1, 0],  # B
    [1, 0, 0, 1, 0],  # C
    [0, 1, 1, 0, 1],  # D
    [0, 0, 0, 1, 0],  # E
]
```

### Properties of the Adjacency Matrix
- **Symmetry**: In an undirected graph, $M[i][j] == M[j][i]$ for all $i, j$. The matrix is completely symmetric across the main diagonal. In a directed graph, the matrix can be asymmetric.
- **Space Complexity**: Always $O(V^2)$, regardless of how few edges exist!
- **Checking if Edge $(u, v)$ Exists**: $O(1)$ instant array lookup: `matrix[index[u]][index[v]] == 1`.
- **Finding Neighbors of $u$**: Requires scanning all $|V|$ columns in row $u$, which takes $O(V)$ time, even if $u$ has only 1 neighbor!
- **Adding a Vertex**: Expensive ($O(V^2)$), because a new row and column must be allocated and previous rows resized.

---

## 4. Side-by-Side Trade-off Comparison

| Operation | Adjacency List | Adjacency Matrix |
| :--- | :--- | :--- |
| **Storage Space** | $\mathbf{O(V + E)}$ (optimal for sparse) | $\mathbf{O(V^2)}$ (wasteful for sparse) |
| **Add Vertex** | $O(1)$ amortized | $O(V^2)$ (reallocate matrix) |
| **Add Edge** | $O(1)$ | $O(1)$ |
| **Check Edge $(u, v)$** | $O(\deg(u))$ (or $O(1)$ with set) | $O(1)$ |
| **Iterate Neighbors of $u$** | $\mathbf{O(\deg(u))}$ (optimal) | $\mathbf{O(V)}$ (must scan entire row) |
| **Symmetry check** | Requires traversal | Check if $M = M^T$ |

---

## 5. When to Choose Which: Sparse vs. Dense Graphs

The ratio of edges to vertices is described by density:
- **Dense Graph**: The number of edges is close to the theoretical maximum $|E| \approx |V|^2$. Every node connects to almost every other node.
- **Sparse Graph**: The number of edges is far smaller than the maximum $|E| \ll |V|^2$. Typically, $|E| \in O(V)$.

### Why the Adjacency List Wins in Practice
Almost all real-world graphs are **sparse**:
- **Social Networks**: A network might have 1,000,000 users ($V = 10^6$). Each user has perhaps 300 friends ($\deg(v) \approx 300$).
  - An **adjacency matrix** requires $V^2 = (10^6)^2 = 10^{12}$ cells. At 1 byte per cell, that requires **1 Terabyte** of RAM!
  - An **adjacency list** stores only $V + 2E \approx 10^6 + 2(300 \times 10^6) \approx 6 \times 10^8$ entries, which easily fits in a few gigabytes of RAM.
- **Road Networks**: Intersections usually connect to 3 or 4 roads ($\deg(v) \le 4$). $E$ is strictly $O(V)$.

For this reason, our tutorials and the module `graphs_from_first_principles` use the **Adjacency List** as the primary data structure.

---

## 6. Check Your Understanding: Exercises

### Exercise 1: Space Comparison
Suppose you are modeling a road network with $V = 10,000$ intersections and $E = 15,000$ roads.
1. How many integers are required to represent this network in an Adjacency Matrix?
2. Approximately how many list elements are stored in an Adjacency List for this undirected graph?

<details>
<summary>View Solution</summary>

1. **Adjacency Matrix**: Size is $|V| \times |V| = 10,000 \times 10,000 = \mathbf{100,000,000}$ cells (100 million).
2. **Adjacency List**: Stores $V$ keys and $2E$ neighbor entries: $10,000 + 2(15,000) = \mathbf{40,000}$ entries. The adjacency list is **2,500 times smaller**!
</details>

### Exercise 2: Matrix to Neighbors
Given the adjacency matrix row for vertex $C$ with index labels `["A", "B", "C", "D", "E"]`:
`[1, 0, 0, 1, 0]`
1. Which vertices are neighbors of $C$?
2. What is the degree of vertex $C$?

<details>
<summary>View Solution</summary>

1. Column 0 corresponds to $A$ (value 1) and Column 3 corresponds to $D$ (value 1). The neighbors of $C$ are **$\{A, D\}$**.
2. The degree of $C$ is the number of 1s in its row: **$2$**.
</details>

---

## Next Steps
Now that you understand the data representation trade-offs, proceed to **[Tutorial 3: Building Graphs in Python](file:///Users/xq/Documents/GitHub/_first-principles/graphs-from-first-principles/tutorials/03-building-a-graph-in-python.md)** to see how to implement an adjacency-list graph class cleanly from scratch.
