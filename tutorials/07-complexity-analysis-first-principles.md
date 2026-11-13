# Tutorial 7: Complexity Analysis from First Principles

> **Inspiration & Attribution**: This tutorial expands on the time and space complexity analysis presented in Paaras Chand's course presentation on [Graphs](https://paaras.github.io/python_ds/graphs#1).

---

## 1. Why Do Graph Algorithms Use Two Variables: $V$ and $E$?

When analyzing algorithms on arrays, we describe runtime with a single variable: $N$, the length of the array.

In graphs, however, two graphs with the exact same number of vertices $|V|$ can have drastically different numbers of edges $|E|$:
- A graph with $V = 1,000$ isolated vertices has **$E = 0$ edges**.
- A graph with $V = 1,000$ vertices where every vertex is connected to every other vertex (a complete graph $K_V$) has:
  $$E = \frac{V(V - 1)}{2} = \frac{1,000 \times 999}{2} = 499,500 \text{ edges!}$$

Because $E$ can range from $0$ all the way to $\Theta(V^2)$, a single parameter cannot describe graph performance. We must express both time and space in terms of both $|V|$ (the number of vertices) and $|E|$ (the number of edges).

---

## 2. Deriving the Time Complexity of DFS and BFS: $O(V + E)$

Why does traversing an adjacency list with DFS or BFS take exactly **$O(V + E)$** time? Let us dissect the work into its two fundamental components:
1. **Vertex Work**
2. **Edge Work**

```
Total Time = (Work spent per vertex) + (Work spent per edge)
```

### Component 1: Vertex Work
- In both BFS and DFS, every vertex enters the `visited` set at most once.
- In DFS, a vertex generates at most one recursive function call (or one `stack.pop()`).
- In BFS, a vertex is appended to the `queue` and popped with `popleft()` at most once.
- Inside each vertex visit, operations such as checking `visited`, appending to `order`, and marking the vertex take $O(1)$ time.
- Across all $|V|$ vertices, the vertex overhead is:
  $$\sum_{v \in V} O(1) = \mathbf{O(V)}$$

### Component 2: Edge Work (The Handshaking Lemma)
Inside the traversal loop for vertex $u$, the algorithm iterates through each neighbor $v \in \text{neighbors}(u)$:

```python
for neighbor in graph.neighbors(curr):
    if neighbor not in visited:
        ...
```

The loop runs $\deg(u)$ times for vertex $u$. Over the entire course of the traversal, what is the total number of iterations across all vertices?

- In a **directed graph**, each edge $(u, v)$ leaves vertex $u$ and appears in exactly one neighbor list. Thus:
  $$\sum_{v \in V} \text{out-deg}(v) = |E|$$
- In an **undirected graph**, each edge $\{u, v\}$ connects two vertices and appears in two neighbor lists (once in $u$'s list and once in $v$'s list). By the **Handshaking Lemma**:
  $$\sum_{v \in V} \deg(v) = 2|E|$$

In both cases, the total number of neighbor loop iterations over the entire traversal is proportional to $|E|$:
$$\sum_{v \in V} O(\deg(v)) = \mathbf{O(E)}$$

### Combining the Two:
$$\text{Total Time} = O(V) + O(E) = \mathbf{O(V + E)}$$

> [!IMPORTANT]
> **Can We Simplify $O(V + E)$ to Just $O(E)$ or $O(V)$?**
> **No!**
> - If the graph is sparse or has many isolated vertices ($E = 0$), $O(V + E) = O(V)$. If you only counted edges ($O(E)$), you would predict zero time, ignoring the time spent initializing and checking vertices!
> - If the graph is dense ($E \approx V^2$), $O(V + E) = O(V^2)$.
> Keeping both terms accounts for all graph densities accurately.

---

## 3. What Happens with an Adjacency Matrix?

What if we performed BFS or DFS using an **Adjacency Matrix** instead of an Adjacency List?

In an adjacency matrix, finding the neighbors of vertex $u$ requires scanning row $u$ across all $|V|$ columns to find which entries are `1`:

```python
# Neighbor lookup in an Adjacency Matrix:
for v in range(num_vertices):
    if matrix[u][v] == 1:
        ...
```

For every single vertex $u$, scanning the row takes $O(V)$ time.
Across all $|V|$ vertices:
$$\sum_{v \in V} O(V) = \mathbf{O(V^2)}$$

Even if the graph has **zero edges**, an adjacency-matrix traversal must inspect all $V^2$ cells in the matrix!
This illustrates why the Adjacency List's $O(V + E)$ runtime is strictly superior for sparse and real-world graphs.

---

## 4. Deriving Space Complexity from First Principles

Space complexity divides into two parts:
1. **Graph Representation Storage**
2. **Auxiliary Search Memory** (data structures used during traversal)

### 4.1 Representation Storage
- **Adjacency List**:
  - The dictionary stores $|V|$ keys.
  - The neighbor lists store $2|E|$ items (undirected) or $|E|$ items (directed).
  - Storage space: **$O(V + E)$**.
- **Adjacency Matrix**:
  - A 2D array of size $|V| \times |V|$.
  - Storage space: **$O(V^2)$**, regardless of how many edges exist.

### 4.2 Auxiliary Traversal Space
During traversal, the algorithm allocates memory for:
1. **The `visited` Set**: Stores at most $|V|$ vertices $\to \mathbf{O(V)}$.
2. **The Output Order List**: Stores at most $|V|$ vertices $\to \mathbf{O(V)}$.
3. **The Call Stack or Queue**:
   - In **DFS**, the call stack depth equals the length of the current exploration path.
     - Worst case: A linear graph ($1 - 2 - 3 - \dots - V$) creates a recursion stack of depth $|V| \to \mathbf{O(V)}$.
     - Best case: A star graph (one central hub connected to $V-1$ leaves) has recursion stack depth $1 \to O(1)$.
   - In **BFS**, the queue holds the frontier of vertices at the current distance.
     - Worst case: A star graph where the center node enqueues all $V-1$ neighbors $\to \mathbf{O(V)}$.
     - Best case: A linear graph where each level has only 1 vertex $\to O(1)$.

In all cases, neither the stack nor the queue can ever hold more than $|V|$ vertices simultaneously. Therefore, the worst-case auxiliary space for both BFS and DFS is **$O(V)$**.

---

## 5. Summary Reference Table

| Operation / Metric | Adjacency List | Adjacency Matrix | Notes |
| :--- | :--- | :--- | :--- |
| **Storage Space** | $\mathbf{O(V + E)}$ | $\mathbf{O(V^2)}$ | List is vastly superior for sparse graphs |
| **Add Vertex** | $O(1)$ amortized | $O(V^2)$ | Matrix must reallocate grid |
| **Add Edge** | $O(1)$ | $O(1)$ | Direct cell update in matrix |
| **Check Edge $(u, v)$** | $O(\deg(u))$ | $\mathbf{O(1)}$ | Matrix wins on direct edge lookup |
| **List Neighbors of $u$** | $\mathbf{O(\deg(u))}$ | $O(V)$ | List only iterates actual neighbors |
| **DFS Time** | $\mathbf{O(V + E)}$ | $O(V^2)$ | List is optimal across all components |
| **BFS Time** | $\mathbf{O(V + E)}$ | $O(V^2)$ | List is optimal across all components |
| **Traversal Auxiliary Space** | $\mathbf{O(V)}$ | $\mathbf{O(V)}$ | For visited set + stack/queue |

---

## 6. Check Your Understanding: Exercises

### Exercise 1: Dense Graph Equivalence
For a complete graph $K_V$ where every pair of vertices is connected by an edge ($E = \frac{V(V-1)}{2}$), what is the time complexity of adjacency-list DFS in terms of $V$ alone?

<details>
<summary>View Solution</summary>

Substitute $E = \frac{V(V-1)}{2} = \Theta(V^2)$ into $O(V + E)$:
$$O(V + E) = O\left(V + \frac{V(V-1)}{2}\right) = \mathbf{O(V^2)}$$
On dense graphs, an adjacency-list traversal and an adjacency-matrix traversal take the same asymptotic time $\Theta(V^2)$.
</details>

### Exercise 2: Space Extremes
Consider two graphs:
1. **Graph A (Linear chain)**: $1 - 2 - 3 - \dots - V$.
2. **Graph B (Star graph)**: Center node $0$ connected to leaves $1, 2, \dots, V-1$.

For each graph, which search (DFS or BFS) uses more auxiliary memory for its stack/queue?

<details>
<summary>View Solution</summary>

- **Graph A (Linear chain)**:
  - DFS stack grows to depth $V$ ($O(V)$ space).
  - BFS queue never holds more than 1 node at any time ($O(1)$ queue space).
  - *BFS is much more memory-efficient on linear chains.*
- **Graph B (Star graph)**:
  - DFS visits the center, then visits leaf 1, backtracks immediately, visits leaf 2, etc. Stack depth is at most 2 ($O(1)$ stack space).
  - BFS visits the center and immediately enqueues all $V-1$ leaves ($O(V)$ queue space).
  - *DFS is much more memory-efficient on star graphs.*
</details>

---

## Conclusion
You have now explored graph fundamentals completely from first principles:
1. Mental models from trees to general graphs.
2. Adjacency list and matrix representations and trade-offs.
3. Clean, typed Python implementation with deterministic ordering.
4. Depth-First Search with visited sets and recursion stack dynamics.
5. Breadth-First Search with FIFO queues and shortest unweighted paths.
6. Disconnected component traversal.
7. Rigorous $O(V + E)$ time and $O(V)$ space complexity derivations.

Check the project [README.md](file:///Users/xq/Documents/GitHub/_first-principles/graphs-from-first-principles/README.md) for instructions on running the test suite and interactive demos!
