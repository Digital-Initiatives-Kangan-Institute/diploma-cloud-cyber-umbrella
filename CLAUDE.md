# CLAUDE.md — diploma-cloud-cyber-umbrella

**diploma-cloud-cyber-umbrella** is the coordination layer for building the **ICT50220 Diploma of IT
— Cloud & Cybersecurity** teaching and assessment materials. It holds no deliverables itself; it sits
above two independent working repos — **`diploma-cloud-cyber-content`** (curriculum, cluster
assessments, UoC mappings, validators) and **`diploma-cloud-cyber-website`** (the Astro "YAT" scenario
website the assessments are set in) — and version-controls the tooling they share: cross-repo
`CLAUDE.md` context, project-wide rules, and a portable, self-healing Claude memory. Its purpose is to
give one launch point when work spans both repos and to make that tooling travel between machines via
git.

**⭐ The one rule: always launch Claude with the umbrella as the workspace root** — even when editing
inside a sub-repo. Skills and `CLAUDE.md` cascade down to where you're working; agents, settings,
rules, and memory load *only* from the launch dir, so launching from a sub-repo silently loses the
shared layer.

## Read first — REQUIRED
- **[docs/INDEX.md](docs/INDEX.md) — read this every session.** It is the catalogue of all project
  documentation (the single docs surface for the umbrella *and* both sub-repos). Knowing what docs
  exist is mandatory; **load the relevant doc before doing related work** (assessment authoring,
  delivery planning, scenario/website work, lab-packs). This is the same index-then-load-on-demand
  pattern as MEMORY — but `docs/INDEX.md` is **not** auto-injected, so reading it is on you.
- [README.md](README.md) — what the project is, the layout, and the new-machine setup flow.
- [docs/doco-structure.md](docs/doco-structure.md) — the four doc surfaces and the `CLAUDE.md`⇄`MEMORY` split.
- [.claude/README.md](.claude/README.md) — reference for what each `.claude/` folder holds.

## Sub-repo context
Each sub-repo has its own `CLAUDE.md`, **auto-loaded (lazily) when Claude reads a file in that repo**:
[content](diploma-cloud-cyber-content/CLAUDE.md) · [website](diploma-cloud-cyber-website/CLAUDE.md).
(Plain links, never `@imports` — the cascade is lazy by design.)

## Cross-repo conventions
- The **content** repo authors the curriculum/assessments; the **website** renders the in-world YAT
  scenario those assessments reference.
- Scenario / intranet content is **in-world only** — no course/assessment/cluster meta-language (sole
  exception: the UoC footer on migrated docs).
- Each sub-repo owns its own history (own remote); the umbrella **gitignores** them entirely.
- Per-cluster system↔scenario mappings and delivery state live in **MEMORY**, not here (they change).

## Working discipline — assumptions & documentation

Never record anything as *decided / agreed / canonical* unless it was actively discussed **and**
explicitly approved. Flag anything not yet agreed with `[TBD — needs discussion: <what is open>]`
rather than writing it as settled.

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
repo (umbrella or either sub-repo) — on your own. Propose the exact command(s) + rationale and wait
for explicit approval; "go ahead" approves *that* operation only, not a standing licence. Read-only
git (`status`, `diff`, `log`, `show`, …) is always fine.

## Project status
Current delivery state is **not** recorded here (it goes stale) — see **MEMORY** (the per-cluster
assessment/delivery entries) and each sub-repo's `CLAUDE.md`.

## Where things live (audience decides)
- **`docs/`** — knowledge needed by **both humans and agents** (project, processes, conventions,
  scenario, website, lab-packs). The single docs surface for the umbrella *and* both sub-repos;
  catalogued in [docs/INDEX.md](docs/INDEX.md) (required reading, above). Sub-repos hold **no** docs.
- **MEMORY** (`.claude/memory/`, auto-loaded) — **LLM-only** durable knowledge: how Claude should
  behave here, and the per-cluster working state. Not for human consumption.
- **README** — user-facing framing + setup. **`.claude/README.md`** — `.claude/` asset reference.
