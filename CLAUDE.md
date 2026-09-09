# CLAUDE.md — courseware-development umbrella

This umbrella is a **course-agnostic layer for developing courseware** — the *process*, *tooling*, and
*conventions* for authoring a qualification's teaching and assessment materials, plus a portable,
self-healing Claude memory. It holds **no deliverables of its own**: they live in **per-semester working
sub-repos** cloned inside it (and gitignored here). The umbrella sits above them, giving one launch point
and a shared toolkit that travels between machines via git.

**Design intent — any course, any qualification.** A Diploma of IT, a Certificate III in IT, a
Certificate IV in Nursing should each be able to plug their sub-repos into this umbrella and reproduce
the *same* authoring process. Everything here is **process and concept**; everything course- or
semester-specific lives in a sub-repo. When adding to the umbrella, keep it generic — if a thing only
makes sense for one course or one semester, it belongs in that sub-repo.

**Currently hosting:** the **ICT50220 Diploma of IT — Cloud & Cybersecurity**, split by semester into a
content repo (curriculum/assessment authoring) + a website repo (the Astro in-world scenario site):

| Semester | Content repo | Website repo |
|---|---|---|
| S1 — Cloud | `diploma-cloud-cyber-content-s1` | `diploma-cloud-cyber-website-s1` |
| S2 — Cyber | `diploma-cloud-cyber-content-s2` | `diploma-cloud-cyber-website-s2` |

Each semester's two repos are **self-contained**; semesters do **not** share scenario continuity.

**⭐ The one rule: always launch Claude with the umbrella as the workspace root** — even when editing
inside a sub-repo. Skills and `CLAUDE.md` cascade down to where you're working; agents, settings,
rules, and memory load *only* from the launch dir, so launching from a sub-repo silently loses the
shared layer.

## Read first — REQUIRED
- **[docs/big-picture.md](docs/big-picture.md)** — the whole factory in one page (UoCs → assessments →
  practice mirrors → teaching → delivery). Thirty seconds; read it before anything else.
- **[docs/INDEX.md](docs/INDEX.md) — read this every session.** It is the catalogue of all process +
  course documentation (the single docs surface for the umbrella *and* the sub-repos). Knowing what docs
  exist is mandatory; **load the relevant doc before doing related work** (assessment authoring,
  delivery planning, scenario/website work, lab-packs). This is the same index-then-load-on-demand
  pattern as MEMORY — but `docs/INDEX.md` is **not** auto-injected, so reading it is on you.
- [README.md](README.md) — what the umbrella is, the layout, and the new-machine setup flow.
- [docs/doco-structure.md](docs/doco-structure.md) — the doc surfaces and the `CLAUDE.md`⇄`MEMORY` split.
- [.claude/README.md](.claude/README.md) — reference for what each `.claude/` folder holds.

## The umbrella ⇄ sub-repo boundary
- **Umbrella = common process + tooling (course-agnostic).** The step→gate run-sheets and format
  standards (`docs/`); the authoring skills, validators, and shared engine (`.claude/skills/`);
  institutional templates; project-wide rules; and the portable memory (principles + working state).
  This is the reproducible machinery — the same for any course plugged in.
- **Sub-repo = the specifics (this course, this semester).** The units of competency / clusters,
  assessment instruments, mappings, the scenario website, and any **semester-specific generators**. A
  content repo authors the curriculum/assessment; its paired website renders the in-world scenario the
  assessments reference.
- Scenario / intranet content is **in-world only** — no course/assessment/cluster meta-language (applies
  wherever a course uses a scenario site; sole exception: the UoC footer on migrated docs).
- Each sub-repo owns its own history (own remote); the umbrella **gitignores** them
  (`/diploma-cloud-cyber-content*/`, `/diploma-cloud-cyber-website*/`).
- Per-semester working state (system↔scenario mappings, delivery state) lives in **MEMORY**, namespaced
  per semester — not here (it changes).

## Sub-repo context
Each sub-repo has its own `CLAUDE.md`, **auto-loaded (lazily) when Claude reads a file in that repo**
(plain links, never `@imports` — the cascade is lazy by design). Launched from the umbrella, you get the
shared layer plus whichever semester's context you're currently touching.

## Working discipline — assumptions & documentation

**Everything we write here is the current working approach, not law.** Docs, standards, conventions and
memory record what we do *now*, open to change when a better path shows up — write *"the current
approach"*, not *"never"* / *"must"* / *"invariant"*. State firmly only a constraint we have no
capability to change (e.g. the Learner Lab refusing IAM creation). Full principle:
[docs/doco-structure.md](docs/doco-structure.md).

Never record anything as *decided / agreed / canonical* unless it was actively discussed **and**
explicitly approved. Flag anything not yet agreed with `[TBD — needs discussion: <what is open>]`
rather than writing it as settled. A thing tried **once** is not a convention — say it is being
trialled, name where, and don't propagate it.

**Documentation is never grounds for declining an idea.** This is the harm the rule above exists to
prevent: Tim proposes improvements to how the work is done, and locking language written today becomes
a later session **quoting the docs back at him** — *"it is written that we do it this way"* — as a
reason not to consider his idea. What is written records how we **currently** understand the job and
**currently** approach it; new understanding, methods and tooling are always possible. When a proposal
touches something already written down, treat the doc as **context, never as an objection**: say what
it says and why, then keep weighing the idea on its merits.

**No check, constraint or finding is ever decisive or a dead end.** Never frame a test, lookup or
investigation as settling a question or blocking the work — *"this decides it"*, *"this means we
can't proceed"*. A check yields **one input**, weighed with everything else. At most it leans us
toward an option or rules out one particular way of doing a thing; the goal stays reachable and there
is room to be creative about how. The framing is always: *we'll check this, and it informs how we
proceed.*

- Capture only what was discussed and agreed; don't extrapolate a principle into unraised specifics.
- Flag open questions explicitly with `[TBD — …]` so a later session picks them up deliberately.
- Distinguish archived/historical material from in-conversation decisions.
- Smaller is better — three faithfully-captured points beat ten padded ones.
- Self-correct — if you catch yourself writing beyond what was discussed, remove it or mark it `[TBD]`.
- Docs describe the **current state only**; what-was lives in git history, not in prose.

## Git safety — destructive operations require explicit approval

Never run a destructive git operation without explicit, in-conversation approval for that specific
action — regardless of any settings allowlist or prior approval. Destructive includes: force push,
hard reset, discarding uncommitted changes, `git clean -f`, force-deleting branches, history rewrites
(`rebase`, `amend` on pushed commits, `filter-branch`/`filter-repo`), dropping stashes, deleting tags,
and any `--no-verify` / `--no-gpg-sign` bypass. Force-pushing a protected branch (`main`/`master`/
`release/*`) must be refused outright. When unsure whether something can lose work or rewrite history,
treat it as destructive and ask.

**Non-destructive git too (this project's convention):** do **not** run state-changing git — in *any*
repo (umbrella or any sub-repo) — on your own. Propose the exact command(s) + rationale and wait
for explicit approval; "go ahead" approves *that* operation only, not a standing licence. Read-only
git (`status`, `diff`, `log`, `show`, …) is always fine.

## Project status
Current per-semester delivery state is **not** recorded here (it goes stale) — see **MEMORY** (the
per-cluster assessment/delivery entries) and each sub-repo's `CLAUDE.md`.

## Where things live (audience decides)
- **`docs/`** — knowledge needed by **both humans and agents** (process, conventions, format standards,
  and course/scenario/website/lab-pack documentation). The single docs surface for the umbrella *and*
  the sub-repos; catalogued in [docs/INDEX.md](docs/INDEX.md) (required reading, above). Sub-repos hold
  **no** docs.
- **MEMORY** (`.claude/memory/`, auto-loaded) — **LLM-only** durable knowledge: how Claude should
  behave here (course-agnostic principles), and the per-semester working state (namespaced). Not for
  human consumption.
- **README** — user-facing framing + setup. **`.claude/README.md`** — `.claude/` asset reference.
