# Step 05 — Practice tasks

*(loop per AT)* · Run-sheet: [process-delivery.md](../../../docs/process-delivery.md)

Build the practice that mirrors each AT task-for-task through the assessment's own renderers, re-scenarioed so nothing leaks.

## Tooling

- engine `run_sheet.py` — `scripts/helpers/`
- generators — content repo `scripts/s1_cl*/*_practice_run_sheet.py`
- website state — website repo `states.ts`, `projects.ts`

## Gate

**Gate 05 → 06** · *human review* — the practice covers the AT's parts, is re-scenarioed, and leaks nothing. **No validator** (human-only).

## Status

**Not ported** — the tooling above still lives at its legacy location. Converting it is done on request,
test-first; see [factory/README.md](../../README.md).
