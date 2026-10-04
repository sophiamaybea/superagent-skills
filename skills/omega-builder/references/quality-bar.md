---
description: "Definition of done, adversary tests, and the twelve-pass critique. Read before claiming the build is finished."
connections: [execution-protocol, architecture, research-method]
---

# Quality bar

Something is not finished because code exists.

## Definition of done

Mark each item verified or not applicable:

- Architecture is coherent and written in the frame
- Primary workflow functions on real data
- Edge cases found in the attack pass are handled
- Types, tests, build, and lint were run, with results recorded
- Error, loading, and empty states work
- Responsive layout and keyboard access are respectable
- Performance is acceptable on the measured bottleneck
- Security assumptions are addressed
- Setup is reproducible and secrets are absent
- Placeholders and dead controls are gone
- The user can actually use the product

## Adversary pass

Try ordinary use, empty state, enormous input, malformed data, slow network, failed APIs, concurrent operations, repeated clicks, refresh during a write, lost connectivity, expired auth, missing environment variables, unexpected database state, mobile and extreme widths, keyboard only, and a high-load case if the bottleneck is throughput.

## No fake completion

Do not claim tests, deploys, APIs, or speedups that were not run or inspected. Label anything not run as inferred.
