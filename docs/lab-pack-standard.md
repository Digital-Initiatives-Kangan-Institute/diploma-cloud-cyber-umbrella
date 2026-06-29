# Lab-pack standard

A **lab-pack** provides the assessor-supplied, runnable AWS artefacts a student deploys into
an **ephemeral AWS Academy lab** to get a consistent baseline/environment for an assessment,
together with a **local validation harness** that proves the artefacts before they ever touch
a lab. This is the course-wide standard for that problem.

> **Reference implementation:** `S1-CL1-Cloud-Design-Build/assessments/AT3/lab-pack/` — the AT3
> non-HA baseline students harden. It was the first pack proven against a live AWS Academy
> session (2026-06-07); the findings below come from that run.

---

## Acceptance — what "realised/done" means (and what verification checks)

A lab-pack is **delivered as a deployable pack, never as a live/running environment.** Standing it
up — and deploying any end-application onto it — is **downstream** (the teacher/student in class, as
needed), or, where the scenario puts the application out of scope entirely (e.g. **CL1**, where the LMS
app is YAT in-house), **not at all**. So a lab-pack's **definition of done for the assessment process**
is:

1. **The pack exists** at `<cluster>/assessments/<AT>/lab-pack/` — template(s) + student README +
   claude-notes + the local test harness.
2. **The local validation harness passes** (cfn-lint clean + pytest).
3. **It has been proven once in a live AWS Academy session** (deploy → serves/verifies → tear down),
   the result recorded in `claude-notes.md`.

**What verification must NOT require:** a live/running environment, a stack standing in an account, or a
deployed end-application. The deliverable is the *proven, deployable pack* — not its deployment. A
lab-pack whose template serves only a placeholder page is **complete** when that is the scoped end-state
(again, CL1: "infrastructure ready for application deployment" *is* the deliverable). Checking a lab-pack
= confirm 1–3, not "is it deployed".

---

## Why the pattern exists

AWS Academy labs are **ephemeral** — whatever a student built in a prior session/AT is gone.
When an assessment needs a known starting environment (and the student is **not** assessed on
*building* that environment), ship a lab-pack: a CloudFormation template (plus any application
code) the student deploys at the start, validated locally first.

## When it applies — and when it does NOT

A lab-pack provides an environment the student is **not assessed on building**.

- **Fits:** AT3 (harden a *given* baseline), and any AT that builds on a prior end-state that
  doesn't survive an ephemeral session.
- **Does NOT fit** an AT where *building the environment is the assessed skill* — e.g. **CL1
  AT2 (ICTCLD401)** is a hands-on **manual console build** (point-and-click + screenshots), no
  template. **Infrastructure as Code as a skill is ICTCLD505 = CL2**, where students author and
  operate templates. A student deploying a lab-pack baseline is just running a **black-box
  installer** (upload → Create stack), not "doing IaC".

So: CL1 = manual build + hardening; CL2 = IaC.

**Provided-to-work-from artefacts are NOT a lab-pack either.** Where an AT *gives* the student code or
templates to operate, debug, or author their own IaC around, supply them **inline as assessment appendices**,
not as a validated pack — e.g. **CL2 AT2**: a data-store template (another contractor's, in-scenario)
carrying a **deliberate fault the student must debug**, plus the microservice **code** the student writes
their own deploy template for. A pre-built/validated pack would remove the assessed work, and a
*deliberately-faulty* template must **not** be "proven to deploy". Don't flag such inline artefacts as a
missing lab-pack — that's the wrong delivery mechanism for them.

---

## Folder structure

Location: `<cluster>/assessments/<AT>/lab-pack/`. Always present:

```
lab-pack/
  README.md            STUDENT-FACING, click-by-click: open the sandbox -> region -> deploy ->
                       verify -> tear down. Plain language, no jargon, no meta.
  claude-notes.md      Author/assessor notes: findings, deviations, the standard, links. NOT student-facing.
  requirements.txt     local-validation deps (cfn-lint always; pytest where useful). Keep LIGHT.
  .gitignore           .venv/  __pycache__/  .pytest_cache/
  .cfnlintrc.yaml      documented lint suppressions only (short + justified)
  <template>.yaml      the CloudFormation the student deploys
  [code/ | microservice/]   any application code (e.g. a Lambda handler)
  [assessor-model/]    model answers / assessor-only reference, where relevant
  tests/               cfn-lint on every template + a pytest asserting structural invariants
  .venv/               gitignored; recreate from requirements.txt
```

**README vs claude-notes is a hard split:** the README contains *only* student deploy steps;
everything else (reference-implementation framing, standard links, deviations, the validation
harness, live-lab findings) goes in `claude-notes.md`.

---

## The lab environment — AWS Academy Learner Lab (`us-east-1`)

**One course-wide lab product: the AWS Academy Learner Lab** (decided 2026-06-29). Every lab-pack,
activity and assessment deploys there, for **consistency** (students learn one environment) and
**session persistence** (the Learner Lab keeps state between sessions; the Cloud Architecting Sandbox
did not). The Learner Lab exposes a **single region — `us-east-1`**.

**Region is simulated by substitution.** The YAT scenario is Australian and its architectures are
genuinely multi-region (Sydney `ap-southeast-2`, Mumbai `ap-south-1`, Melbourne `ap-southeast-4`), but
all of it deploys to `us-east-1`. The **design layer stays multi-region** (region choice, residency, DR
are taught and assessed in full, with real region codes); only the **physical deploy** collapses to
`us-east-1` — deployment is mechanically identical in any region, so nothing assessable is lost. The seam
is the substitution token, e.g. `[scenario: ap-southeast-2 (Sydney) | deploy: us-east-1]`. The full rule
— notation, canonical mapping, residency/DR handling — is the
[region-substitution standard](region-substitution-standard.md); **every lab-pack README must use it**
on each deploy step.

**`LabRole` is available** — a broad pre-provisioned role you can pass to Lambda etc. (the Cloud
Architecting Sandbox had no usable role; that constraint no longer applies). Keep any role/instance
profile an **optional parameter** anyway (see constraints below) so templates stay portable.

**Serverless on `LabRole` — proven.** An API-GW → SQS → Lambda → DynamoDB stack deploys and runs via
CloudFormation with `LabRole` serving as **both** the Lambda execution role **and** the API-GW→SQS
credentials — so build ATs needing a serverless execution role (e.g. the CL2 microservice) can be
hands-on.

**Multi-AZ HA — proven (2026-06-26).** The CL1 AT3 baseline, hardened to the full multi-AZ end-state
(RDS `MultiAZ: true` on `db.t3.medium` + an ASG spanning two private app subnets), deploys to
`CREATE_COMPLETE` in `us-east-1` with the **RDS standby in a second AZ** — no AZ or capacity refusal. So
**within-region, cross-AZ HA is real, not simulated** (and AZs are never substituted — the token is
region-level only). Two limits remain: (1) **cross-region residency/DR is notional** — Mumbai/Melbourne
deploy as extra stacks in `us-east-1`, with the geography simulated and noted in-world (never fake a
region with an AZ); (2) on a live run the Windows placeholder instances churned on an **ELB health-check
replace loop** (~6 min) — a UserData/bootstrap issue, not a multi-AZ one, to fix before any live "lose an
AZ, stay up" demo.

---

## AWS Academy constraints — bake in every time

These are the things a paper spec forgets and a live deploy enforces. (✔ = confirmed in the
Cloud Architecting Sandbox, 2026-06-07.)

- **Never create IAM.** The lab forbids it (IAM is read-only). **Role/profile names vary by lab
  and may not exist** — the Cloud Architecting Sandbox has **no `LabRole`/`LabInstanceProfile`**
  (only `EMR_EC2_DefaultRole`, `myS3Role`); the Learner Lab *does* have them. So make any
  role/instance-profile an **optional parameter** (default blank) and omit it via
  `!If`/`AWS::NoValue` when empty. A baseline EC2 instance serving a page needs none. ✔
- **AMIs via SSM public parameter** — `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>`, default
  `/aws/service/ami-windows-latest/...`. Never a hardcoded AMI that ages. ✔
- **Region = `us-east-1` always; geography is simulated by substitution.** The Learner Lab exposes
  only `us-east-1`, so **every** deploy targets it regardless of the design region — the console
  already defaults there. The design stays multi-region; the deploy step carries the substitution
  token (`[scenario: ap-southeast-2 (Sydney) | deploy: us-east-1]`) per the
  [region-substitution standard](region-substitution-standard.md). Templates stay region-portable
  via the SSM AMI parameter + `!GetAZs` (so they'd still deploy elsewhere if a region were ever
  added). ✔
- **Instance/DB classes are parameters.** The sandbox allows EC2 `t2/t3` nano–medium and RDS
  `db.t3.micro`–`db.t3.medium` only. Default `t3.medium` / `db.t3.medium`; adjust per lab. ✔
- **RDS Multi-AZ IS supported** in the Cloud Architecting Sandbox — **proven live 2026-06-15**
  (RDS `MultiAZ: true`, MySQL 8.4.8, `db.t3.medium`, synchronous standby in a 2nd AZ) reaching
  CREATE_COMPLETE alongside cross-AZ compute (2× `t3.medium`, AZs 2a/2b, healthy). **This corrects
  an earlier mistaken "not supported / do not create a standby instance" note** (the doc previously
  said the opposite — it is wrong; do not reinstate it). So the **full multi-AZ HA end-state**
  (Multi-AZ RDS **and** ASG-across-AZs + ALB) deploys cleanly, and an HA assessment can use a **real
  live DB failover demo** (reboot-with-failover), not just compute failover. ✔ (2026-06-15)
- **SQL Server: use Express in the sandbox.** RDS rejects **`sqlserver-se` (Standard, license-included) on
  `db.t3.medium`** ("RDS does not support creating a DB instance with the following combination") — SE needs a
  larger class than the sandbox permits. **Express (`sqlserver-ex`) deploys fine** on `db.t3.medium` (proven in
  `us-east-1` **and** `ap-southeast-2`, 2026-06-21). For an empty lab DB the edition is immaterial; if the
  scenario calls for Standard, ship Express as a documented stand-in. ✔ (2026-06-21)
- **The sandbox role denies `rds:ModifyDBInstance` — RDS is create-only.** The `voclabs` role can **create** an
  RDS instance but **cannot modify** an existing one (a change-set altering `BackupRetentionPeriod` failed with
  `AccessDenied`, 2026-06-21, CL3 AT3). **For any apply-as-update / change-set lab-pack: never modify an existing
  RDS instance** — set the DB's final config at *create* time and leave it untouched by later updates. This
  blocks in-lab DB modification via **both** CloudFormation and the console, so DB-tier changes needing
  `ModifyDBInstance` (retention, etc.) are not lab-executable; show DB reliability via PITR/restore instead
  (restore perms not yet verified). ✔ (2026-06-21)
- **2-AZ gotchas:** an internet-facing **ALB needs ≥2 subnets in 2 AZs**, and an **RDS DB subnet
  group needs ≥2 AZs** — so even a "single-AZ baseline" must include a 2nd public + 2nd data
  subnet to deploy. Keep the **compute (ASG) single-AZ** to preserve the non-HA state. ✔
- **Clean teardown:** RDS `DeletionPolicy: Delete` (no lingering final snapshot); empty S3
  buckets; the README stresses `delete-stack` + End Lab to free credits.
- **Deferred by default:** VPC flow logs to CloudWatch need an IAM role (forbidden) → drop or
  send to S3; HTTPS/ACM needs a domain → use HTTP:80 in the lab.

---

## Local validation harness

Proves the template/code before a lab. Students never run this — it's author/assessor only.

```bash
cd lab-pack
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt   # Windows  (.venv/bin on macOS/Linux)
.venv/Scripts/cfn-lint <template>.yaml                    # lint clean (exit 0)
.venv/Scripts/python -m pytest -q                         # structural / handler tests
```

- **`cfn-lint`** every template. It runs via its **console script** (`.venv/Scripts/cfn-lint`),
  **not** `python -m cfnlint`.
- **pytest** asserts structural invariants — for a baseline: the non-HA state (Single-AZ RDS,
  single-subnet ASG), the Academy constraints (zero `AWS::IAM::*` resources, optional instance
  profile, SSM AMI, locked-down buckets), expected Outputs. Parse templates with
  **`cfnlint.decode.cfn_yaml`** (it understands `!Ref`/`!GetAtt`). For Lambda handlers, use a
  small in-file fake — **NOT `moto`** (its deep package paths break Windows `MAX_PATH` inside
  these repo folders).
- **cfn-lint does NOT catch everything** — see the ASCII lesson below. Keep a Python non-ASCII
  scan in the loop.
- Document any lint suppression in **`.cfnlintrc.yaml`**, short and justified (e.g. `W1011` for
  a NoEcho DB-password parameter).

---

## Lessons learned (hard-won, from the live proving run)

- **Keep templates PURE ASCII.** A non-ASCII char (em-dash `—`) in an RDS
  `DBSubnetGroupDescription` **fails the live deploy** ("must not contain non-printable control
  characters"), and **cfn-lint does NOT flag it** — it only enforces the printable-char regex on
  *security-group* descriptions, not RDS ones. Replace em-dashes with hyphens; scan for
  non-ASCII after edits.
- **Instance-profile name is the #2 failure.** `LabInstanceProfile` is a *Learner Lab* name; the
  Architecting Sandbox doesn't have it → "Invalid IAM Instance Profile name." Make it optional.
- **Use "Preserve successfully provisioned resources"** on a proving run (stack-failure option)
  so the partial state is inspectable instead of rolled back.
- **`moto`** is banned (MAX_PATH on Windows) — hand-roll small fakes instead.

---

## Building a new lab-pack — checklist

1. Author the template(s) to the constraints above (optional role param, SSM AMI, real region,
   parameterised classes, 2-AZ where ALB/RDS need it, clean teardown, pure ASCII).
2. Set up the venv + `requirements.txt`; get **cfn-lint clean** and a **pytest** asserting the
   invariants. Run a non-ASCII scan.
3. Write the **student README** (click-by-click) and the **claude-notes** (everything else).
4. **Prove it in a live Academy session** once — deploy, verify it serves, tear down. Record any
   findings back into this doc.
5. Commit (the `.venv` is gitignored; `requirements.txt` recreates it anywhere).
