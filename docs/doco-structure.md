# Documentation Structure

This project uses **four distinct documentation surfaces**. Each has a different audience, lifespan,
and update cadence. Putting content in the wrong place is a slow-burning cost: the wrong people read
it (or miss it), it goes stale, or it crowds out what the surface is actually for.

This document explains what belongs where, when to update each, and the conventions that keep them
coherent.

## Everything we write is the current working approach, not law

This governs **all four surfaces** below, and it is the frame everything else in this document sits in.

What we record is *what we do now, and why* — the best approach we have at the time of writing. It is not
a constitution, and nothing here is settled beyond revision. A standard that stops serving the work gets
changed; that is the system working, not the system failing.

**So write it that way.** Reach for *"the current approach"*, *"what we do now"*, *"the working
assumption"*, *"the ambition is…"*. Avoid *"the rule"*, *"never"*, *"must"*, *"invariant"*,
*"non-negotiable"* — absolutist framing reads as a prohibition, and a prohibition invites contorting real
work to defend a line that was only ever a preference.

**Prefer an ambition to a prohibition.** Where something genuinely is worth protecting, name it as
something we aim at rather than something we forbid — *"the evergreen ambition: instruments avoid a
hard-coded URL wherever that costs nothing"*, not *"instruments must never carry a URL"*. The ambition
tells you what good looks like **and** leaves room to not force the point when the cost lands on the
student or the work. A prohibition only does the first.

**The exception — constraints we have no capability to change.** Some limits shouldn't be softened: the
AWS Academy lab refuses IAM creation; CloudFormation rejects a non-ASCII resource description; the training
package requires every PC/PE/KE/FS/AC to be assessed somewhere. State those firmly and plainly — hedging a
hard external fact just misleads the next reader into wasting a day on it.

**The test is two questions, and a hard constraint has to pass both.** Is this someone else's constraint
rather than a position we hold? **And — if we needed it changed, could we change it?** Only a *no* to the
second makes it hard. Externally imposed is not the same as immovable: an outside constraint we could
negotiate, swap out, or work around is still a working approach. The institutional template being the
format-of-record is Kangan's call, but it is a call that could be revisited — so it is written as what we
currently do. The lab refusing IAM creation is not revisitable by us, so it is written as a wall.

**This principle is itself a current working approach, not law.**

## The four surfaces

### 1. `/README.md` — for humans landing on the repo

**Audience.** Someone who just clicked through to the repository. A prospective user, a curious
passer-by, a future contributor. No prior context.

**Purpose.** Answer the first-ninety-seconds questions: What is this? Is it for me? What's its status
(usable / in development / abandoned)? How do I install or try it? Where do I learn more?

**Tone.** Big-picture, plain language, skim-friendly. One browser tab, no scrolling fatigue.

**Does NOT belong here.** Architecture detail (→ `docs/`), implementation specifics, working notes,
LLM agent instructions (→ `CLAUDE.md`).

**Cadence.** Stable. Edit when something *user-facing* changes (status, positioning, install steps).

### 2. `/CLAUDE.md` — the always-loaded operating rules for LLM agents

**Audience.** Claude (and other LLM agents) picking up a task here, with no memory of prior sessions.

**Mechanics that define it.** `CLAUDE.md` is loaded **in full, every session**, and read as
instructions to obey. Every token is paid on every session — so it must stay **small and
high-leverage**; bloat dilutes the signal and gets load-bearing rules missed.

**Purpose.** The small set of **always-on, imperative** rules + orientation:
- what the project is, in one paragraph;
- where to read first / the repo's layout;
- load-bearing **principles** that constrain *every* task;
- the **out-of-scope** list, so the agent never proposes deliberately-excluded things;
- broad project-specific conventions;
- **pointers** (not duplicated content) to `MEMORY` and `docs/`.

**Does NOT belong here.** Situational knowledge that isn't relevant every session (→ `MEMORY`),
generic language/framework advice, deep detail (→ `docs/`), user-facing framing (→ `README`).

**Cadence.** Stable. A rule lands here when it must bind **every** session — often by *graduating up*
from `MEMORY` (see the split below). Don't let it grow into a wiki.

### 3. `MEMORY.md` (+ `.claude/memory/`) — the agent's accumulated durable knowledge

**Audience.** Claude, across sessions. The **index** (`MEMORY.md`, one line per memory) is loaded
every session; the **topic files** are pulled in **on demand** when a task touches them.

**Mechanics that define it.** Because only the index is always-loaded and the detail is lazy-loaded,
`MEMORY` can hold a **large, growing** body of knowledge cheaply — the situational counterpart to
CLAUDE.md's always-on rules.

**Purpose.** Durable, **declarative** decisions / agreements / facts — *"principles, not state":*
- durable decisions and the **why** behind them;
- user preferences and agreements;
- component- or area-specific facts you should **recall when working there**.

**Does NOT belong here.** Universal rules that bind *every* session (→ `CLAUDE.md`); **ephemeral or
repo-derivable state** — paths, "what's built", commit SHAs (git/code already holds it; it goes stale
on creation); deep architectural rationale (→ `docs/`).

**Cadence.** Living. Claude writes to it as decisions accrue — one focused topic file per memory, a
one-line entry in `MEMORY.md` so it's discoverable.

### 4. `docs/` — the technical / knowledge wiki

**Audience.** Anyone working on the project's architecture, design, or substance — humans and agents
alike.

**Purpose.** The full record. Architecture, decisions, rationale, plans, post-mortems, glossaries —
the place where deep *why* lives. (For a non-software project, the same surface holds the project's
substantive knowledge base; the role is identical even if the content isn't code.)

**Structure.**
- **`INDEX.md`** — entry point: every document with a one-line description, organised by category.
- **Content documents** — one focused topic per file, kebab-case (`schema-design.md`).

**Does NOT belong here.** Agent instructions (`CLAUDE.md`), user-facing framing (`README.md`),
throwaway scratch notes (if it isn't worth indexing, it isn't worth keeping).

**Cadence.** Active — documents are added/updated as topics arise; history is preserved (supersede,
don't delete).

## The `CLAUDE.md` ⇄ `MEMORY` split (the LLM-facing division)

Both are for the agent, so the boundary matters. Two axes settle it:

- **Always-on vs situational.** `CLAUDE.md` is loaded in full *every* session → only universal,
  every-task content earns a place (keep it small). `MEMORY` is indexed-now / detail-on-demand →
  the larger body of *sometimes-relevant* durable knowledge.
- **Imperative vs declarative.** `CLAUDE.md` = rules you *apply* ("do X, never Y, read Z first").
  `MEMORY` = knowledge you *recall* ("we chose X because Y; the user prefers Z").

**The graduation flow:** a decision is made in conversation → if durable, it's recorded in `MEMORY`
→ **if it must bind every session, it graduates up into `CLAUDE.md`.** If `CLAUDE.md` accumulates
situational detail, that **demotes down into `MEMORY`.** `CLAUDE.md` trends small-and-universal;
`MEMORY` accumulates-and-specialises.

## Quick decision guide

| Question | ⇒ goes in |
|---|---|
| Will a non-developer visitor want to see this? | `README.md` |
| Is it a rule/constraint that must steer **every** agent session? | `CLAUDE.md` |
| Is it a durable decision/agreement/fact to **recall when working on a specific thing**? | `MEMORY` (topic file + index line) |
| Is it architectural detail, decision rationale, or a plan? | `docs/` (and indexed in `INDEX.md`) |
| Is it ephemeral or derivable from the repo (paths, "what's built")? | Don't write it — git/code has it |
| Useful for the *current task only*? | Don't write it — keep it in the conversation |

If content seems to belong in two places, prefer the more durable/detailed surface (`docs/` or
`MEMORY`) and **link** to it from the always-on ones (`README`, `CLAUDE.md`), which stay short.

## Conventions for `docs/` documents

- **Filename:** kebab-case, descriptive, stable (`schema-design.md`, not `notes-2026-04.md`).
- **First line:** an `# H1 Title` matching the filename.
- **Second block:** a one-paragraph summary — what shows in a preview pane and gets quoted in `INDEX.md`.
- **Cross-references:** relative links to other docs (`[schema design](schema-design.md)`); leading
  slash to root files (`[CLAUDE.md](../CLAUDE.md)`).
- **Index it.** Add a one-line entry to `INDEX.md`. An un-indexed document is invisible.
- **Capture the *why*.** A doc that says *what* without *why* is obsoleted by the first strong
  counter-argument. The *why* is what makes it durable.
- **Don't delete; supersede.** Leave a superseded doc in place with a note linking forward.

## Why four surfaces and not one

A single `README` is too long for visitors or too shallow for contributors. `CLAUDE.md` alone either
pulls in agent-irrelevant marketing or omits depth. `MEMORY` exists because an agent needs durable
recall that *accumulates* without bloating the always-loaded rules. `docs/` without an entry point is
invisible. Four surfaces, each focused on one audience and one cadence, linking where helpful: the
cost is a little discipline about what goes where; the benefit is each surface stays useful for the
long haul.
