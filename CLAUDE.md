# Umbrella / Coordination Instructions

> This is the **parent (umbrella) repo** for the Diploma Cloud Cyber project. It exists
> to hold cross-repo coordination context and Claude Code tooling, and to version-control
> them so they travel between machines. The actual deliverables live in two nested repos
> that this repo deliberately **gitignores**:
>
> - `diploma-cloud-cyber-content/`  — curriculum / assessment authoring (own remote)
> - `diploma-cloud-cyber-website/`  — Astro scenario website (own remote)
>
> Open Claude here, at the umbrella root, when work needs coordination across both repos.

This file holds what is **common across the whole project**. Each sub-repo keeps its own
`CLAUDE.md` for repo-specific context, so nothing is duplicated and each session loads only
what's relevant.

## Sub-repo context

Each sub-repo has its own `CLAUDE.md`, **auto-loaded when Claude reads a file in that repo**:
[content](diploma-cloud-cyber-content/CLAUDE.md) · [website](diploma-cloud-cyber-website/CLAUDE.md).

## How CLAUDE.md works (so future-you remembers)

- This file is loaded automatically when Claude runs with this folder in scope.
- At launch, Claude reads CLAUDE.md by walking from the working directory **upward** toward
  home. It also **lazily** loads a nested sub-repo's `CLAUDE.md` the moment it reads a file in
  that repo — so sub-repo context arrives automatically when (and only when) it's relevant.
- `CLAUDE.local.md` (same dir) is appended after this file but is **gitignored** (personal).

## Project context

<!-- Fill in: what the diploma project is, who it's for, the relationship between the
     content repo and the website repo, and any cross-repo invariants. -->

## Cross-repo conventions

<!-- e.g. shared naming, how content maps to website pages, build/deploy ordering. -->

## Working agreements with Claude — standing rules

Standing rules for how I (Claude) operate across this project — the umbrella repo and both
sub-repos. Loaded at the start of every session from the umbrella root.

### Rule 1 — No presumptive planning

I do **not** record anything as *decided*, *locked in*, *finalised*, *agreed*, *canonical*,
or any equivalent unless **both** of the following are true:

1. The item has been actively discussed with Tim in conversation.
2. Tim has explicitly approved it.

This applies to — but is not limited to — phases, schedules, sequencing, priorities, scope,
scope exclusions, naming conventions, folder structures, technology choices, tool choices,
cluster composition, audit methodology, assessment strategies, validation approaches, and
anything else a future reader of the document might treat as a project decision.

If something is *my own suggestion* that hasn't been through that loop, it is not a decision.
It is a proposal at best, and must be visibly marked as such (see Rule 2).

### Rule 2 — TBD marker for unapproved items

If I think something is worth capturing but it has **not** yet been discussed and approved by
Tim, I flag it clearly with **TBD (to be discussed)**. Examples of acceptable forms:

- Inline: `**TBD** — proposed sequencing: audit before build.`
- Section heading: `## TBD items` collecting all open proposals in one place.
- Table column: an explicit `Status` column with `TBD` as a value.

Whichever form I use, the TBD must be visible at a glance — not buried in a paragraph or only
implied by context.

### Rule 3 — When in doubt, ask or mark TBD

If I'm unsure whether something counts as "agreed", it doesn't. Either:

- ask Tim in chat before recording it, or
- record it as TBD.

I do not optimise for the appearance of decisiveness by presenting proposals as if they were
decisions.

### Rule 4 — Retroactive corrections

If I notice a previous document of mine contains items I treated as decisions when they were
actually my proposals, I flag them. I do not silently rewrite them, but I do clearly note the
issue (either at the top of the document or against the specific item).

### Rule 5 — No unilateral git operations

I do **not** run any git command that changes repository state — in **any** repo (the umbrella
or either sub-repo) — unless Tim has explicitly approved that specific operation. This includes
— but is not limited to — `git add`, `git commit`, `git restore`, `git checkout`, `git reset`,
`git rm`, `git mv`, `git branch`, `git merge`, `git rebase`, `git stash`, `git push`, `git pull`,
`git fetch`, `git tag`, `git config` (writing values), `git clean`, and any subcommand that
mutates the working tree, index, refs, or config.

Read-only commands (`git status`, `git diff`, `git log`, `git show`, `git config --get`,
`git ls-files`, etc.) are fine to run whenever they help me answer Tim's question.

If I think a state-changing git operation is warranted, I **suggest** it in chat — naming the
exact command(s) I would run — and wait for explicit approval before executing. If Tim says "go
ahead" or equivalent for that specific suggestion, that's approval for that operation only, not
a standing licence to keep running git commands.

If I'm uncertain whether something counts as a state change, I treat it as a state change and
ask first.

### Origin of these rules

- Rules 1–4 recorded on 2026-05-15 after Tim observed that I had presumptively drafted a project
  plan (phases, critical path, sequencing) and presented it as if it had been agreed, when in
  fact none of it had been discussed with him.
- Rule 5 added on 2026-05-15 to extend the same "explicit-approval" principle to git operations.
- Lifted from `diploma-cloud-cyber-content/CLAUDE.md` to this umbrella file (project-wide scope)
  on 2026-06-14, so the rules govern every repo rather than just the content repo.
