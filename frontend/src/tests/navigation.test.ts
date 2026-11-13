import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { TUTORIALS } from '../data/curriculum';
import { PREDEFINED_GRAPH, generateBFSSteps, generateDFSSteps } from '../lib/traversalEngine';

describe('Curriculum & Navigation Integrity', () => {
  it('has exactly 7 sequential chapters', () => {
    expect(TUTORIALS.length).toBe(7);
    TUTORIALS.forEach((tut, index) => {
      expect(tut.chapterNumber).toBe(index + 1);
    });
  });

  it('matches Markdown source files in ../tutorials', () => {
    const tutorialsDir = path.resolve(__dirname, '../../../tutorials');
    expect(fs.existsSync(tutorialsDir)).toBe(true);

    for (const tut of TUTORIALS) {
      const filePath = path.join(tutorialsDir, `${tut.id}.md`);
      expect(fs.existsSync(filePath), `Missing tutorial file: ${filePath}`).toBe(true);
      const content = fs.readFileSync(filePath, 'utf-8');
      expect(content.length).toBeGreaterThan(100);
    }
  });

  it('verifies traversal step generator works from all graph nodes', () => {
    for (const node of PREDEFINED_GRAPH.nodes) {
      const bfsSteps = generateBFSSteps(PREDEFINED_GRAPH, node.id);
      expect(bfsSteps.length).toBeGreaterThan(1);
      expect(bfsSteps[bfsSteps.length - 1].isComplete).toBe(true);

      const dfsSteps = generateDFSSteps(PREDEFINED_GRAPH, node.id);
      expect(dfsSteps.length).toBeGreaterThan(1);
      expect(dfsSteps[dfsSteps.length - 1].isComplete).toBe(true);
    }
  });

  it('verifies static build artifacts exist in dist', () => {
    const distDir = path.resolve(__dirname, '../../dist');
    // If build has run, verify routes
    if (fs.existsSync(distDir)) {
      expect(fs.existsSync(path.join(distDir, 'index.html'))).toBe(true);
      expect(fs.existsSync(path.join(distDir, '404.html'))).toBe(true);
      expect(fs.existsSync(path.join(distDir, 'visualizer/index.html'))).toBe(true);
      for (const tut of TUTORIALS) {
        expect(
          fs.existsSync(path.join(distDir, `tutorials/${tut.slug}/index.html`)),
          `Missing static build HTML for ${tut.slug}`,
        ).toBe(true);
      }
    }
  });
});
