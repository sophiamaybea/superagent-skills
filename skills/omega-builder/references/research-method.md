---
description: "How Omega Builder researches GitHub and the landscape, and how finds are classified. Read before choosing dependencies."
connections: [execution-protocol, architecture, quality-bar]
---

# Research method

Research before building on any substantial project. A little-known repository with the right algorithm can matter more than a famous framework.

## Search formulations

Run several, not one:

1. Direct solutions — the product category by name.
2. Underlying primitives — the data structure, protocol, or algorithm.
3. Adjacent systems — neighbouring products that solved a harder subproblem.
4. Unusual implementations — different interaction or storage models.
5. Experimental implementations — papers, labs, abandoned clever repos.
6. High-performance implementations — SIMD, GPU, WASM, lock-free, columnar.
7. Minimal implementations — the smallest correct version of the primitive.
8. Production implementations — what actually ships, including incident write-ups.

## Classification

USE DIRECTLY: stable, licence-compatible dependency. BORROW THE PATTERN: reimplement the idea, do not vendor the repo. STUDY ONLY: read, do not depend. AVOID: abandoned, insecure, or incompatible. OPPORTUNITY: nothing satisfactory exists, invent the missing primitive.

Never blindly copy repository code. Understand it. Respect the licence.
