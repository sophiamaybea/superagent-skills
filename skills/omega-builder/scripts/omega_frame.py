#!/usr/bin/env python3
"""Emit an Omega Builder project frame for an objective.

The frame is a decision record. Fill it before implementation and update it
when a decision changes. It does not build the system.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date


TEMPLATE = """# Omega frame — {objective}

Date: {today}
Status: open

## Objective

- Stated request: {objective}
- Real outcome:
- 10× version (same objective, better means):
- Assumptions deleted:
- Assumption recorded (default chosen):

## Reduction

- Inputs:
- State:
- Transformations:
- Outputs:
- Feedback:

## Forces

- Invariants:
- Constraints:
- Bottlenecks:
- Uncertainty:
- Failure modes:

## Research

Formulations to run: direct, primitive, adjacent, unusual, experimental, high-performance, minimal, production.

| Find | Class (USE / BORROW / STUDY / AVOID / OPPORTUNITY) | Why |
| --- | --- | --- |
|  |  |  |

## Stack

- Chosen:
- Rejected alternative:
- Why each dependency earns its place:

## Vertical slice

- User action:
- Real logic:
- Real data:
- Real output:
- Verified command and result:
- Still inferred:

## Attack notes

- Empty:
- Malformed:
- Double submit / refresh mid-write:
- Failed dependency:

## Done

- [ ] Primary workflow works
- [ ] Edge cases from the attack pass handled
- [ ] Build / types / tests run, results recorded
- [ ] Empty, loading, and error states work
- [ ] Secrets absent
- [ ] Placeholders removed
- [ ] User can run it
"""


def build_frame(objective: str, today: str | None = None) -> str:
    cleaned = " ".join(objective.split())
    if not cleaned:
        raise ValueError("objective must not be empty")
    return TEMPLATE.format(objective=cleaned, today=today or date.today().isoformat())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Emit an Omega Builder project frame")
    parser.add_argument("--objective", required=True, help="The build objective")
    parser.add_argument("--out", help="Write the frame to this path instead of stdout")
    args = parser.parse_args(argv)
    try:
        frame = build_frame(args.objective)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(frame)
        print(args.out)
    else:
        sys.stdout.write(frame)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
