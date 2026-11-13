import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';

describe('Code Theme & Syntax Highlighting Contrast', () => {
  it('configures Astro Shiki with a dark theme in astro.config.mjs', () => {
    const configPath = path.resolve(__dirname, '../../astro.config.mjs');
    const content = fs.readFileSync(configPath, 'utf-8');

    // Must configure a dark theme directly rather than defaulting to light-theme inline styles
    expect(content).toMatch(/theme:\s*['"]github-dark['"]/);
    expect(content).not.toMatch(/themes:\s*\{\s*light:/);
  });

  it('does not contain contradictory !important color or background overrides on pre in global.css', () => {
    const cssPath = path.resolve(__dirname, '../styles/global.css');
    const content = fs.readFileSync(cssPath, 'utf-8');

    // Verify absence of !important overrides on pre background/color that clobber Shiki
    expect(content).not.toMatch(/background-color:[^;]*!important/);
    expect(content).not.toMatch(/color:[^;]*!important/);
  });

  it('renders high-contrast syntax tokens without near-black text in Python code blocks', () => {
    const ch3Path = path.resolve(
      __dirname,
      '../../dist/tutorials/03-building-a-graph-in-python/index.html',
    );

    if (fs.existsSync(ch3Path)) {
      const html = fs.readFileSync(ch3Path, 'utf-8');

      // Verify to_adjacency_matrix exists in the generated HTML
      expect(html).toContain('to_adjacency_matrix');

      // The pre container should use github-dark with its dark background (#24292e)
      expect(html).toContain('class="astro-code github-dark"');
      expect(html).toContain('background-color:#24292e');

      // Find the code block for to_adjacency_matrix
      const toAdjIndex = html.indexOf('to_adjacency_matrix');
      const blockStart = html.lastIndexOf('<pre class="astro-code', toAdjIndex);
      const blockEnd = html.indexOf('</pre>', toAdjIndex);
      const codeBlock = html.substring(blockStart, blockEnd);

      // Verify that NO token spans have near-black #24292e text
      const tokenSpans = codeBlock.match(/<span[^>]*style="[^"]*"/g) || [];
      const nearBlackTokens = tokenSpans.filter(span => /(?<!background-)color:\s*#24292[eE]/i.test(span));
      expect(nearBlackTokens).toEqual([]);

      // Verify presence of high-contrast dark theme token colors
      expect(codeBlock).toContain('#F97583'); // Keyword (def, for, in)
      expect(codeBlock).toContain('#B392F0'); // Function name (to_adjacency_matrix)
      expect(codeBlock).toContain('#79B8FF'); // Builtin / Type (self, len, int)
      expect(codeBlock).toContain('#E1E4E8'); // Identifier / Punctuation (labels, matrix)
    }
  });

  it('renders plaintext ASCII diagrams with accessible light text color', () => {
    const ch1Path = path.resolve(
      __dirname,
      '../../dist/tutorials/01-foundations-trees-to-graphs/index.html',
    );

    if (fs.existsSync(ch1Path)) {
      const html = fs.readFileSync(ch1Path, 'utf-8');
      expect(html).toContain('Binary Tree (Hierarchical)');
      // Plaintext blocks should have color:#e1e4e8 on pre
      expect(html).toContain('style="background-color:#24292e;color:#e1e4e8;');
    }
  });
});
