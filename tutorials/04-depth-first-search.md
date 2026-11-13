# Tutorial 4: Depth-First Search (DFS)

> **Inspiration & Attribution**: This tutorial expands on the DFS concepts, visited sets, and recursion mechanics introduced in Paaras Chand's course presentation on [Graphs](https://paaras.github.io/python_ds/graphs#1).

---

## 1. The Intuition Behind Depth-First Search

Imagine exploring an unfamiliar maze. When you reach an intersection, you pick one path and follow it as deep as you can. If you hit a dead end, you backtrack to the most recent intersection and try the next unexplored path.

This strategy is known as **Depth-First Search (DFS)**:
- From the current vertex, move to the first unvisited neighbor.
- Repeat this recursively until reaching a vertex with no unvisited neighbors.
- Backtrack to the previous vertex and explore its remaining unvisited neighbors.

---

## 2. Why Naive Recursion Fails on Graphs: Cycles

When traversing a binary tree, you can write:

```python
def print_tree(node):
    if node is None:
        return
    print(node.val)
    print_tree(node.left)
    print_tree(node.right)
```

In a tree, this recursion always finishes because you are always moving downward away from the root toward leaves. There are **no loops**.

Now consider what happens if you try naive recursion on a graph:

```
        (A) -------- (B)
         |            |
         |            |
        (D) -------- (C)
```

If you start at `A`:
1. `A` calls its neighbor `B`.
2. `B` calls its neighbor `C`.
3. `C` calls its neighbor `D`.
4. `D` calls its neighbor `A`!
5. `A` calls `B` again...

Because the graph contains a **cycle**, the naive function loops forever until Python crashes with `RecursionError: maximum recursion depth exceeded`.

---

## 3. The Remedy: Remembering Where We Have Been

To prevent infinite loops, we maintain a **`visited` set**.
- Before visiting any neighbor, we check if it is already in `visited`.
- If it is in `visited`, we skip it.
- If it is not, we mark it as visited and recurse.

### Why a `set` Instead of a `list`?
In Python, checking `item in visited_list` takes **$O(n)$** time because Python must scan the list sequentially.
Checking `item in visited_set` takes **$O(1)$** amortized time because sets use a hash table.
Using a `set` ensures that our traversal remains efficient.

---

## 4. Recursive DFS Implementation

Here is the recursive DFS implementation from [`src/graphs_from_first_principles/traversals.py`](file:///Users/xq/Documents/GitHub/_first-principles/graphs-from-first-principles/src/graphs_from_first_principles/traversals.py):

```python
def dfs_recursive(
    graph: Graph[T],
    start: T,
    visited: set[T] | None = None,
    order: list[T] | None = None,
) -> list[T]:
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
```

### Trace Walkthrough
Let us trace `dfs_recursive` on this 5-node graph, starting at `A`:

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

| Step | Current Node | `visited` Set | `order` List | Action |
| :---: | :---: | :--- | :--- | :--- |
| 1 | `A` | `{'A'}` | `['A']` | Inspect neighbor `B` (unvisited) $\to$ recurse to `B` |
| 2 | `B` | `{'A', 'B'}` | `['A', 'B']` | Neighbor `A` is visited. Inspect `D` (unvisited) $\to$ recurse to `D` |
| 3 | `D` | `{'A', 'B', 'D'}` | `['A', 'B', 'D']` | Neighbor `B` is visited. Inspect `C` (unvisited) $\to$ recurse to `C` |
| 4 | `C` | `{'A', 'B', 'D', 'C'}` | `['A', 'B', 'D', 'C']` | Neighbor `A` is visited. Neighbor `D` is visited. No unvisited neighbors $\to$ backtrack to `D` |
| 5 | `D` | `{'A', 'B', 'D', 'C'}` | `['A', 'B', 'D', 'C']` | Inspect next neighbor `E` (unvisited) $\to$ recurse to `E` |
| 6 | `E` | `{'A', 'B', 'D', 'C', 'E'}` | `['A', 'B', 'D', 'C', 'E']` | Neighbor `D` is visited. No unvisited neighbors $\to$ backtrack to `D` |
| 7 | `D` | ... | ... | Finished all neighbors $\to$ backtrack to `B` |
| 8 | `B` | ... | ... | Finished all neighbors $\to$ backtrack to `A` |
| 9 | `A` | ... | ... | Inspect next neighbor `C` (already visited) $\to$ finish! |

Final traversal order: `['A', 'B', 'D', 'C', 'E']`.

---

## 5. Iterative DFS Using an Explicit Stack

In recursive DFS, the Python interpreter's **call stack** remembers where to backtrack. We can implement DFS iteratively using an explicit Python `list` as a Last-In, First-Out (LIFO) stack:

```python
def dfs_iterative(graph: Graph[T], start: T) -> list[T]:
    if not graph.has_vertex(start):
        raise KeyError(f"Start vertex {start!r} does not exist in graph")

    visited: set[T] = {start}
    stack: list[T] = [start]
    order: list[T] = []

    while stack:
        curr = stack.pop()
        order.append(curr)

        # Push unvisited neighbors in reverse order so the first neighbor is popped first
        for neighbor in reversed(graph.neighbors(curr)):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return order
```

> [!NOTE]
> **Why Reverse the Neighbors When Pushing?**
> A stack pops the *newest* item first. If vertex `A` has neighbors `['B', 'C']`:
> - Pushing in forward order puts `B` on bottom and `C` on top, so `C` is popped first.
> - Pushing in reverse order (`['C', 'B']`) puts `C` on bottom and `B` on top, so `B` is popped first!
> This ensures that iterative DFS produces the exact same left-to-right exploration order as recursive DFS.

---

## 6. Cycle Detection via DFS

DFS is also the standard technique for detecting cycles:
- **In an Undirected Graph**: If we explore a neighbor that is *already visited* and is *not* our direct parent (the node we just came from), we have found an alternative path back to an earlier vertex — a cycle!
- **In a Directed Graph**: A cycle occurs when an edge points back to an ancestor currently on the active recursion stack (a *back-edge*). We can track three states: `0` (unvisited), `1` (currently visiting / on active stack), and `2` (completely visited).

See [`src/graphs_from_first_principles/traversals.py`](file:///Users/xq/Documents/GitHub/_first-principles/graphs-from-first-principles/src/graphs_from_first_principles/traversals.py) for the tested `has_cycle` implementation.

---

## 7. Time and Space Complexity Summary

- **Time Complexity**: **$O(V + E)$**.
  - Every vertex is added to `visited` and entered once: $O(V)$.
  - In an adjacency list, every edge is examined once (directed) or twice (undirected) across all neighbor loops: $O(E)$.
- **Auxiliary Space Complexity**: **$O(V)$**.
  - The `visited` set holds at most $|V|$ vertices.
  - The recursion call stack (or explicit stack) reaches depth at most $|V|$ in the worst case (e.g., a straight line graph).

---

## 8. Check Your Understanding: Exercises

### Exercise 1: Recursive vs Iterative Call Stack
Suppose a graph is a single straight line of 100,000 vertices: $v_1 - v_2 - \dots - v_{100,000}$.
What will happen if you run `dfs_recursive` in standard Python? What will happen if you run `dfs_iterative`?

<details>
<summary>View Solution</summary>

- `dfs_recursive` will fail with a `RecursionError` because Python's default recursion limit is typically 1,000 frames.
- `dfs_iterative` uses a Python heap-allocated list as the stack and easily handles 100,000 items without overflowing Python's call stack.
</details>

### Exercise 2: Parent Tracking in Undirected Cycles
In the undirected graph $A - B$, why does checking whether $A$ is in `visited` when looking at $B$'s neighbors NOT indicate a cycle?

<details>
<summary>View Solution</summary>

Because the edge between $A$ and $B$ is bidirectional, $A$ is in $B$'s neighbor list simply because we just came from $A$! $A$ is the *immediate parent* of $B$. A cycle only exists if an already-visited neighbor is **not** the parent.
</details>

---

## Next Steps
Now that you have mastered Depth-First Search, proceed to **[Tutorial 5: Breadth-First Search (BFS) and Shortest Paths](file:///Users/xq/Documents/GitHub/_first-principles/graphs-from-first-principles/tutorials/05-breadth-first-search-and-shortest-paths.md)** to see how level-by-level search finds shortest paths in unweighted graphs.
