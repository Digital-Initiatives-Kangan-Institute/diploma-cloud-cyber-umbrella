---
name: s1cl2-delivery-state
description: S1-CL2 delivery-planning workstream — Topic spine + per-Topic coverage were done but PARTLY DELETED after the assessment re-vehicling (LMS→website); to be redone once the re-pointed assessments are finalised.
metadata:
  type: project
---

CL2 **delivery-planning** workstream (process: `documentaion/delivery_process.md`, model `AT → Topic → component`; same lean Topic-based approach as [[s1cl1-delivery-state]]). Distinct from [[s1cl2-cluster-state]] (the assessment authoring).

**⚠ INVALIDATED BY RE-VEHICLING (2026-06-08) — see [[s1cl2-cluster-state]].** CL2's assessment re-pointed **LMS → website**; the delivery Topic docs were built on the old LMS framing. **DELETED (to redo after the re-pointed assessments are finalised):** `delivery/planning/cl2-teaching-topics-draft.md` + `delivery/topic_{01,02,03,05}/coverage.md`. The other coverage docs (`topic_04`, `06–10`) were vehicle-neutral and remain. The "Done & pushed" section below is now historical.

**Frame:** CL2 = **weeks 9–18, 30 × 3h sessions (3/wk), 84h goal**, delivered in parallel with CL3. AT1's `.docx` allocates Part A ≈ 2 wks / Part B ≈ 3 wks → AT1 phase ≈ first 5 wks, AT2 phase ≈ last 5 wks.

**Done & pushed (`c80a259`):**
- **Step 1 — Topic spine** (`delivery/planning/cl2-teaching-topics-draft.md`): 10 content Topics. **AT1 → T1–T5** (web-scale design · microservice design · DR requirements/impact · DR strategy/plan · documenting+presenting) at **design/plan** depth. **AT2 → T6–T10** (IaC + operate provided templates · author own template · build the microservice · monitoring · documenting/sign-off) at **build** depth. `topic_01..10/` folders pre-existed and match.
- **Step 2 — `coverage.md` per Topic** (components → UoC mapping → AT alignment → out-of-scope → checklist; depth ceiling stated). Cross-check: collectively tag **every PC (56/56) and PE (12/12)** the two ATs assess.

**Practice vehicle (per scenario-flow):** the **LMS** (`lms-global-expansion`) is the CL2 practice vehicle — web-scale-credible, so the T1 web-scale-practice-app TBD is **resolved** (the LMS carries it). *(Supersedes the earlier "Accounting carries the Topics" framing.)*

**NEXT — Step 3:** `slide_plan.md` → Kangan-branded deck per Topic (primer-first, **reuse-first from the AWS decks**, `teach → demo → practice`), then size Topics against the tempo bands and lay onto the 30 sessions. **Blocked-ish on:** the web-scale practice app (T1) + the lab-product `[VERIFY]` (Learner Lab vs Architecting Sandbox — shapes the T6–T9 demos).
