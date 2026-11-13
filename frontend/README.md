# Graphs from First Principles — Interactive Frontend

An Apple-inspired interactive visual textbook and laboratory for the graph algorithms curriculum in this repository.

Built with **Astro 5**, **TypeScript**, **KaTeX**, and clean SVG interactive components with zero heavyweight UI framework dependencies.

---

## Design Principles

- **Apple-Inspired Restraint**: Light neutral backgrounds, San Francisco system typography stack, generous whitespace, subtle 1px borders, and purposeful accent colors.
- **Zero Frontend Framework Bloat**: Pure Astro components and standard TypeScript. No React, Vue, or bulky client bundles.
- **Deterministic Interactivity**: The graph traversal simulator uses the exact deterministic neighbor ordering and state transitions as the Python implementation.
- **Static First**: Generates pure static HTML and minimal client-side JavaScript, ready for deployment on GitHub Pages or any static host.
- **Accessible & Responsive**: Keyboard shortcuts for the simulator (`Space`, `→`, `←`, `R`), high-contrast focus rings, and responsive layouts across mobile and desktop.

---

## Architecture

```
frontend/
├── astro.config.mjs             # Base path configuration & KaTeX / Shiki plugins
├── package.json                 # Minimal dependencies (astro, vitest, katex)
├── tsconfig.json                # TypeScript configuration
├── vitest.config.ts             # Vitest test runner configuration
└── src/
    ├── content.config.ts        # Astro 5 Content Collections glob loader
    ├── data/
    │   └── curriculum.ts        # Chapter metadata, reading times, and topics
    ├── lib/
    │   └── traversalEngine.ts   # Pure TS deterministic BFS and DFS step generator
    ├── components/
    │   ├── Header.astro         # Sticky frosted-glass header
    │   ├── Sidebar.astro        # Responsive chapter navigation tree
    │   └── InteractiveGraphVisualizer.astro # SVG canvas + step inspector
    ├── layouts/
    │   ├── BaseLayout.astro     # Global HTML shell + KaTeX CSS + footer
    │   └── TutorialLayout.astro # Article layout with breadcrumbs and prev/next
    ├── pages/
    │   ├── index.astro          # Landing page & curriculum overview
    │   ├── visualizer.astro     # Dedicated Traversal Laboratory page
    │   ├── 404.astro            # 404 Not Found page
    │   └── tutorials/[...slug].astro # Dynamic static route rendering markdown
    ├── styles/
    │   └── global.css           # Apple design tokens, typography, and controls
    └── tests/
        ├── traversalEngine.test.ts # Unit tests for BFS/DFS step transitions
        └── navigation.test.ts      # Tests for curriculum and build artifacts
```

---

## Verification & Commands

From the `frontend/` directory:

### 1. Install Dependencies
```bash
npm ci
```

### 2. Type-Check and Linting
```bash
npm run check
```

### 3. Run Unit Tests
```bash
npm test
```

### 4. Build Static Site
```bash
npm run build
```
Build output is generated into `frontend/dist/`.

### 5. Preview Locally
```bash
npm run preview
```

### 6. Development Server
```bash
npm run dev
```

---

## Static Deployment (e.g. GitHub Pages)

The static build supports subpath deployments using the `ASTRO_BASE_PATH` environment variable:

```bash
# For GitHub Pages hosted at https://<username>.github.io/<repo>/
ASTRO_BASE_PATH="/graphs-from-first-principles/" npm run build
```

The resulting `dist/` folder can be directly uploaded to GitHub Pages, Cloudflare Pages, Netlify, or Vercel.
