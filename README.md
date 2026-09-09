# courseware-development umbrella

A **course-agnostic layer for developing courseware** — the process, tooling, conventions, and a
portable, self-healing Claude memory for authoring any qualification's teaching and assessment
materials. It holds **no deliverables of its own**; those live in **per-semester working sub-repos**
cloned inside it (and gitignored here).

**This is the entry point for the whole project.** Clone this repo first; the working repos are cloned
**inside** it and **gitignored** here, and you always **launch Claude from this umbrella root** — never
from a sub-repo. Its job is to give you one launch point when work spans repos, and to make the shared
process + tooling travel between machines via git.

**Design intent — any course.** A Diploma of IT, a Cert III in IT, a Cert IV in Nursing should each be
able to plug their sub-repos into this umbrella and reproduce the *same* authoring process. Everything
here is process and concept; everything course- or semester-specific lives in a sub-repo.

---

## Currently hosting

The **ICT50220 Diploma of IT — Cloud & Cybersecurity**, split by semester into a content repo
(curriculum/assessment authoring) + a website repo (the Astro in-world scenario site). Each semester's
two repos are self-contained; **semesters do not share scenario continuity.**

| Semester | Content repo | Website repo |
|---|---|---|
| S1 — Cloud | `diploma-cloud-cyber-content-s1` | `diploma-cloud-cyber-website-s1` |
| S2 — Cyber | `diploma-cloud-cyber-content-s2` | `diploma-cloud-cyber-website-s2` |

## Repository layout

```
<umbrella>/                       ← this repo (the course-agnostic layer)
├── .claude/                      ← shared tooling: skills + validators, rules, memory, settings, hooks
├── docs/                         ← process + format standards + the current course's docs (start at docs/INDEX.md)
├── scripts/                      ← the shared engine: deck builder, workbook/docx helpers, mapping + coverage generators, tests
├── CLAUDE.md                     ← umbrella context + working rules
├── README.md                     ← you are here
├── diploma-cloud-cyber-content-s1/   ← WORKING REPO (cloned inside; gitignored here)
├── diploma-cloud-cyber-website-s1/   ← WORKING REPO
├── diploma-cloud-cyber-content-s2/   ← WORKING REPO
└── diploma-cloud-cyber-website-s2/   ← WORKING REPO
```

The working repos are **independent git repositories** with their own remotes. The umbrella
**gitignores them** by wildcard (`/diploma-cloud-cyber-content*/`, `/diploma-cloud-cyber-website*/`), so
it never tracks their files — each remains the sole owner of its own history.

**The umbrella ⇄ sub-repo boundary:**
- **Umbrella = common process + tooling (course-agnostic):** the step→gate run-sheets and format
  standards (`docs/` — catalogued in [docs/INDEX.md](docs/INDEX.md), with the one-page overview in
  [docs/big-picture.md](docs/big-picture.md)); the authoring skills + validators (`.claude/skills/`);
  the shared engine (`scripts/` — deck builder, workbook/docx helpers, mapping + coverage generators);
  institutional templates, project-wide rules, and portable memory. The reproducible machinery.
- **Sub-repo = the specifics:** the units/clusters, the generated assessment instruments (guided
  workbooks with practice twins — see [docs/assessment-workbook-format.md](docs/assessment-workbook-format.md)),
  mappings, the scenario website, and the semester-specific generators the engine drives.

---

## Getting set up (first time, any machine)

Clone the umbrella, then clone the semester working repos **inside it** (with their exact directory
names — the umbrella's `.gitignore` excludes them by the `…-content*` / `…-website*` wildcard):

```bash
# 1. Clone the umbrella (the coordination layer)
git clone https://github.com/Digital-Initiatives-Kangan-Institute/diploma-cloud-cyber-umbrella.git
cd diploma-cloud-cyber-umbrella

# 2. Clone the semester working repos INTO the umbrella folder (the semesters you're working on)
git clone https://github.com/Digital-Initiatives-Kangan-Institute/diploma-cloud-cyber-content-s1.git
git clone https://github.com/Digital-Initiatives-Kangan-Institute/diploma-cloud-cyber-website-s1.git
git clone https://github.com/Digital-Initiatives-Kangan-Institute/diploma-cloud-cyber-content-s2.git
git clone https://github.com/Digital-Initiatives-Kangan-Institute/diploma-cloud-cyber-website-s2.git
```

The first time you open a Claude session here, the **self-healing memory** step runs automatically
(see below) — accept the workspace-trust prompt if shown, then **relaunch once** so memory loads from
the repo. After that, setup is permanent on this machine.

---

## ⭐ The one rule: always launch Claude from the umbrella

**Open your Claude session with the umbrella as the workspace root — even when the actual editing
happens inside a sub-repo.** Skills and `CLAUDE.md` cascade down into the sub-repos; agents, settings,
rules and memory are only discovered from the launch directory (the table below). Launching from a
sub-repo silently loses the shared layer.

---

## How it works

### 1. Cascading `CLAUDE.md`

- **`./CLAUDE.md` (umbrella)** — loaded automatically every session. Umbrella context + the standing
  **working rules** (no presumptive planning, TBD markers, no unilateral git operations, etc.).
- **`<sub-repo>/CLAUDE.md`** — that repo's specific instructions. **Lazy-loaded** the moment Claude
  reads any file inside that sub-repo.

The umbrella file is the always-on base layer; each sub-repo's file layers on top when you work there.

### 2. Division of labour — where each asset lives

| Asset | Lives in | Active from the umbrella root? |
|---|---|---|
| **Umbrella `CLAUDE.md`** | umbrella root | ✅ always loaded |
| **Repo-specific `CLAUDE.md`** | each sub-repo | ✅ lazy-loaded when you read that repo's files |
| **Process skills + validators** (the shared toolchain) | umbrella `.claude/skills/` | ✅ always |
| **Shared engine** (deck builder, workbook/docx helpers, mapping + coverage generators) | umbrella `scripts/` (run with its `.venv`) | ✅ always |
| **Semester-specific generators** | the sub-repo's `scripts/` (driven by the umbrella engine) | ✅ on-demand when working there |
| **Rules** | umbrella `.claude/rules/` (scoped with `paths:` globs) | ✅ always — target sub-repo files via globs |
| **Agents** | umbrella `.claude/agents/` | ⚠️ only from the umbrella (no nested discovery) |
| **Settings** | umbrella `.claude/settings.json` (+ machine-local `settings.local.json`) | ⚠️ only from the umbrella |
| **Memory** | umbrella `.claude/memory/` | ⚠️ only from the umbrella |

That asymmetry is the whole reason for the one rule. The course-agnostic toolchain lives in the
umbrella so any semester of any course reuses it unchanged; only course/semester-specific artefacts and
generators live in the sub-repos.

### 3. Self-healing, version-controlled memory

Claude's persistent memory normally lives outside any repo (in Claude's config area), so it never syncs
between machines. Here it's relocated **into the umbrella** so it travels via git:

- **The memory files** live in `.claude/memory/` (committed, synced).
- **The redirect** is `autoMemoryDirectory` in `.claude/settings.local.json` — **machine-local and
  gitignored**, because the path is absolute and differs per machine.
- **The self-heal** is the vendored Node hook `.claude/hooks/ensure-repo-memory.mjs`, run automatically
  by a `SessionStart` hook. On each machine it checks that `settings.local.json` points at this repo's
  `.claude/memory/`, and sets it if not — idempotently (a no-op once correct).

**New-machine flow:** clone → ensure **Node** is installed (the hook runs via `node`) → first umbrella
session → the hook sets the path and asks you to relaunch → relaunch once → memory now loads from the
repo. Every session after that, the hook just confirms `OK` silently.

---

## TL;DR

1. Clone the umbrella, then clone the semester working repos inside it.
2. **Always launch Claude from the umbrella root.**
3. Edit wherever you need — the right `CLAUDE.md` and skills follow you; the shared rules, agents,
   settings, and memory are always there because you launched from the top.
4. On a new machine, accept trust + relaunch once so portable memory loads.
