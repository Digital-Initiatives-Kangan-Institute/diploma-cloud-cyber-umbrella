# Step 01 — Cluster specification (delivery frame)

*(per cluster; gate is semester-level)* · Run-sheet: [process-delivery.md](../../../docs/process-delivery.md)

Elicit and record the box the teaching is fitted into: nominal hours, weeks, sessions, session length, schedule conventions, and the derived topic budget.

## Tooling

- skill `setup-cluster-spec` — `.claude/skills/setup-cluster-spec/`
- validator `validate_cluster_spec.py` — `.claude/skills/scripts/`
- format standard `cluster-specification-format.md` — `docs/`

## Gate

**Gate 01 → 02** *(definition phase)* · *validator* `validate-cluster-spec` = **PASS for EVERY cluster**. Human review: whether the frame is pedagogically sound.

## Status

**Not ported** — the tooling above still lives at its legacy location. Converting it is done on request,
test-first; see [factory/README.md](../../README.md).
