# diploma-cloud-cyber-umbrella

Umbrella (parent) repository for the **ICT50220 Diploma of Information Technology — Cloud
and Cybersecurity** development work.

**This is the entry point for the whole project.** Clone this repo first; the two working repos
(`diploma-cloud-cyber-content`, `diploma-cloud-cyber-website`) are cloned **inside** it and
**gitignored** here, and you always **launch Claude from this umbrella root** — never from a sub-repo.

This repo doesn't hold the deliverables. It is a thin **coordination layer** that sits
*above* the two working repos and holds the things they share: cross-repo `CLAUDE.md`
context, project-wide rules, project documentation (`docs/`), and a version-controlled, portable
Claude memory. Its job is to give you one place to launch Claude from when work spans both repos — and
to make all of that tooling travel between machines via git.

---

## Repository layout

```
diploma-cloud-cyber-umbrella/        ← this repo (the coordination layer)
├── .claude/                         ← shared Claude tooling (rules, skills, memory, settings)
├── CLAUDE.md                        ← project-wide context + working rules
├── README.md                        ← you are here
├── diploma-cloud-cyber-content/     ← WORKING REPO (cloned inside; gitignored here)
└── diploma-cloud-cyber-website/     ← WORKING REPO (cloned inside; gitignored here)
```

The two working repos are **independent git repositories** with their own remotes. The
umbrella **gitignores them entirely** (`.gitignore`), so it never tries to track their
files — each remains the sole owner of its own history.

| Repo | Purpose | Remote |
|---|---|---|
| `diploma-cloud-cyber-umbrella` | Coordination layer (this repo) | `…/diploma-cloud-cyber-umbrella` |
| `diploma-cloud-cyber-content` | Curriculum / assessment authoring (UoCs, clusters, validators) | `…/diploma-cloud-cyber-content` |
| `diploma-cloud-cyber-website` | YAT scenario website (Astro) | `…/diploma-cloud-cyber-website` |

---

## Getting set up (first time, any machine)

Clone the umbrella, then clone the two working repos **inside it**:

```bash
# 1. Clone the umbrella (the coordination layer)
git clone https://github.com/Digital-Initiatives-Kangan-Institute/diploma-cloud-cyber-umbrella.git
cd diploma-cloud-cyber-umbrella

# 2. Clone the working repos INTO the umbrella folder
git clone https://github.com/Digital-Initiatives-Kangan-Institute/diploma-cloud-cyber-content.git
git clone https://github.com/Digital-Initiatives-Kangan-Institute/diploma-cloud-cyber-website.git
```

That's it for files. The first time you open a Claude session here, the **self-healing
memory** step runs automatically (see below) — accept the workspace-trust prompt if shown,
then **relaunch once** so memory loads from the repo. After that, setup is permanent on
this machine.

> The folder names matter: the umbrella's `.gitignore` excludes the working repos by their
> exact directory names, so clone them with their default names.

---

## ⭐ The one rule: always launch Claude from the umbrella

**Open your Claude session with `diploma-cloud-cyber-umbrella` as the workspace root —
even when the actual editing happens inside a sub-repo.**

This isn't a preference; it's how Claude Code's discovery works. Claude resolves its
tooling relative to the folder you launch it in, and **some asset types are only discovered
from the launch directory** (they don't reach down into sub-folders). Launch from the
umbrella and you get the full toolkit; launch from inside a sub-repo and you silently lose
the umbrella's agents, settings, rules, and shared memory.

The two asset types that *do* cascade downward (skills and `CLAUDE.md`) still work when you
edit inside a sub-repo — so launching from the umbrella genuinely gives you **everything**:
the umbrella's shared layer, plus each sub-repo's own context as you touch its files.

---

## How it works

### 1. Cascading `CLAUDE.md`

Context is split so nothing is duplicated and each session loads only what's relevant:

- **`./CLAUDE.md` (umbrella)** — loaded automatically every session. Holds project-wide
  context and the standing **working rules** (no presumptive planning, TBD markers, no
  unilateral git operations, etc.).
- **`<sub-repo>/CLAUDE.md`** — holds that repo's specific instructions. It is **lazy-loaded
  automatically** the moment Claude reads any file inside that sub-repo. You don't need to
  ask for it; working in the repo pulls it in.

So the umbrella file is the always-on base layer, and each sub-repo's file layers on top
only when you're working there.

### 2. Division of labour — where each asset lives

Because of the discovery rules, assets are placed deliberately:

| Asset | Lives in | Active from the umbrella root? |
|---|---|---|
| **Project-wide `CLAUDE.md`** | umbrella root | ✅ always loaded |
| **Repo-specific `CLAUDE.md`** | each sub-repo | ✅ lazy-loaded when you read that repo's files |
| **Repo-specific skills** | the sub-repo's `.claude/skills/` | ✅ on-demand when working in that sub-repo |
| **Cross-project skills** | umbrella `.claude/skills/` | ✅ always |
| **Rules** | umbrella `.claude/rules/` (scoped with `paths:` globs) | ✅ always — target sub-repo files via globs |
| **Agents** | umbrella `.claude/agents/` | ⚠️ only from the umbrella (no nested discovery) |
| **Settings** | umbrella `.claude/settings.json` (+ machine-local `settings.local.json`) | ⚠️ only from the umbrella |
| **Memory** | umbrella `.claude/memory/` | ⚠️ only from the umbrella |

Rule of thumb: **skills and `CLAUDE.md` follow you down into the sub-repos; agents, settings,
rules, and memory stay at the top.** That asymmetry is the whole reason for "always launch
from the umbrella."

Every repo also carries the same standard `.claude/` skeleton (empty slots for all asset
types) so the structure is uniform and ready to use. See `.claude/README.md` for a full
reference of what each folder does.

### 3. Self-healing, version-controlled memory

Claude's persistent memory normally lives outside any repo (in Claude's config area), so it
never syncs between machines. Here it's relocated **into the repo** so it travels via git:

- **The memory files** live in `.claude/memory/` (committed, synced).
- **The redirect** is `autoMemoryDirectory` in `.claude/settings.local.json` — which is
  **machine-local and gitignored**, because the path is absolute and differs per machine.
- **The self-heal** is the vendored Node hook `.claude/hooks/ensure-repo-memory.mjs`, run
  automatically by a `SessionStart` hook (in `settings.json`, as `node .claude/hooks/ensure-repo-memory.mjs`
  — an identical command on Windows/macOS/Linux). On each machine it checks that
  `settings.local.json` points at this repo's `.claude/memory/`, and sets it if not —
  idempotently (a no-op once correct).

**New-machine flow:** clone → ensure **Node** is installed (the hook runs via `node`) → first umbrella
session → the hook sets the path and asks you to relaunch → relaunch once → memory now loads from the
repo. Every session after that, the hook just confirms `OK` silently.

> The hook is **vendored** (committed in-repo) rather than installed centrally, so it arrives
> with the clone — no per-machine install. **Node is a prerequisite** (not bundled with Claude
> Code's native installer). If the hook is ever improved, re-copy it into the repos that use it.

---

## TL;DR

1. Clone the umbrella, then clone the two working repos inside it.
2. **Always launch Claude from the umbrella root.**
3. Edit wherever you need — the right `CLAUDE.md` and skills follow you; the shared rules,
   agents, settings, and memory are always there because you launched from the top.
4. On a new machine, accept trust + relaunch once so portable memory loads.
