# Lab-pack standard

A **lab-pack** provides the assessor-supplied, runnable AWS artefacts a student deploys into
an **ephemeral AWS Academy lab** to get a consistent baseline/environment for an assessment,
together with a **local validation harness** that proves the artefacts before they ever touch
a lab. This is the course-wide standard for that problem.

> **Reference implementation:** `S1-CL1-Cloud-Design-Build/assessments/AT3/lab-pack/` — the AT3
> non-HA baseline students harden. It was the first pack proven against a live AWS Academy
> session (2026-06-07); the findings below come from that run.

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

## Choosing the lab environment (per activity)

There is **no single course-wide lab product.** Each activity or assessment uses the AWS Academy
environment that best serves *its* learning outcome — chosen case by case. The two known
environments trade off against each other, and neither does everything:

| Environment | Gives you | Costs you | Fits |
|---|---|---|---|
| **Cloud Architecting Sandbox** | **Real regions** (Sydney `ap-southeast-2`, Mumbai `ap-south-1`) | **No usable IAM role** (no `LabRole`; IAM read-only) | Activities needing real geography or no custom IAM — e.g. the **CL1 AT3 baseline** (EC2 serving a page, no role) |
| **Learner Lab** | **`LabRole`** — a broad pre-provisioned role you can pass to Lambda etc. | **Regions limited to `us-east-1` / `us-west-2`** (geography is simulated) | Activities needing a serverless execution role — e.g. the **CL2 AT2 microservice** (Lambda needs a role) |

**Mandatory student-facing disclosure.** Because the environment changes per activity, every
lab-pack README must state, for its activity:

1. **which** environment to use;
2. **why** that one was chosen (the capability it provides); and
3. **what its limitations are** — and how the activity accommodates them (e.g. "regions are
   simulated here, so us-west-2 stands in for India; the *mechanics* are what's assessed, not the
   geography").

Students may switch environments between activities — that is expected; the README removes the
confusion by being explicit every time. *(The specific environment for each activity still
depends on what Kangan provisions.)*

**Serverless on `LabRole` — proven.** In the Learner Lab, an API-GW → SQS → Lambda → DynamoDB stack
deploys and runs via CloudFormation with `LabRole` serving as **both** the Lambda execution role **and**
the API-GW→SQS credentials. So Learner Lab build ATs that need a serverless execution role (e.g. the
CL2 microservice) **can be hands-on** — this joins the EC2/RDS baseline proven in the Cloud
Architecting Sandbox.

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
- **Region = the deploy target, and real geography works.** The Cloud Architecting Sandbox
  **deploys real regions** — `ap-southeast-2` (Sydney) proven end-to-end; `ap-south-1` (Mumbai)
  offered. **No region simulation needed.** (The us-east-1/us-west-2-only limit is the
  *Learner Lab*, a different product.) The console defaults to us-east-1 — **switch to the real
  region before deploying**; the template adapts via the SSM AMI parameter + `!GetAZs`. ✔
- **Instance/DB classes are parameters.** The sandbox allows EC2 `t2/t3` nano–medium and RDS
  `db.t3.micro`–`db.t3.medium` only. Default `t3.medium` / `db.t3.medium`; adjust per lab. ✔
- **RDS Multi-AZ IS supported** in the Cloud Architecting Sandbox — **proven live 2026-06-15**
  (RDS `MultiAZ: true`, MySQL 8.4.8, `db.t3.medium`, synchronous standby in a 2nd AZ) reaching
  CREATE_COMPLETE alongside cross-AZ compute (2× `t3.medium`, AZs 2a/2b, healthy). **This corrects
  an earlier mistaken "not supported / do not create a standby instance" note** (the doc previously
  said the opposite — it is wrong; do not reinstate it). So the **full multi-AZ HA end-state**
  (Multi-AZ RDS **and** ASG-across-AZs + ALB) deploys cleanly, and an HA assessment can use a **real
  live DB failover demo** (reboot-with-failover), not just compute failover. ✔ (2026-06-15)
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
