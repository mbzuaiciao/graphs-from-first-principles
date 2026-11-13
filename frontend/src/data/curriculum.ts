export interface TutorialMeta {
  id: string; // e.g. "01-foundations-trees-to-graphs"
  slug: string;
  chapterNumber: number;
  chapterNumberStr: string;
  title: string;
  shortTitle: string;
  part: string;
  partNumber: number;
  partRoman: string;
  summary: string;
  readingTimeMin: number;
  topics: string[];
}

export const TUTORIALS: TutorialMeta[] = [
  {
    id: '01-foundations-trees-to-graphs',
    slug: '01-foundations-trees-to-graphs',
    chapterNumber: 1,
    chapterNumberStr: '01',
    title: 'Foundations: From Trees to Graphs',
    shortTitle: 'From Trees to Graphs',
    part: 'Part I: Mental Models & Foundations',
    partNumber: 1,
    partRoman: 'I',
    summary:
      'Transition from hierarchical binary trees to arbitrary graphs with vertices, edges, degrees, cycles, and directed vs. undirected connections.',
    readingTimeMin: 7,
    topics: ['Trees vs Graphs', 'Vertices & Edges', 'Degree', 'Directed vs Undirected', 'Walks, Paths & Cycles', 'Handshaking Lemma'],
  },
  {
    id: '02-representations-adjacency-list-and-matrix',
    slug: '02-representations-adjacency-list-and-matrix',
    chapterNumber: 2,
    chapterNumberStr: '02',
    title: 'Graph Representations: Adjacency Lists vs Matrices',
    shortTitle: 'Lists vs Matrices',
    part: 'Part I: Mental Models & Foundations',
    partNumber: 1,
    partRoman: 'I',
    summary:
      'Compare memory layouts, trade-offs, and query complexities between Adjacency Lists (O(V+E)) and Adjacency Matrices (O(V²)).',
    readingTimeMin: 8,
    topics: ['Adjacency List', 'Adjacency Matrix', 'Sparse vs Dense Networks', 'Complexity Trade-offs', 'Matrix Symmetry'],
  },
  {
    id: '03-building-a-graph-in-python',
    slug: '03-building-a-graph-in-python',
    chapterNumber: 3,
    chapterNumberStr: '03',
    title: 'Building a Graph in Python',
    shortTitle: 'Python Graph Class',
    part: 'Part II: Code Construction & Traversals',
    partNumber: 2,
    partRoman: 'II',
    summary:
      'Implement an object-oriented Graph class from first principles with deterministic neighbor ordering, degrees, and matrix export.',
    readingTimeMin: 8,
    topics: ['Class Design', 'Vertex & Edge Ops', 'Deterministic Ordering', 'Defensive Copies', 'Matrix Conversion'],
  },
  {
    id: '04-depth-first-search',
    slug: '04-depth-first-search',
    chapterNumber: 4,
    chapterNumberStr: '04',
    title: 'Depth-First Search (DFS)',
    shortTitle: 'Depth-First Search',
    part: 'Part II: Code Construction & Traversals',
    partNumber: 2,
    partRoman: 'II',
    summary:
      'Explore deep into branches, prevent infinite cycle recursion with visited sets, and trace both recursive and iterative stack executions.',
    readingTimeMin: 9,
    topics: ['The Maze Intuition', 'Cycle Traps', 'Visited Set', 'Recursive DFS', 'Iterative Stack DFS', 'Cycle Detection'],
  },
  {
    id: '05-breadth-first-search-and-shortest-paths',
    slug: '05-breadth-first-search-and-shortest-paths',
    chapterNumber: 5,
    chapterNumberStr: '05',
    title: 'Breadth-First Search & Shortest Paths',
    shortTitle: 'BFS & Shortest Paths',
    part: 'Part II: Code Construction & Traversals',
    partNumber: 2,
    partRoman: 'II',
    summary:
      'Expand level-by-level using collections.deque, enforce the mark-at-enqueue rule, and reconstruct unweighted shortest paths.',
    readingTimeMin: 10,
    topics: ['Ripple Wavefront', 'collections.deque O(1)', 'Mark-at-Enqueue Rule', 'DFS vs BFS', 'Shortest Unweighted Paths'],
  },
  {
    id: '06-disconnected-graphs-and-components',
    slug: '06-disconnected-graphs-and-components',
    chapterNumber: 6,
    chapterNumberStr: '06',
    title: 'Disconnected Graphs & Connected Components',
    shortTitle: 'Connected Components',
    part: 'Part III: Structure & Mathematical Rigor',
    partNumber: 3,
    partRoman: 'III',
    summary:
      'Overcome single-source traversal blindspots by using an outer vertex loop to discover all isolated vertices and connected subgraphs.',
    readingTimeMin: 7,
    topics: ['Single-Source Blindspot', 'Component Definition', 'Outer Loop Pattern', 'Component Traversal', 'Isolated Vertices'],
  },
  {
    id: '07-complexity-analysis-first-principles',
    slug: '07-complexity-analysis-first-principles',
    chapterNumber: 7,
    chapterNumberStr: '07',
    title: 'Complexity Analysis from First Principles',
    shortTitle: 'Complexity Analysis',
    part: 'Part III: Structure & Mathematical Rigor',
    partNumber: 3,
    partRoman: 'III',
    summary:
      'Rigorously derive O(V + E) time using the Handshaking Lemma and prove O(V) auxiliary space bounds for stacks and queues.',
    readingTimeMin: 8,
    topics: ['Two-Variable Complexity', 'Vertex Work vs Edge Work', 'Handshaking Lemma Proof', 'Auxiliary Space', 'Worst-Case Bounds'],
  },
];
