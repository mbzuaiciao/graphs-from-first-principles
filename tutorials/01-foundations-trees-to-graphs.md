# Tutorial 1: Foundations — From Trees to Graphs

> **Inspiration & Attribution**: This tutorial series is an original from-first-principles guide inspired by the topic progression in Paaras Chand's course presentation on [Graphs](https://paaras.github.io/python_ds/graphs#1).

---

## 1. Moving Beyond Trees

In introductory computer science, one of the first non-linear data structures you study is the **binary tree**. A tree organizes data hierarchically:
- It has exactly one **root** node at the top.
- Every node has at most two child pointers (`left` and `right`).
- Every node (except the root) has exactly one incoming connection from its parent.
- There are strictly **no cycles** (you cannot follow pointers and return to a node you already visited).

```
        Binary Tree (Hierarchical)
                 [Root]
                 /    \
             [Child]  [Child]
             /    \
          [Leaf] [Leaf]
```

While trees are ideal for hierarchical structures like file systems and organizational charts, many real-world systems cannot be forced into a hierarchy:
- In a **road network**, roads form loops, intersections connect many streets, and there is no "root" intersection.
- In a **social network**, friendships form interconnected webs where you can be mutual friends with several people.
- On the **World Wide Web**, web pages link to each other freely, often linking back and forth.

To model these interconnected systems, we relax the rigid rules of trees. We arrive at the **graph**.

```
            General Graph (Interconnected)
                 (A) --------- (B)
                  |  \         / |
                  |   \       /  |
                  |    \     /   |
                  |     ( C )    |
                  |    /     \   |
                  |   /       \  |
                 (D) --------- (E)
```

In a general graph:
1. There is **no designated root**. Any vertex can serve as a starting point.
2. A node can be connected to **any number** of other nodes.
3. Connections can form **cycles** (closed loops).
4. The graph can even consist of multiple **disconnected components**.

---

## 2. Core Terminology

A graph $G = (V, E)$ consists of two fundamental sets:
- **Vertices** (also called **Nodes**): The entities or objects in the system, denoted by the set $V$.
- **Edges** (also called **Links** or **Arcs**): The connections between pairs of vertices, denoted by the set $E$.

### Neighbors and Adjacency
When an edge connects vertex $u$ and vertex $v$, we say that $u$ and $v$ are **adjacent** or that they are **neighbors**.

### Degree of a Vertex
The **degree** of a vertex $v$, denoted $\deg(v)$, is the number of edges incident to it (i.e., how many neighbors it has).
- In an undirected graph, an isolated vertex has degree $0$.
- A vertex connected to 4 neighbors has degree $4$.

---

## 3. Directed vs. Undirected Graphs

The relationship between two nodes can be symmetric or asymmetric. This gives rise to two distinct classes of graphs.

```
       Undirected Edge                 Directed Edge
        (A) -------- (B)               (A) --------> (B)
     "Friendship (Mutual)"             "Follows (One-Way)"
```

### Undirected Graphs
In an **undirected graph**, edges have no orientation. An edge between $u$ and $v$ is an unordered pair $\{u, v\}$.
- If $u$ is connected to $v$, then $v$ is automatically connected to $u$.
- **Real-world example**: Facebook friendship or LinkedIn connection. If Ana is connected to Ben, Ben is connected to Ana.

### Directed Graphs (Digraphs)
In a **directed graph**, edges have a specific direction from a source vertex to a target vertex. An edge is an ordered pair $(u, v)$, often drawn as an arrow $u \to v$.
- An edge from $u$ to $v$ does **not** imply an edge from $v$ to $u$.
- **Real-world example**: Twitter/X or Instagram following, web hyperlinks, or prerequisite courses. Ana can follow Ben without Ben following Ana.
- In directed graphs, degree is split into:
  - **In-degree**: The number of incoming edges pointing into $v$.
  - **Out-degree**: The number of outgoing edges leaving $v$.

---

## 4. Walks, Paths, and Cycles

Understanding how to travel through a graph is the foundation of graph algorithms.

1. **Walk**: An alternating sequence of vertices and edges $v_0, e_1, v_1, e_2, \dots, v_k$ where each edge connects consecutive vertices. Vertices and edges may be repeated.
2. **Path (Simple Path)**: A walk where **no vertices are repeated**. For example, in the path $A \to B \to C$, all three vertices are distinct.
3. **Cycle**: A path that starts and ends at the **same vertex**, with no other repeated vertices.
   - For example: $A \to B \to C \to A$.
   - A graph that contains at least one cycle is **cyclic**.
   - A graph that contains no cycles is **acyclic**.
   - A **Directed Acyclic Graph (DAG)** is a directed graph with no directed cycles, commonly used to model task dependencies and build pipelines.

> [!NOTE]
> A tree is simply a special case of a graph: a **connected, undirected, acyclic graph**.

---

## 5. Manually Worked Example

Let us examine the following undirected graph with 5 vertices $\{A, B, C, D, E\}$:

```
        (A) -------- (B)
         |            |  \
         |            |   (E)
         |            |  /
        (C) -------- (D)
```

Let's compute the properties manually:
- **Vertices ($V$)**: $\{A, B, C, D, E\}$, so $|V| = 5$.
- **Edges ($E$)**: $\{\{A, B\}, \{A, C\}, \{B, D\}, \{B, E\}, \{C, D\}, \{D, E\}\}$, so $|E| = 6$.
- **Vertex Degrees**:
  - $\deg(A) = 2$ (neighbors: $B, C$)
  - $\deg(B) = 3$ (neighbors: $A, D, E$)
  - $\deg(C) = 2$ (neighbors: $A, D$)
  - $\deg(D) = 3$ (neighbors: $B, C, E$)
  - $\deg(E) = 2$ (neighbors: $B, D$)
- **Handshaking Lemma Check**:
  Notice the sum of all degrees:
  $$2 + 3 + 2 + 3 + 2 = 12$$
  Since every undirected edge has two endpoints, the sum of degrees is always twice the number of edges: $\sum \deg(v) = 2|E| = 2 \times 6 = 12$.
- **Cycles**:
  - Cycle 1: $A - B - D - C - A$ (length 4)
  - Cycle 2: $B - E - D - B$ (length 3)
  - Cycle 3: $A - B - E - D - C - A$ (length 5)

---

## 6. Check Your Understanding: Exercises

### Exercise 1: Directed vs. Undirected Modeling
Which type of graph (directed or undirected) best models:
1. One-way flight routes between airports?
2. Mutual Bluetooth connections between paired devices?
3. Package dependencies in a `pyproject.toml` file?

<details>
<summary>View Solution</summary>

1. **Directed**: Flights travel in a specific direction (e.g., flight from JFK to LHR does not automatically represent the return leg).
2. **Undirected**: Bluetooth pairing is a mutual, two-way communication channel between two devices.
3. **Directed**: Package A requiring Package B is a one-way dependency ($A \to B$).
</details>

### Exercise 2: Degree Calculation
Suppose an undirected graph has 4 vertices with degrees $1, 2, 3$, and $2$.
1. How many edges does the graph have?
2. Is it possible for an undirected graph to have degree sequence $1, 2, 2, 2$? Why or why not?

<details>
<summary>View Solution</summary>

1. By the Handshaking Lemma, the sum of degrees equals $2|E|$:
   $$\text{Sum} = 1 + 2 + 3 + 2 = 8 \implies 2|E| = 8 \implies |E| = 4.$$
2. **No**, it is impossible. The sum of degrees would be $1 + 2 + 2 + 2 = 7$, which is odd. Since every undirected edge adds $2$ to the total degree sum, the sum must always be an even integer. An odd sum cannot exist in any undirected graph.
</details>

---

## Next Steps
Now that we have built an intuitive mental model of vertices, edges, paths, and cycles, head to **[Tutorial 2: Graph Representations](file:///Users/xq/Documents/GitHub/_first-principles/graphs-from-first-principles/tutorials/02-representations-adjacency-list-and-matrix.md)** to see how graphs are represented inside computer memory.
