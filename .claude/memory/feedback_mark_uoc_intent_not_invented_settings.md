---
name: feedback-mark-uoc-intent-not-invented-settings
description: "Assessments invent specific settings to make a task doable; mark the UoC intent, never the invented values"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a40bd230-c889-45bf-97c8-0b1ee173f18b
  modified: 2026-08-27T00:31:22.157Z
---

UoC wording is vague and general — *"create virtual machine"*, *"design and deploy automated
infrastructure scaling"*. We necessarily invent specific settings so the student has a concrete task.
Those invented values are **context, not the standard**. What is marked is the UoC intent.

**The per-setting test:** if the student got this value wrong, would the UoC item still be evidenced?

- Yes → cosmetic. Feedback, never NYS. (ASG minimum 3 where we wrote 2; a different CIDR.)
- No → load-bearing. (ASG minimum left at 1 — one instance in one zone is not resilient to a
  data-centre failure, so `[ICTCLD502 PE 2]` is not evidenced, whatever the student's reasoning.)

**Why:** an assessor with only a settings table marks against our invented numbers, which fails
students for typing the wrong CIDR while passing designs that miss the requirement. It also makes the
assessment indefensible at validation — the standard has to be the unit's.

**How to apply:** every element in an instrument carries **two** assessor-only lines, not one —
`Evidences:` (the UoC tags) and `Satisfactory when` (what must be true for them to be met, stated in
the unit's terms, naming which settings are load-bearing and which are context). State the same rule
in the Assessment Overview so the assessor reads it before marking. Implemented in
`run_sheet_render.standard_line()`; see [[s1cl1-assessment]].

**The companion rule for guided/scaffolded instruments:** scaffold the **process**, never the
**finding**. *"Work through each tier and record whether its failure would take the LMS down"* is
scaffolding; *"the database is a single point of failure — fix it"* hands over the answer. Items whose
verb is *identify*, *determine* or *evaluate* die if the workbook supplies the finding.
