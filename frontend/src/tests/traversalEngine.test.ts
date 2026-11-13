import { describe, expect, it } from 'vitest';
import {
  PREDEFINED_GRAPH,
  generateBFSSteps,
  generateDFSSteps,
} from '../lib/traversalEngine';

describe('Traversal Engine', () => {
  it('verifies predefined graph structure', () => {
    expect(PREDEFINED_GRAPH.nodes.length).toBe(6);
    expect(PREDEFINED_GRAPH.edges.length).toBe(6);
    expect(PREDEFINED_GRAPH.adjacency['A']).toEqual(['B', 'C']);
  });

  describe('BFS Step Generation', () => {
    const bfsSteps = generateBFSSteps(PREDEFINED_GRAPH, 'A');

    it('generates non-empty step sequence ending in complete state', () => {
      expect(bfsSteps.length).toBeGreaterThan(0);
      expect(bfsSteps[0].stepIndex).toBe(0);
      expect(bfsSteps[0].frontierType).toBe('queue');
      expect(bfsSteps[0].frontier).toEqual(['A']);
      expect(bfsSteps[0].visited).toEqual(['A']);

      const lastStep = bfsSteps[bfsSteps.length - 1];
      expect(lastStep.isComplete).toBe(true);
      expect(lastStep.frontier).toEqual([]);
      expect(new Set(lastStep.visited)).toEqual(new Set(['A', 'B', 'C', 'D', 'E', 'F']));
    });

    it('enforces FIFO queue ordering across levels', () => {
      // Find step where B is dequeued
      const dequeueB = bfsSteps.find(
        (s) => s.actionTitle.includes('Dequeue') && s.currentNode === 'B',
      );
      // Find step where C is dequeued
      const dequeueC = bfsSteps.find(
        (s) => s.actionTitle.includes('Dequeue') && s.currentNode === 'C',
      );
      // Find step where D is dequeued
      const dequeueD = bfsSteps.find(
        (s) => s.actionTitle.includes('Dequeue') && s.currentNode === 'D',
      );

      expect(dequeueB).toBeDefined();
      expect(dequeueC).toBeDefined();
      expect(dequeueD).toBeDefined();

      // In BFS, Level 1 (B, C) is dequeued before Level 2 (D)
      expect(dequeueB!.stepIndex).toBeLessThan(dequeueD!.stepIndex);
      expect(dequeueC!.stepIndex).toBeLessThan(dequeueD!.stepIndex);
    });
  });

  describe('DFS Step Generation', () => {
    const dfsSteps = generateDFSSteps(PREDEFINED_GRAPH, 'A');

    it('generates non-empty step sequence ending in complete state', () => {
      expect(dfsSteps.length).toBeGreaterThan(0);
      expect(dfsSteps[0].stepIndex).toBe(0);
      expect(dfsSteps[0].frontierType).toBe('stack');
      expect(dfsSteps[0].frontier).toEqual(['A']);
      expect(dfsSteps[0].visited).toEqual(['A']);

      const lastStep = dfsSteps[dfsSteps.length - 1];
      expect(lastStep.isComplete).toBe(true);
      expect(lastStep.frontier).toEqual([]);
      expect(new Set(lastStep.visited)).toEqual(new Set(['A', 'B', 'C', 'D', 'E', 'F']));
    });

    it('enforces LIFO deep exploration before backtracking to C', () => {
      // In DFS from A, B is visited, then D is popped before C
      const popD = dfsSteps.find(
        (s) => s.actionTitle.includes('Pop') && s.currentNode === 'D',
      );
      const popC = dfsSteps.find(
        (s) => s.actionTitle.includes('Pop') && s.currentNode === 'C',
      );

      expect(popD).toBeDefined();
      expect(popC).toBeDefined();

      // D (deep in B's subtree) is popped BEFORE C
      expect(popD!.stepIndex).toBeLessThan(popC!.stepIndex);
    });
  });
});
