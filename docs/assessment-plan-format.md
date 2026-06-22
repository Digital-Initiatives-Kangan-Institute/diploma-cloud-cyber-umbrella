# Assessment-plan format — standard

**Audience:** humans and LLM agents authoring a cluster's assessment plan. Paths are relative to the
`diploma-cloud-cyber-content/` repo root.

A cluster's assessment plan (`<cluster>/assessments/assessment_plan.md`) is the **authored source of
truth** for that cluster's assessments: the AT structure, what each AT covers of the UoC, and what each AT
needs from the scenario. It is **one per cluster** — the cross-scenario view (all clusters' coverage + the
full scenario-requirements register) is *derived by tooling* reading across the per-cluster plans, not
hand-maintained (see [process-assessment.md](process-assessment.md) §4 and the scenario plan).

This standard fixes the plan's structure so two checks can run against it:

- **`validate-assessment-plan` (linter — deterministic):** the required sections/fields are present and the
  references are well-formed.
- **UoC-coverage validator:** every item in the cluster's `consolidated_uoc.md` is referenced by at least
  one AT's **UoC coverage** (reuses the canonical `[UNIT SEC num]` tag machinery).

A third check lives with the scenario plan — the **scenario cross-check** reads every `SR-*` declared here
and confirms the scenario plan satisfies it.

## Conventions

- **UoC references** use the canonical tag `[<UNIT> <SECTION> <numbering>]` — e.g. `[ICTCLD504 PC 1.1]`,
  `[ICTCLD504 KE 4]`, `[ICTCLD504 FS Reading]`. Ranges/lists allowed (`[ICTCLD504 PC 1.1–1.6]`,
  `[ICTCLD504 PC 2.1, 2.3]`) — the same parser the AT validators use expands them. Tags must appear
  **unwrapped** (not inside backticks) to count. This is the **authoritative coverage notation** — the
  older backtick form (`` `504 PC 1.1` ``) is prose only and is **not** counted.
- **Scenario-requirement IDs** are `SR-<CLUSTER>-NN` — cluster-scoped so they stay unique when the scenario
  cross-check aggregates across clusters (e.g. `SR-CL3-01`). Each is declared once in the register (§6) and
  referenced from the AT that needs it (§3).

## Required sections (in order)

The linter requires these headings and their key fields. Prose within each is free.

1. **Header banner** — title `# <cluster> — Cluster Assessment Plan`; a `> **STATUS:** …` line; and a
   **Scenario binding** line naming the scenario this plan maps to and linking the scenario plan.
2. **`## 1. Integration approach`** — how the cluster's units form one engagement (the thread; the
   approval moments; how KE is evidenced).
3. **`## 2. Scenario`** — the vehicle and baseline this cluster assesses on, and the provided-vs-authored
   boundary. (Narrative; the testable scenario needs are the `SR-*` in §3/§6.)
4. **`## 3. Assessment structure`** — the AT table, then **per AT** a block containing, as labelled fields:
   - **Mode** (Individual / Group) and **Format** (the parts) and **Unit focus**;
   - **UoC coverage:** the `[UNIT SEC num]` items this AT evidences *(authoritative — the UoC-coverage
     validator reads these)*;
   - **Scenario requirements:** the `SR-*` IDs this AT depends on *(the scenario cross-check reads these)*.
5. **`## 4. Provenance`** — reuse basis (brownfield) and new authoring; `author-fresh` noted where greenfield.
6. **`## 5. Coverage verification`** — the human-readable proof that nothing is unassessed: the per-section
   distribution checks (PE/KE placed) and a one-line verification statement. *(A rollup view of §3's
   coverage; may be generated. The validator's authoritative source is §3's per-AT UoC coverage.)*
7. **`## 6. Scenario requirements register`** — one row per `SR-*`: **ID · description (the condition the
   scenario must enable) · AT(s) that need it · AC link**. The **AC link** names any UoC Assessment
   Condition item the requirement subsumes (`[<UNIT> AC n]`), so the scenario/lab providing the `SR-*` also
   discharges that AC. Requirements with no AC are narrative-only conditions (stakeholders, baseline state,
   constraints) — that is expected.
8. **`## 7. Worklist`** — modifications / additions / authoring to be done.
9. **`## 8. Open questions / TBDs`** — choices awaiting decision (mark `[TBD — …]`).
10. **`## Changelog`** — dated entries; current-state prose above, history here.

## Scenario requirements — what to capture

For each AT, ask: *what must the scenario provide for this assessment to be meaningful and do-able?* Capture
each as an `SR-*`. Typical kinds:

- **Environmental / access** — the lab + tools + data the AT needs. These map to UoC **AC** items (the AC
  link), so the AC conditions are discharged through the `SR-*` set rather than tracked separately.
- **Narrative / situational** — a stakeholder who can role-play a sign-off; a documented procedure to
  follow; a baseline system in a specific state; a constraint that drives the work (e.g. a regulatory
  requirement). No AC link; these are what make the assessment *believable*.

The register is the contract the scenario plan must satisfy. The scenario cross-check fails if any `SR-*`
declared here is not provided by the scenario plan; the **quality/coherence** of the world stays a human
call.

## Skeleton

```markdown
# S1-CLn <Cluster Name> — Cluster Assessment Plan
> **STATUS: DRAFT.** <one line>
> **Scenario binding:** maps to the <scenario> scenario — see <scenario plan link>.

## 1. Integration approach
<the engagement thread; approval moments; KE approach>

## 2. Scenario
<vehicle, baseline, provided-vs-authored boundary>

## 3. Assessment structure
| AT | Working title | Mode | Format | Unit focus |
|----|---|---|---|---|
| AT1 | … | Individual | … | <UNIT> el … |

### AT1 — <title>
- **Mode / Format / Unit focus:** …
- **UoC coverage:** [<UNIT> PC 1.1–1.6] · [<UNIT> PE 1] · [<UNIT> KE 1, 2, 3]
- **Scenario requirements:** SR-CLn-01 · SR-CLn-02

## 4. Provenance
<reuse / new authoring / author-fresh>

## 5. Coverage verification
PE: … (all placed). KE: … (all placed). Verification: every consolidated item is covered by ≥1 AT above.

## 6. Scenario requirements register
| SR | Condition the scenario must enable | AT(s) | AC link |
|----|---|---|---|
| SR-CLn-01 | <e.g. a single-AZ baseline system deployable as a lab-pack> | AT1, AT3 | [<UNIT> AC 1] |
| SR-CLn-02 | <e.g. a stakeholder who role-plays design sign-off> | AT1 | — |

## 7. Worklist
## 8. Open questions / TBDs
## Changelog
```

## See also

- [process-assessment.md](process-assessment.md) — the run-sheet; step 4 produces this plan, step 5
  consolidates the per-cluster plans, step 6 authors the scenario materials it maps to.
- [cluster-authoring-conventions.md](cluster-authoring-conventions.md) — the UoC traceability rule the tag
  conventions share.
- [scenario-plan-format.md](scenario-plan-format.md) — the scenario-plan format: defines the in-world
  elements the `SR-*` map back to, and the cross-check that confirms every `SR-*` is satisfied.
