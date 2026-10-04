---
description: "Phase-by-phase Omega Builder execution. Read at the start of a build and again before ship."
connections: [research-method, architecture, quality-bar]
---

# Execution protocol

Run scripts/omega_frame.py --objective and fill the frame before implementation.

1. Understand the real outcome and the 10x version.
2. Inspect the repo and environment before a rewrite.
3. Research with the eight formulations.
4. Inspect promising repos for architecture, tests, licence, and unfixed limits.
5. Classify finds before integrating.
6. Architect the smallest system that can still be exceptional.
7. Build a vertical slice: user action, real logic, real data, real output.
8. Integrate persistence, errors, loading, and empty states.
9. Verify with real commands. Label anything not run as inferred.
10. Attack empty, malformed, double-submit, and failed dependency cases.
11. Optimise only measured bottlenecks.
12. Refine architecture if the critique found a structural flaw.
13. Polish. No dead navigation or placeholder copy.
14. Ship setup instructions, verified results, and no secrets.

Ask only if a missing fact would change the product.
