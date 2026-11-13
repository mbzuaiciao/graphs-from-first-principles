"""Interactive demonstration of graphs and traversals from first principles.

Run with:
    python -m examples.demo
or:
    uv run python -m examples.demo
"""

from graphs_from_first_principles import (
    Graph,
    bfs,
    bfs_shortest_path,
    dfs_iterative,
    dfs_recursive,
    find_connected_components,
    has_cycle,
)


def main() -> None:
    print("=" * 60)
    print(" GRAPHS FROM FIRST PRINCIPLES: DEMONSTRATION")
    print("=" * 60)

    # 1. Building an Undirected Graph
    print("\n1. Building an Undirected Graph:")
    g = Graph[str](directed=False)
    for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F")]:
        g.add_edge(u, v)

    print(f"Graph: {g}")
    print(f"Vertices ({g.order()}): {g.vertices()}")
    print(f"Edges ({g.size()}): {g.edges()}")
    for node in g.vertices():
        print(f"  Neighbors of {node}: {g.neighbors(node)} (degree {g.degree(node)})")

    # 2. Adjacency Matrix Conversion
    print("\n2. Adjacency Matrix Representation:")
    matrix, labels = g.to_adjacency_matrix()
    header = "    " + " ".join(f"{v:>3}" for v in labels)
    print(header)
    print("   " + "-" * (len(header) - 3))
    for v, row in zip(labels, matrix):
        row_str = " ".join(f"{val:>3}" for val in row)
        print(f"{v:>2} | {row_str}")

    # 3. Depth-First Search (DFS)
    print("\n3. Depth-First Search (DFS from 'A'):")
    dfs_rec = dfs_recursive(g, "A")
    dfs_it = dfs_iterative(g, "A")
    print(f"  DFS Recursive order: {dfs_rec}")
    print(f"  DFS Iterative order: {dfs_it}")
    assert dfs_rec == dfs_it

    # 4. Breadth-First Search (BFS)
    print("\n4. Breadth-First Search (BFS from 'A'):")
    bfs_order = bfs(g, "A")
    print(f"  BFS Level-by-level order: {bfs_order}")
    print("  Notice how BFS visits all neighbors at distance 1 ('B', 'C') before")
    print("  moving to distance 2 ('D', 'E', 'F'), whereas DFS dives deep first!")

    # 5. Shortest Paths in Unweighted Graphs
    print("\n5. Shortest Path via BFS:")
    # Add a shortcut to show edge-count optimality
    g.add_edge("A", "E")
    print("  Added edge ('A', 'E') creating a direct shortcut.")
    path_to_e = bfs_shortest_path(g, "A", "E")
    print(f"  Shortest path from 'A' to 'E': {' -> '.join(path_to_e)}")
    path_to_d = bfs_shortest_path(g, "A", "D")
    print(f"  Shortest path from 'A' to 'D': {' -> '.join(path_to_d)}")

    # 6. Cycle Detection
    print("\n6. Cycle Detection:")
    print(f"  Does graph have a cycle now? {has_cycle(g)}")
    print("  (Yes, A - B - E - A forms a cycle of length 3)")

    # 7. Disconnected Graphs & Connected Components
    print("\n7. Disconnected Graphs & Components:")
    # Add disconnected vertices and edges
    g.add_edge("X", "Y")
    g.add_vertex("Z")  # Isolated vertex
    print("  Added independent edge ('X', 'Y') and isolated vertex 'Z'.")
    print(f"  Total vertices: {g.order()}")

    single_bfs = bfs(g, "A")
    print(f"  Single BFS starting from 'A' can only reach: {single_bfs}")

    components = find_connected_components(g)
    print(f"  Component analysis finds {len(components)} distinct components:")
    for i, comp in enumerate(components, 1):
        print(f"    Component {i}: {comp}")

    print("\n" + "=" * 60)
    print(" Demonstration complete! All fundamentals working as expected.")
    print("=" * 60)


if __name__ == "__main__":
    main()
