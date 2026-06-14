---
name: lab-pack-standard
description: Course-wide standard for "lab-pack" folders — runnable AWS artefacts students deploy into an ephemeral AWS Academy lab to get a consistent baseline/environment for an assessment, with a local validation harness. Reference implementation = S1-CL1 AT3.
metadata:
  type: project
---

**CANONICAL DOC = `documentaion/lab-pack-standard.md`** (in the repo, committed `eae2e18`) — the authoritative, complete standard. This memory is the lean recall; defer to the repo doc.

**Lab environment = PER-ACTIVITY choice (Tim decision, 2026-06-07).** No single course-wide lab product — each activity/assessment uses the AWS Academy environment that best serves its learning outcome. Trade-off: **Cloud Architecting Sandbox** = real regions (Sydney/Mumbai) but NO usable role (fits CL1 AT3 baseline — no IAM); **Learner Lab** = `LabRole` you can pass to Lambda but regions limited to us-east-1/us-west-2 (geography simulated; fits CL2 AT2 microservice — Lambda needs a role). **Mandatory:** every lab-pack README states which env / why / its limitations. Open `[VERIFY]`: confirm Kangan provisions BOTH products + the Learner Lab `LabRole` is passable to Lambda/API-GW->SQS.

**The pattern.** AWS Academy labs are ephemeral — whatever a student built in a prior AT is gone. When an assessment needs a known starting environment, ship a **lab-pack**: assessor-supplied **runnable CloudFormation** (+ any app code) the student deploys at the start, plus a **local validation harness** that proves the artefacts before they touch a lab. Tim's decision (2026-06-07): **this is the standard throughout the whole course** unless a strong reason to deviate arises. **Reference implementation = `S1-CL1-Cloud-Design-Build/assessments/AT3/lab-pack/`** (the AT3 non-HA baseline students harden); it is the **first to be live-lab-proven**, and live findings feed back here. CL2's `assessments/AT2/lab-pack/` predates the standard and is a back-port target (align, don't treat as canonical).

## When the pattern applies (and when it doesn't)
A lab-pack provides an environment the student is **NOT assessed on building** — so they deploy it and get on with the actual task. **Fits:** AT3 (harden a given baseline), and any AT that builds on a prior end-state that doesn't survive an ephemeral lab session. **Does NOT fit** an AT where *building the environment is the assessed skill* — e.g. **CL1 AT2 (ICTCLD401)** is a hands-on **manual console build** (point-and-click + screenshots), no template. **IaC as a skill is ICTCLD505 = CL2** (students author/operate templates there). A CL1 AT3 student deploying the baseline is just running a **black-box installer** (upload → Create stack), not doing IaC — a soft primer for CL2, not instruction. So: CL1 = manual build + hardening; CL2 = IaC.

## Structure (per assessment that needs a deployable baseline)
Location `<cluster>/assessments/<AT>/lab-pack/`. Always:
- `README.md` — three fixed sections: **A. Local validation** / **B. AWS-lab deploy** (deploy → verify → teardown commands) / **⚠️ live-lab verify** (what only a real session can confirm). Plus a "deviations from spec" note where reality forced changes.
- `requirements.txt` — harness deps (cfn-lint always; pytest where a structural/handler test adds value). **Keep it LIGHT.**
- `.gitignore` — `.venv/ __pycache__/ .pytest_cache/`.
- the CloudFormation template(s); optional `assessor-model/` (model answers, assessor-only) and app `code/` (e.g. a Lambda handler).
- `tests/` — local validation: cfn-lint on every template + (optional) a pytest that asserts structural invariants / runs handler code.
- `.venv/` **inside the folder, gitignored**, recreated from `requirements.txt`.
Validation must be **GREEN locally** (lint clean + tests pass) before delivery; **one live-lab verify** is the only remaining gate, flagged explicitly.

## AWS Academy constraints — bake in EVERY time
- **Never create IAM** (the lab forbids it). **Role/profile names vary by lab and may not exist** — the Cloud Architecting Sandbox has NO `LabRole`/`LabInstanceProfile` (only `EMR_EC2_DefaultRole`, `myS3Role`); the Learner Lab has them. So make the role/instance-profile a **parameter that defaults to none** and omit it via `!If`/`AWS::NoValue` when blank; only pass a name where one exists and is actually needed (baseline EC2 serving a page needs none). Structural test asserts zero `AWS::IAM::*` resources.
- **AMIs via SSM public parameter** (`AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>`, default `/aws/service/ami-windows-latest/...`) — never a hardcoded AMI that ages.
- **Region** as the deploy target: **`ap-southeast-2`** = AU default; **`us-west-2`** = India stand-in (Learner Lab only offers us-east-1/us-west-2; `ap-south-1` unavailable — see [[s1-cl2-cluster-state]]).
- **Instance/DB classes are parameters** (Academy restricts types; default to `t3.medium` / `db.t3.medium`, adjust per lab).
- **2-AZ gotchas:** an internet-facing **ALB needs ≥2 subnets in 2 AZs**, and an **RDS DB subnet group needs ≥2 AZs** — even a "single-AZ baseline" must include a 2nd public + 2nd data subnet to deploy. Keep the **compute (ASG) single-AZ** to preserve the non-HA state.
- **Clean teardown:** RDS `DeletionPolicy: Delete` (no lingering snapshot); empty S3 buckets; README stresses `delete-stack` to free credits.
- **Deferred-by-default:** VPC flow logs to CloudWatch need an IAM role (forbidden) → drop or send to S3; HTTPS/ACM needs a domain → use HTTP:80 in the lab.

## Harness lessons (hard-won)
- **`moto` breaks Windows `MAX_PATH`** — its `stepfunctions/parser/asl/...` tree pushes the venv path past 260 chars inside these deep repo folders. **Don't use moto.** For Lambda handler tests use a small in-file fake (see CL2 `tests/test_handler.py`); for template structure use **`cfnlint.decode.cfn_yaml`** (it understands `!Ref`/`!GetAtt`).
- `cfn-lint` runs via its console script (`.venv/Scripts/cfn-lint`), **not** `python -m cfnlint`.
- Document justified lint suppressions in **`.cfnlintrc.yaml`** (e.g. `W1011` for a NoEcho DB-password param) — keep the list short and commented.
- SG `GroupDescription` rejects em-dashes (`—`) — use hyphens.

## Status
- **S1-CL1 AT3 baseline** — ✅ **PROVEN LIVE & committed `eae2e18`** (2026-06-07): CREATE_COMPLETE in the Cloud Architecting Sandbox (Sydney, ap-southeast-2) and serves the placeholder page end-to-end. Two cfn-lint-missed bugs caught+fixed (em-dash in RDS description; `LabInstanceProfile` absent → instance profile optional). **Real Sydney deploys — no region simulation needed** (revisit CL2's us-west-2=India stand-in). **RDS Multi-AZ NOT supported in the sandbox** (compute/AZ sims fine). Supersedes the placeholder `scenario/assessor-resources/at2-baseline-cloudformation.md`.
- **Parked for AT3 revisit:** RDS-Multi-AZ workaround (design+document / read-replica / elsewhere); whether to re-add the EC2 "Application-Service" instance role as an optional param. **Next uses:** any future AT needing a baseline; back-port CL2 AT2 lab-pack to this standard. CL1 AT3 design confirmed **A** (ASG in AT2 per 401 Element 3; AT3 hardens to multi-AZ) — not changing.
