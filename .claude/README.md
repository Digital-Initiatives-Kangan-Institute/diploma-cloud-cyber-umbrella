# `.claude/` — capabilities reference

This is the **canonical reference** for what Claude Code can hold at the project level — the
single place (across the umbrella and both sub-repos) that explains each folder/file. The repo
carries a **uniform skeleton**: folders that aren't in use yet are held open by a `.gitkeep` and
are ready to fill (drop a skill in `skills/`, a rule in `rules/`, etc.). Live assets currently in
use: `settings.json` (incl. the SessionStart memory hook), `hooks/ensure-repo-memory.mjs`,
`rules/`, and `memory/`. `settings.example.json` is an inert catalogue of keys you can copy into
`settings.json`.

> Scope note: this is the **project / umbrella** layer. There is also a **user layer**
> at `~/.claude/` (settings, skills, agents, rules, keybindings, CLAUDE.md) that applies
> across *all* projects and is not part of this repo.

## What lives here

| Path | What it is | Synced (git)? |
|------|------------|---------------|
| `settings.json` | Shared project settings (model, permissions, env, hooks, statusLine…) | ✅ committed |
| `settings.local.json` | Personal project settings (overrides shared) | ❌ gitignored |
| `rules/` | Path-scoped instruction files (modern alternative to nested CLAUDE.md) | ✅ committed |
| `skills/<name>/SKILL.md` | Custom skills (invokable as `/<name>`, or auto-invoked) | ✅ committed |
| `agents/<name>.md` | Custom subagents Claude can delegate to | ✅ committed |
| `agent-memory/<agent>/` | Project-scoped persistent memory for a subagent | ✅ committed |
| `agent-memory-local/<agent>/` | Machine-local subagent memory | ❌ gitignored |
| `output-styles/<name>/` | Output style definitions (adjust system-prompt tone/format) | ✅ committed |
| `hooks/` | Hook scripts referenced from `settings.json` | ✅ committed |
| `status-line.md` | Custom status line script (alternative to `settings.statusLine`) | ✅ committed |

## Related files OUTSIDE `.claude/` (at the repo root)

| Path | What it is |
|------|------------|
| `../CLAUDE.md` | Project instructions (auto-loaded; the main coordination file) |
| `../CLAUDE.local.md` | Personal project instructions (gitignored) |
| `../.mcp.json` | Project-scope MCP servers (shared) |
| `../plugins/` | Self-contained plugins (bundle skills/agents/hooks/mcp together) |

## Loading & precedence (quick reference)

- **Settings** (highest→lowest): managed → CLI flags → `settings.local.json` → `settings.json` → `~/.claude/settings.json`
- **Skills/Agents**: managed → user (`~/.claude/`) → project (`.claude/`) → plugins
- **CLAUDE.md**: org → user → repo-root CLAUDE.md (or `.claude/CLAUDE.md`) → `CLAUDE.local.md` → path-matched `rules/`
