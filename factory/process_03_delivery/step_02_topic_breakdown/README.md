# Step 02 — Topic breakdown

*(loop per AT)* · Run-sheet: [process-delivery.md](../../../docs/process-delivery.md)

Split each AT into the Topics that teach it — every AT gets at least one Topic, every Topic declares its AT.

## Tooling

- validator `validate_topic_breakdown.py` — `.claude/skills/scripts/`

## Gate

**Gate 02 → 03** · *validator* `validate-topic-breakdown` = every AT has ≥1 Topic, every Topic declares a real AT, count fits the frame.

## Status

**Not ported** — the tooling above still lives at its legacy location. Converting it is done on request,
test-first; see [factory/README.md](../../README.md).
