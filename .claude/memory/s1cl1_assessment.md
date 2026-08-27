---
name: s1cl1-assessment
description: "S1-CL1 (Cloud Design and Build) pilot cluster, assessment workstream — DELIVERED, now in a feedback-driven improvement pass: AT shape, settled cross-AT design decisions; instruments passed institutional review 2026-07-10 and are now OPEN for in-place edits via their generators."
metadata: 
  node_type: memory
  type: project
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
  modified: 2026-08-27T15:31:26.177Z
---


S1-CL1 (Cloud Design and Build) is the **pilot cluster**, developed end-to-end. This entry holds the
**assessment workstream**: the cluster's **AT shape**, its **settled design decisions**, and its
**completion status**. Delivery-planning (sessions/teaching materials) is a separate workstream — see
[[s1cl1-delivery]]. General authoring rules live in docs/cluster-authoring-conventions.md.

## Cluster shape

| AT | Title | Format | Primary unit |
|---|---|---|---|
| AT1 | Business Case: YAT LMS Cloud Migration | Project Assessment — Part A (BC written) + Part B (board presentation) | ICTICT517 |
| AT2 | Cloud Foundation Build: YAT LMS | Project Assessment — single-task; deliverable = Deployment Report + appendices | ICTCLD401 |
| AT3 | High Availability: YAT LMS | Project Assessment — Part A (HA Design) + Part B (HA Deployment Report) | ICTCLD502 |

Scenario: the **YAT College (RTO)** world is single-sourced on the **website**
(diploma-cloud-cyber-website) — see docs/website-architecture.md. Cluster artefacts reference it
**abstractly** (e.g. "the YAT intranet"), never by path; the old `<repo_root>/scenario/` folder is no
longer the source of truth.

## Settled cross-AT design decisions (won't re-litigate unless new evidence)

- **Project Assessment template for all three ATs** — even AT2 (single-task): "implementation is a
  project even if the deliverable is written." (General rule: docs/cluster-authoring-conventions.md §7.)
- **502 PC reassignment AT3 → AT2:** PCs 1.3, 4.1, 4.2, 4.3 moved (UoC text analysis — not HA-specific).
  AT3 owns all HA-design / -evaluation / -simulation / -closure PCs.
- **MTS scope = cloud infrastructure only.** YAT IT (in-scenario) handles LMS app deployment, MySQL
  migration, cutover, change management. Single source: the AT1 role-brief § Scope; cross-referenced
  from AT2 + AT3.
- **AT3 is post-cutover** — LMS already deployed by YAT IT after AT2; AT3 hardens running infrastructure
  in place (no re-deploy, no data migration, no cutover for AT3).
- **AT3 has no standalone closure pack / observation event / Security Responsibilities Matrix.** Closure
  PCs (5.1–5.3) evidenced in HA Deployment Report §6.6 + §7.5 + §7.6; FS Oral Communication in AT1's
  presentation.
- **AT2 → AT3 thread loose by design.** AT2 implements a supplied baseline design; AT3 hardens it. The
  assessor distributes an AT2 baseline CloudFormation template so every student starts AT3 consistent.
- **AT3 maintenance-window framing:** simulated Saturday late-night ~3.5h window; brief blips
  acceptable; must end HA-done or rolled back.
- **AT3 Multi-AZ is a real live demo (not a fallback).** The hardened end-state — RDS `MultiAZ: true`
  **and** cross-AZ ASG+ALB — is proven deployable in the **AWS Academy Cloud Architecting Sandbox**
  (`ap-southeast-2`, 2026-06-15). The old "Multi-AZ RDS not supported" reading was wrong for that lab.
  **Required lab for AT3 = the Cloud Architecting Sandbox** — recorded in the AT3 assessment conditions
  (C1 names AWS Academy Cloud Architecting [172221] + Cloud Foundations [104469] and RDS access). The
  design+simulated-failover fallback is NOT needed.

## Status — DELIVERED; improvement pass OPEN

The CL1 assessment workstream passed institutional review (2026-07-10) and has since been **delivered to
a live intake**. That approval is spent: the instruments are now **open for a feedback-driven
improvement pass**, edited in place via their generators, to be re-frozen at the next human review
before the following intake — see [[feedback-finalised-assessments-change-control]].

- **9 instruments** (AT1/AT2/AT3 × assessor / student / exemplar) approved + delivered. All six
  assessor + student instruments **have generators** (`scripts/s1_cl1/build_s1_cl1_at*_{assessor,student}.py`,
  retrofitted 2026-07-09 → one generator process across all clusters, [[one-course-agnostic-mechanism]]);
  the exemplars too (`…_exemplar.py`).
- **Generator drift to check before regenerating:** the institutional-review edits + the KE/reflection
  presentation tidy (2026-07-10) were applied to the **`.docx` directly**, so those approved `.docx` went
  **ahead of their generators**. Before regenerating any CL1 instrument, run
  `validate-instrument-reproduction` against the committed copy — a mismatch means real content lives only
  in the `.docx` and must be lifted into the generator first, or the regenerate silently drops it.
  `[TBD — needs discussion: whether AT1's improvement pass already reconciled its generators, and whether
  to reconcile AT2/AT3 up front.]`
- **Version:** the delivered baseline is **v1.0** (version shown in the document footer). `[TBD — confirm
  the footer version field is present/reads v1.0 on all six instruments.]`
- **AT3 uses a real live Multi-AZ failover demo** (proven in the Cloud Architecting Sandbox); the AT2
  baseline CloudFormation + AT3 lab-pack deploy there.
- The **Records Management Policy** is authored on the website (`src/content/policies/records-management.md`).
- **YAT Feedback Record template built (2026-08-03):** AT1 Appendix 4 (criterion A13) names a
  standalone "YAT Feedback Record template" download that never existed on the website — a gap between
  the frozen instrument and the documented in-deliverable-feedback decision
  (docs/document-template-system.md). Resolved by adding the template
  (`diploma-cloud-cyber-website-s1/public/templates/YAT-Feedback-Record-Template.docx`, generator
  `diploma-cloud-cyber-content-s1/scripts/templates/build_feedback_record_template.py`), wired to
  s1-cl1* states only. The instrument itself was not touched (it was frozen at the time).
- Delivery workstream: see [[s1cl1-delivery]].

## AT3 — reframed as a guided workbook (2026-08-26)

AT3 is no longer two written reports. It is **one guided design-and-build workbook**, the same form
AT2 took, and the run-sheet chain has been re-walked to match: assessment plan **Gate 4 PASS**,
consolidated plan **Gate 5 PASS**, scenario plan **Gate 6 PASS**. The assessor instrument is
authored, in place, and passes traceability + 106/106 coverage.

- **Part A tasks 1–18** (design) → **Part B tasks 19–24** (build) → **T1–T4** → **tasks 25–29**
  (closing) → **knowledge questions 1–6** → **reflections 1–3**. Numbering is continuous because
  every Part B task cites the Part A task it builds.
- **Performance criteria are framed as tasks; knowledge criteria as questions.** Tim's rule.
- **The copy-forward is what keeps `PE 1`/`PE 2` alive** — each build task names the Part A task
  whose answer it implements, so the same candidate designs *and* implements the same infrastructure.
  A supplied exemplar design would break both items — and so would an assessor-corrected one.
- **No marking checkpoint between the parts** — it is one continuous worksheet. An assessor who
  corrects a design before the student builds it has made the build an implementation of the
  *assessor's* design, breaking `PE 1`/`PE 2` the same way a supplied exemplar would, only smaller.
  A design that would not deliver HA fails at its design task and again at the build task that
  implements it; the standard is stated at both.
- **The starting state is the AT2 run sheet's end state**, not the old supplied baseline design.
  The lab-pack is rebuilt to reproduce it (another session); the assessor distributes it, channel
  their choice, and deploying it is task 19.
- Marking model: see [[feedback-mark-uoc-intent-not-invented-settings]].
- Files: `at3_run_sheet.py` (content, one definition rendered two ways), `run_sheet_render.py`
  (shared primitives — AT2 keeps its own copies until that session lands, then switches),
  `build_s1_cl1_at3_assessor.py`. The old report-based assessor generator is deleted.
- **`[ICTCLD401 PC 4.1]` dropped from AT3** — AT1 evidences it properly (presentation event + its
  sign-off). Removing it exposed that AT1 carried it on criteria but **not in its benchmark**, so
  coverage had been passing only because AT3 mentioned it. Fixed in AT1's benchmark block 13.

**Next:** Tim walks the assessor document through the console himself to prove it is achievable,
then the assessor version locks. Only then the student copy (`render(..., mode="student")`) and the
downstream dependencies. `build_s1_cl1_at3_student.py` and the HA-deployment-report exemplar both
still describe the retired two-report shape.

## AT2 improvement pass — carried forward to the AT3 review

AT2 has been through the redundancy pass of the AT-review process (`scratch/at-review-process.md`).
Three things it uncovered are **AT3's to resolve when AT3 goes through the same review** — they were
deliberately not fixed from the AT2 side.

- **`[ICTCLD401 FS Planning and organising]` is mis-attributed on AT3's B15.** The item's words are
  *"…making limited decisions on sequencing, timing and collaboration…"*; B15 is the reflections
  appendix, written after the work. AT2 carried the identical mis-attribution on its A12 and it has
  been dropped there. **Remap it onto AT3's implementation-sequencing criteria (A4/A5)** — the HA
  Design requires *"an implementation sequencing plan (the order you'll apply the changes during the
  maintenance window)"*, which is the item demonstrated rather than recalled. AT3's coverage line
  already carries the FS, so no assessment-plan change is needed.
- **AT3's reflections are now the cluster's only ones.** AT2's Appendix D was removed as a
  consolidation: its three tags were a strict subset of B15's five, so nothing orphaned. AT2's R1
  prompt — *"lessons applicable beyond this build"* — has **no AT3 equivalent** and is the prompt that
  genuinely carries `FS Learning`; fold it into AT3's set. AT3's R1 (*decisions in hindsight*) was
  already a duplicate of AT2's R2.
- **The same mis-attribution is likely elsewhere in AT3's B15** — it also carries `502 FS Problem
  solving` and `502 FS Self-management`, which may or may not survive the same wording test.

Also carried forward from AT2, for AT2's own later passes (not AT3's):

- **The benchmark's §4 sub-sections name the wrong criterion — all seven.** 5.1/5.2/5.6 say A4 (should
  be A2), 5.3/5.4/5.5 say A5 (should be A3), 5.7 says A6 (should be A4). Deferred: the benchmark gets
  one rewrite pass once the assessment content stops moving, so it reads as an example of a good one.
- **The Appendix A / C evidence lists.** The criteria name counts (17 screenshots, 6 test-evidence
  items) that no artefact has ever enumerated — not the template in any of its five historical
  versions, not the exemplar, not the delivery materials. **The 17 is scratched**; the lists get built
  from what the finished assessment actually asks the student to do.
- **Criterion numbering and appendix letters have deliberate gaps** (A1, A10, A12 removed; Appendix B
  and D removed). One renumbering pass at the end, not per finding.
- **`assessment_plan.md` needs two AT2 edits** once the other session is out of it: AT2's coverage line
  should drop `401 FS Learning`, `401 FS Planning and organising` and `401 FS Self-management skills`
  (they left with Appendix D), and the AT roster table still describes AT2 as having *"direct
  observation"*, which it has never had.

## AT2 supplied design — the review it now needs

Pass B kept running into the **supplied baseline design** (`scripts/scenario/build_at2_baseline_solution_design.py`)
as the thing making the assessment harder than its UoC items require. A design review is the next
substantial piece of work. What it has to settle:

- **Access to the application instance.** §6.1 asks the student to connect to it and run the other
  tests from there. Today that is impossible without a bastion or VPN: the instance is Windows Server
  2016 (no SSH server by default) in a private subnet. Either enable SSH properly — security group,
  key pair, a route in — or accept Session Manager. **Tim's direction is SSH.** Note that SSH points
  toward making the application tier Amazon Linux rather than Windows, which would also shorten the
  test commands; the "DOODLE on Windows Server 2016, no re-platforming" constraint is one we wrote
  ourselves, not a UoC requirement.
- **Something for the load balancer to serve.** The design stops at "infrastructure ready for
  application deployment" with no web server, so the ALB health check fails and the target group shows
  unhealthy. Specify a web server via launch-template user data so the health check passes on its own.
  `SR-CL1-05` assumes a placeholder page exists but assigns it to the **AT3** lab-pack, so AT2 students
  are currently expected to invent it with no instruction anywhere.
- **TLS cannot be built in the lab.** §4.4 mandates an HTTPS:443 listener with an ACM certificate for
  the LMS DNS name, and `sg-alb` allows 443 only. ACM will not issue against a domain the student
  cannot validate, so the listener can never be completed and there is no HTTP fallback. The in-world
  story already resolves this: the hostname and certificate are **issued by YAT ICT**, and cutover is
  outside MTS scope — so the MTS build legitimately ends before TLS. Move to HTTP:80 for the build.
- **`sg-app` still says `RDP:3389 from MTS bastion`**, which contradicts §4.16 (updated to Session
  Manager, no bastion) and is the jump-box requirement that cost a live cohort its lab time.
- **Scaling policy timing.** §6.5 tests autoscaling by lowering the policy target until it scales out,
  then raising it until it scales in — a good test that avoids load generation. Default target-tracking
  scale-in uses a 15-minute alarm window, so specify a cooldown and evaluation period that round-trips
  inside a session.
- **The design `.docx` is ahead of its generator** (two embedded images, a 432 KB PNG and a 903 KB SVG,
  that the generator does not emit). Reconcile before regenerating, or they are lost.

Already changed in the generator, awaiting that regeneration: §4.10 monitoring cut from five alarms to
two; §4.16 configuration decisions cut from eight to two with the other five now specified by the design.

Queued for the **downstream sweep** (§13 of `scratch/at-review-process.md`), once the assessment side
of the AT2 review is signed off — deliberately not chased during the instrument pass:

- **Topic 09's slide plan and built deck teach the old five-alarm set**, including an ALB
  `HTTPCode_Target_5XX_Count` alarm at "> 5/min" that the supplied design never asked for. The design
  now specifies two alarms (ALB target health status; RDS free storage low).
- **The AT3 lab-pack `baseline.yaml` creates `AlarmAlb5xx`** — same drift, and it is the environment
  AT3 students start from.
- **The supplied design `.docx` cannot be regenerated yet.** The monitoring change is in
  `scripts/scenario/build_at2_baseline_solution_design.py` and verified in a scratch build, but the
  committed `YAT-LMS-Baseline-Solution-Design.docx` is **ahead of its generator**: it carries two
  embedded images (a 432 KB PNG + a 903 KB SVG) the generator does not emit, so regenerating drops
  them. Same class of problem as the CL1 instruments' generator drift. Reconcile the images into the
  generator first, then regenerate. Until then the monitoring reduction has not reached students.

**Validator gotcha worth remembering:** `validate_cluster_coverage` collects tags from the **benchmark
section**, not from the marking-guide criterion rows — while `validate_at_traceability` reads the
criterion rows. A tag therefore has to appear in **both** places. Deleting a stray benchmark prose line
during the AT2 pass silently uncovered `[ICTCLD401 FS Reading]` even though A13's criterion still
carried it. Fixed properly by giving the benchmark the A13 Document quality block it had never had.
