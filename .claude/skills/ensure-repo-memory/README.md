# ensure-repo-memory · v1.0.0 (updated 2026-06-14)

## Purpose
Redirect this repository's Claude Code **auto-memory** into the version-controlled
`<repo>/.claude/memory/` folder, so memory is committed to git and travels between machines.
Idempotent self-heal: run it (or let the `SessionStart` hook run it) at the start of a
session — it sets the path once per machine and is a cheap no-op thereafter.

## Prerequisites
- **Windows + PowerShell** — the engine is a `.ps1`; the `SessionStart` hook invokes `powershell`.
- **Git** on PATH (used to find the repo root; falls back to the current directory).
- A **`.claude/` folder** in the repo (the skill reports `SKIP` if absent).
- Write access to `<repo>/.claude/settings.local.json` (machine-local, **gitignored**).
- The memory files live in `<repo>/.claude/memory/` (committed); this skill only points the
  machine *at* them — it doesn't create their content.

## Inputs & outputs
- **Input:** the repo it runs in (root via `git rev-parse --show-toplevel`).
- **Output:** one STATUS line —
  - `OK:` already configured (no change),
  - `FIXED:` set the path → **relaunch required** (auto-memory loads at launch),
  - `SKIP:` no `.claude` folder here.
- **Side effect on FIXED:** writes `autoMemoryDirectory` into `settings.local.json` (preserving
  other keys) and creates `.claude/memory/` if missing.

## How it works
`ensure_repo_memory.ps1`: find repo root → compute `<root>/.claude/memory` → compare to
`autoMemoryDirectory` in `settings.local.json` (case-insensitive) → write it if missing/wrong
(UTF-8, no BOM). `autoMemoryDirectory` must be an absolute path, which differs per machine, so
it lives in the **gitignored** local settings and this skill re-establishes it on each machine.
`SKILL.md` runs the script (`model: haiku`) and relays the STATUS line.

## Version history
- **v1.0.0 (2026-06-14)** — initial documented version (UTF-8-hardened read/write).
