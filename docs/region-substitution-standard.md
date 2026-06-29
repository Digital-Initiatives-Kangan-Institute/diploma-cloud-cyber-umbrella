# Region-substitution standard

Every lab-pack, activity and assessment in this course is **deployed in the AWS Academy Learner Lab**,
which exposes a **single region: `us-east-1`**. The YAT scenario, though, is set in Australia and its
architectures are **genuinely multi-region** (Sydney, Mumbai, Melbourne). This standard is the **one
notation** that bridges the two: it keeps every design, document and assessment fully multi-region while
making the *physical deploy* honest about where it actually lands.

> Read with [lab-pack-standard.md](lab-pack-standard.md) — the deployable-pack standard (now Learner-Lab
> / `us-east-1` only).

## The principle — design is multi-region, deployment is single-region

The assessable competency around regions — **why** a workload belongs in Sydney, **why** residency
forces Mumbai, **why** DR copies to Melbourne — is a **design decision**, and it stays fully intact. The
physical act of deploying is mechanically **identical in any region** (you select the region in the
console's top-right dropdown and the same template applies), so collapsing the deploy target to
`us-east-1` loses nothing of significance.

So there are two layers, and the notation is the visible seam between them:

- **Design layer** — solution designs, architecture diagrams, assessment scenarios, the website. Uses
  the **real AWS regions** the scenario dictates: `ap-southeast-2` (Sydney), `ap-south-1` (Mumbai),
  `ap-southeast-4` (Melbourne). **No substitution here** — this is the real, correct design, and the
  region-choice reasoning is taught and assessed in full.
- **Deployment layer** — lab-pack READMEs and "now deploy this" steps. Carries the **substitution token**
  that maps the design's region to the Learner Lab reality (`us-east-1`).

## The notation

```
[scenario: <real-region-code> (<city>) | deploy: <learner-lab-region>]
```

- Delimiter is **square brackets** `[ ]` — a literal token, easy to spot and to lint (parentheses blend
  into prose).
- **Left** = the real region the design specifies (what the student would use in a real job).
- **Right** = where they actually deploy in the Learner Lab — currently always `us-east-1`.

Examples:

```
[scenario: ap-southeast-2 (Sydney)    | deploy: us-east-1]
[scenario: ap-south-1 (Mumbai)        | deploy: us-east-1]
[scenario: ap-southeast-4 (Melbourne) | deploy: us-east-1]
```

### Always present — even when nothing changes

The token appears at **every** deployment step in **every** lab and assessment, so students learn to
read it once and stop needing it explained. In the rare case where the design region already is the
deploy region, still show the token with an explicit identity marker:

```
[scenario: us-east-1 | deploy: us-east-1 — no substitution]
```

(In practice the YAT scenario is Australian, so almost every deploy substitutes `ap-southeast-2 →
us-east-1`.)

## Canonical mapping

All scenario regions currently map to the single available Learner Lab region. **This table is the
single source of truth** — never invent a per-lab mapping. If the Learner Lab ever exposes a second
region, change it here and nowhere else.

| Scenario region (design) | City | Deploy target (Learner Lab) |
|---|---|---|
| `ap-southeast-2` | Sydney | `us-east-1` |
| `ap-south-1` | Mumbai | `us-east-1` |
| `ap-southeast-4` | Melbourne | `us-east-1` |

## Multi-region / residency / DR labs

An architecture that spans regions in the **design** (residency in Mumbai, a DR copy in Melbourne) is
**deployed in `us-east-1`** like everything else:

- The **design and assessment stay multi-region** — the student still designs for, and is assessed on,
  the correct regions and the reasoning behind them.
- The **deployment is single-region** — each regional component is deployed to `us-east-1` (a second
  "region" becomes a **second stack in `us-east-1`**, not a second real region). The substitution token
  on each deploy step makes this explicit.
- An **in-world note** states that the geography is simulated for the lab, so the scenario stays
  coherent.

Do **not** fake a second region with a second AZ (`us-east-1b` as "Mumbai") — an AZ is not a region, and
pretending otherwise misteaches the cross-region boundary. The honest position is: real region in the
design, one region in the deploy, simulated geography noted.

## Multi-AZ HA is real, not simulated

High availability **within** a region (multi-AZ) is **not** substituted — it deploys for real in
`us-east-1` (proven: RDS `MultiAZ: true` on `db.t3.medium` + an ASG across two AZs reach
`CREATE_COMPLETE`; see [lab-pack-standard.md](lab-pack-standard.md)). Students select two AZs in the
deploy region exactly as they would anywhere; **no substitution token is used for AZs** — the token is a
region-level construct only.

## Authoring checklist

- Design artefacts (designs, diagrams, scenarios, website) use the **real** scenario regions; **no**
  token.
- **Every** deployment step carries a `[scenario: … | deploy: …]` token — including identity cases.
- All tokens resolve against the **canonical mapping** above; no per-lab mappings.
- Residency/DR labs keep the **multi-region design** + a **simulated-geography** in-world note; deploy is
  single-region (extra stacks in `us-east-1`).
- Never substitute at AZ level — multi-AZ is real.

> **Enforcement (planned):** like the other course standards, this is intended to be machine-checkable —
> a linter that confirms every deployment-step region reference uses the token and resolves against the
> canonical mapping. Not yet built.
