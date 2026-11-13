/**
 * Traversal engine for step-by-step interactive graph visualization.
 *
 * Implements deterministic DFS (using explicit LIFO stack) and BFS (using FIFO queue),
 * maintaining exact parity with the Python reference implementation.
 */

export interface GraphNode {
  id: string;
  x: number;
  y: number;
  label: string;
}

export interface GraphEdge {
  u: string;
  v: string;
}

export interface PredefinedGraph {
  nodes: GraphNode[];
  edges: GraphEdge[];
  adjacency: Record<string, string[]>;
}

export interface TraversalStep {
  stepIndex: number;
  totalSteps: number;
  currentNode: string | null;
  visited: string[]; // Order of discovery / visited vertices
  frontier: string[]; // Array representing stack (top on right) or queue (front on left)
  frontierType: 'stack' | 'queue';
  highlightedEdge: [string, string] | null;
  examinedNeighbors: string[];
  actionTitle: string;
  actionExplanation: string;
  isComplete: boolean;
}

export const PREDEFINED_GRAPH: PredefinedGraph = {
  nodes: [
    { id: 'A', x: 320, y: 60, label: 'A' },
    { id: 'B', x: 180, y: 160, label: 'B' },
    { id: 'C', x: 460, y: 160, label: 'C' },
    { id: 'D', x: 100, y: 290, label: 'D' },
    { id: 'E', x: 260, y: 290, label: 'E' },
    { id: 'F', x: 460, y: 290, label: 'F' },
  ],
  edges: [
    { u: 'A', v: 'B' },
    { u: 'A', v: 'C' },
    { u: 'B', v: 'D' },
    { u: 'B', v: 'E' },
    { u: 'C', v: 'F' },
    { u: 'E', v: 'F' },
  ],
  adjacency: {
    A: ['B', 'C'],
    B: ['A', 'D', 'E'],
    C: ['A', 'F'],
    D: ['B'],
    E: ['B', 'F'],
    F: ['C', 'E'],
  },
};

/**
 * Generate all discrete steps for Breadth-First Search (BFS).
 *
 * Uses a FIFO queue. Vertices are marked visited when enqueued,
 * preventing duplicate queue additions.
 */
export function generateBFSSteps(
  graph: PredefinedGraph = PREDEFINED_GRAPH,
  startNode: string = 'A',
): TraversalStep[] {
  const steps: TraversalStep[] = [];
  const visitedSet = new Set<string>([startNode]);
  const queue: string[] = [startNode];
  const visitedHistory: string[] = [startNode];

  // Initial Step 0
  steps.push({
    stepIndex: 0,
    totalSteps: 0, // will patch at the end
    currentNode: null,
    visited: [...visitedHistory],
    frontier: [...queue],
    frontierType: 'queue',
    highlightedEdge: null,
    examinedNeighbors: [],
    actionTitle: `Initialize BFS from Vertex ${startNode}`,
    actionExplanation: `Add start vertex ${startNode} to queue and mark it as visited. Queue holds the frontier of vertices waiting to be explored.`,
    isComplete: false,
  });

  while (queue.length > 0) {
    const curr = queue.shift()!;
    const neighbors = graph.adjacency[curr] || [];
    const unvisitedNeighbors: string[] = [];

    // Step: Dequeue vertex
    steps.push({
      stepIndex: steps.length,
      totalSteps: 0,
      currentNode: curr,
      visited: [...visitedHistory],
      frontier: [...queue],
      frontierType: 'queue',
      highlightedEdge: null,
      examinedNeighbors: [...neighbors],
      actionTitle: `Dequeue Vertex ${curr}`,
      actionExplanation: `Removed ${curr} from the front of the queue. Now inspecting all incident neighbors: [${neighbors.join(', ')}].`,
      isComplete: false,
    });

    for (const neighbor of neighbors) {
      if (!visitedSet.has(neighbor)) {
        visitedSet.add(neighbor);
        visitedHistory.push(neighbor);
        queue.push(neighbor);
        unvisitedNeighbors.push(neighbor);

        steps.push({
          stepIndex: steps.length,
          totalSteps: 0,
          currentNode: curr,
          visited: [...visitedHistory],
          frontier: [...queue],
          frontierType: 'queue',
          highlightedEdge: [curr, neighbor],
          examinedNeighbors: [neighbor],
          actionTitle: `Enqueue Neighbor ${neighbor}`,
          actionExplanation: `Vertex ${neighbor} has not been visited yet. Mark it visited immediately and append to back of queue.`,
          isComplete: false,
        });
      }
    }
  }

  // Final completion step
  steps.push({
    stepIndex: steps.length,
    totalSteps: 0,
    currentNode: null,
    visited: [...visitedHistory],
    frontier: [],
    frontierType: 'queue',
    highlightedEdge: null,
    examinedNeighbors: [],
    actionTitle: 'BFS Complete',
    actionExplanation: `The queue is empty. All reachable vertices were explored level-by-level in ${visitedHistory.length} visits.`,
    isComplete: true,
  });

  const total = steps.length;
  steps.forEach((s) => (s.totalSteps = total));
  return steps;
}

/**
 * Generate all discrete steps for Depth-First Search (DFS).
 *
 * Uses an explicit LIFO stack. To match the left-to-right neighbor ordering
 * of recursive DFS, unvisited neighbors are pushed onto the stack in reverse order.
 */
export function generateDFSSteps(
  graph: PredefinedGraph = PREDEFINED_GRAPH,
  startNode: string = 'A',
): TraversalStep[] {
  const steps: TraversalStep[] = [];
  const visitedSet = new Set<string>([startNode]);
  const stack: string[] = [startNode]; // top of stack is stack[stack.length - 1]
  const visitedHistory: string[] = [startNode];

  // Initial Step 0
  steps.push({
    stepIndex: 0,
    totalSteps: 0,
    currentNode: null,
    visited: [...visitedHistory],
    frontier: [...stack],
    frontierType: 'stack',
    highlightedEdge: null,
    examinedNeighbors: [],
    actionTitle: `Initialize DFS from Vertex ${startNode}`,
    actionExplanation: `Push start vertex ${startNode} onto the stack and mark it as visited.`,
    isComplete: false,
  });

  while (stack.length > 0) {
    const curr = stack.pop()!;
    const neighbors = graph.adjacency[curr] || [];

    // Step: Pop vertex
    steps.push({
      stepIndex: steps.length,
      totalSteps: 0,
      currentNode: curr,
      visited: [...visitedHistory],
      frontier: [...stack],
      frontierType: 'stack',
      highlightedEdge: null,
      examinedNeighbors: [...neighbors],
      actionTitle: `Pop Vertex ${curr} from Stack`,
      actionExplanation: `Popped ${curr} from the top of the stack. Now examining its neighbors in order: [${neighbors.join(', ')}].`,
      isComplete: false,
    });

    // Push unvisited neighbors in reverse order so the first neighbor is on top
    const unvisited = neighbors.filter((n) => !visitedSet.has(n));
    const reversedUnvisited = [...unvisited].reverse();

    for (const neighbor of reversedUnvisited) {
      visitedSet.add(neighbor);
      visitedHistory.push(neighbor);
      stack.push(neighbor);

      steps.push({
        stepIndex: steps.length,
        totalSteps: 0,
        currentNode: curr,
        visited: [...visitedHistory],
        frontier: [...stack],
        frontierType: 'stack',
        highlightedEdge: [curr, neighbor],
        examinedNeighbors: [neighbor],
        actionTitle: `Push Neighbor ${neighbor} to Stack`,
        actionExplanation: `Vertex ${neighbor} is unvisited. Mark visited and push onto stack (next to be explored).`,
        isComplete: false,
      });
    }

    if (unvisited.length === 0) {
      steps.push({
        stepIndex: steps.length,
        totalSteps: 0,
        currentNode: curr,
        visited: [...visitedHistory],
        frontier: [...stack],
        frontierType: 'stack',
        highlightedEdge: null,
        examinedNeighbors: [],
        actionTitle: `Backtrack from Vertex ${curr}`,
        actionExplanation: `No unvisited neighbors remain for ${curr}. Backtracking to next vertex on stack.`,
        isComplete: false,
      });
    }
  }

  // Final completion step
  steps.push({
    stepIndex: steps.length,
    totalSteps: 0,
    currentNode: null,
    visited: [...visitedHistory],
    frontier: [],
    frontierType: 'stack',
    highlightedEdge: null,
    examinedNeighbors: [],
    actionTitle: 'DFS Complete',
    actionExplanation: `The stack is empty. All connected vertices were explored along depth paths in ${visitedHistory.length} visits.`,
    isComplete: true,
  });

  const total = steps.length;
  steps.forEach((s) => (s.totalSteps = total));
  return steps;
}
