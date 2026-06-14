---
name: ensure-repo-memory
version: 1.0.0
updated: 2026-06-14
description: >-
  Ensure this repository's Claude auto-memory is redirected into the version-controlled
  <repo-root>/.claude/memory folder (via autoMemoryDirectory in the machine-local
  settings.local.json). Idempotent, deterministic, machine-local — safe to run at the start
  of every session; re-running once configured is a cheap no-op. Use when setting up a repo's
  portable memory, or as a session-start self-heal check on a new machine.
model: haiku
shell: powershell
---

# Ensure repo memory

A deterministic, machine-local check that this repo's Claude auto-memory points at the
version-controlled `.claude/memory/` folder. The script below does ALL the work (find repo
root → compute the path → reconcile `settings.local.json`). Your only job is to relay its
one-line result.

## Run the check

```!
powershell -NoProfile -ExecutionPolicy Bypass -File "${CLAUDE_SKILL_DIR}/ensure_repo_memory.ps1"
```

## Act on the result

Read the single STATUS line above:

- **`OK:`** — already configured. Continue silently (at most a one-line confirmation).
- **`FIXED:`** — the memory path was just set for **this machine**. Auto-memory is loaded at
  launch, so it won't take effect until the session restarts. **Stop here and tell the user to
  start a new session / reload the window before continuing any other work.** Do not proceed
  until they relaunch.
- **`SKIP:`** — not applicable in this directory (e.g. no `.claude` folder). Mention briefly and
  continue.

> Why machine-local: `autoMemoryDirectory` must be an absolute path, and it lives in the
> gitignored `settings.local.json` so each machine sets its own correct path. The memory
> *files* travel via git in `.claude/memory/`; this skill just re-points each machine at them.
