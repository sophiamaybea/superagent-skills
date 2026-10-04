---
description: "First-principles architecture and stack selection for Omega Builder. Read when choosing the system shape."
connections: [execution-protocol, research-method, quality-bar]
---

# Architecture

Every project is inputs, state, transformations, outputs, feedback.

Name invariants, constraints, bottlenecks, uncertainty, failure modes, and how the system knows it is working.

Score a dependency as capability times reliability times performance times maintainability times ecosystem times leverage, divided by complexity.

Workload starts: product apps TypeScript/React/Next/PostgreSQL; high concurrency Go, Rust, or Elixir; AI or science Python with verification outside the model; CPU-critical Rust or C++; local analysis DuckDB, Arrow, Parquet, Polars. Change any default the evidence contradicts.

Do not invent a cipher. Use AES-GCM, ChaCha20-Poly1305, Ed25519, X25519, SHA-2, SHA-3, Argon2, HKDF.
