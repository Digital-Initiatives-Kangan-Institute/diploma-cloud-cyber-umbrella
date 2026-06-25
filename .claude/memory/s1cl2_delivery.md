---
name: s1cl2-delivery
description: S1-CL2 (Cloud Disaster Recovery) delivery workstream — week/session frame, the 10-Topic spine (AT1 design / AT2 build), the LMS practice vehicle, and the topic-coverage re-check against the finalised website assessments.
metadata:
  type: project
---

S1-CL2 **delivery-planning** workstream (separate from assessment authoring — see [[s1cl2-assessment]]).
General method: docs/process-delivery.md; process doc `docs/process-delivery.md`.

## Frame
CL2 = **weeks 9–18, 30 × 3h sessions (3/wk), 84h**, delivered **in parallel with CL3**. AT1's `.docx`
allocates Part A ≈ 2 wks / Part B ≈ 3 wks → **AT1 phase ≈ first 5 wks, AT2 phase ≈ last 5 wks**.

## Topic spine (10 content Topics)
- **AT1 → T1–T5** at **design/plan depth:** web-scale design · microservice design · DR
  requirements/impact · DR strategy/plan · documenting + presenting.
- **AT2 → T6–T10** at **build depth:** IaC + operate provided templates · author own template · build
  the microservice · monitoring · documenting/sign-off.
- Collectively the two ATs' coverage tags every PC and PE they assess.

## Practice vehicle (settled)
The **LMS** (`lms-global-expansion`) is the CL2 practice vehicle — web-scale-credible, so it carries the
web-scale teaching needs. (Assessed on the website, practised on the LMS — see
docs/scenario-flow.md.)

## Status (2026-06-25)
- **Gates 1–3 PASS.** Cluster spec PASS; every teaching Topic has a `topic_NN/coverage.md`;
  `validate-delivery-coverage` **91/91** — after the project tag retrofit (65 backtick-wrapped tags
  unwrapped in topics 04, 06–10) **and** authoring the AT1 specs (topics **1, 2, 3** were empty, **5**
  was missing), which mapped all 33 previously-untaught items grounded in the AT1 `.docx`. The four AT1
  coverage specs are **DRAFT — human review of the allocation + depth ceilings pending.**
- **Step 4 proven on topic_01:** `slide_plan.md` (finished content) → 20-slide Kangan deck via the generic
  `build_topic_deck.py`, with the web-scale architecture diagram (draw-diagram) + 2 decorative gen images
  placed **in-pipeline**. See [[delivery-run-sheet]].

## Open — where it needs to go
- **Author the other 9 CL2 slide plans** (topics 2–4, 6–10) → build their decks the same way; size the
  Topics onto the 30 sessions.
- CL2 **Steps 5 (practice tasks) + 6 (delivery plan)** still to do.
- **Blocked-ish on:** the web-scale practice app for the T6–T9 demos. (The lab environment is settled —
  both AWS Academy products are provisioned; each activity uses whichever fits. See docs/lab-pack-standard.md.)
