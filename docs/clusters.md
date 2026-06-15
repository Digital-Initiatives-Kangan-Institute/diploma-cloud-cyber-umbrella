# Diploma of IT (Cloud & Cyber Security) — Suggested Cluster Structure

> Status: **draft / proposed**. Tim has scope to challenge the clustering if a unit is clearly misplaced. This document captures the clustering as it currently stands so it can be reasoned about, refined and signed off.

## Semester 1 — Cloud focus

### Cluster: Cloud Design and Build
| Unit code | Unit title |
|---|---|
| ICTCLD502 | Design and implement highly-available cloud infrastructure |
| ICTCLD401 | Configure cloud services |
| ICTICT517 | Match ICT needs with the strategic direction of the organisation |

### Cluster: Cloud Disaster Recovery
| Unit code | Unit title |
|---|---|
| ICTCLD501 | Develop cloud disaster recovery plans |
| ICTCLD503 | Implement web-scale cloud infrastructure |
| ICTCLD505 | Implement cloud infrastructure with code |

### Cluster: Cloud Improve Infra as a Team
| Unit code | Unit title |
|---|---|
| ICTCLD504 | Improve cloud-based infrastructure |
| BSBXTW401 | Lead and facilitate a team |

---

## Semester 2 — Cyber Security focus

### Cluster: Cyber Design
| Unit code | Unit title |
|---|---|
| ICTCYS613 | Utilise design methodologies for security architecture |
| ICTSAS524 | Develop, implement and evaluate an incident response plan |
| ICTSAS526 | Review and update disaster recovery and contingency plans |

### Cluster: Cyber Policy
| Unit code | Unit title |
|---|---|
| BSBXCS402 | Promote workplace cyber security awareness and best practices |
| ICTICT532 | Apply IP, ethics and privacy in ICT environments |

### Cluster: Enterprise Systems
| Unit code | Unit title |
|---|---|
| ICTCYS610 | Protect critical infrastructure for organisations |
| ICTNWK553 | Configure enterprise virtual computing environments |
| VU23226 | Test Concepts / Procedures for Cyber Exploitation |
| ICTNWK540 | Design, build and test network servers |

### Cluster: Threat Hunting
| Unit code | Unit title |
|---|---|
| ICTCYS407 | Gather, analyse and interpret threat data |
| BSBCRT512 | Originate and develop concepts |
| ICTSAS527 | Manage client problems |

---

## Summary

- **Total clusters:** 7 (3 cloud + 4 cyber)
- **Total units:** 20 (Semester 1: 8 across 3 clusters · Semester 2: 12 across 4 clusters)
- **Atomic unit of delivery and assessment:** the **cluster**, not the course
- **Cross-cluster duplication:** acceptable
- **Within-cluster duplication:** to be removed by combining/remapping assessments

## Notes on potential reconsideration

These are things to keep an eye on as we work through content mapping — they may or may not warrant moving a unit:

- **ICTSAS526** (DR/contingency plans) sits in *Cyber Design*, but ICTCLD501 (Cloud DR) is in *Cloud Disaster Recovery*. There is likely strong content overlap; question is whether ICTSAS526 should follow ICTCLD501 in semester 1, or whether the semester split (cloud → cyber) takes priority over the content affinity.
- **ICTICT517** (strategic ICT alignment) is grouped with hands-on cloud build units. May be a thin fit unless the cluster's project deliverable has a strategy/architecture artefact.
- **BSBCRT512** (originate and develop concepts) inside *Threat Hunting* — the creative/concept-generation lens applied to threat actor thinking is a defensible framing, but worth validating during the content map.
- **BSBXTW401** (lead and facilitate a team) paired only with ICTCLD504 — a two-unit cluster is small; check whether it warrants a third unit or whether the team-leadership lens is strong enough to carry a focused cluster.

## Source materials cross-check

- **ICTCLD505** (Cloud Disaster Recovery) has no folder of learning/assessment material under `original_materials/`, but its **UoC reference document is present** at `courseware/semester_1/cl_cloud_dissaster_recovery/units_of_competency/ICTCLD505_Complete_R1.docx`. We have everything we need to author against it.
- **VU23226** (Enterprise Systems) has **no folder *and* no UoC reference document** anywhere in the source. The UoC itself — Performance Criteria, Knowledge Evidence, etc. — is not in the supplied materials. This needs to be obtained (the VU prefix indicates a Victoria University accredited course unit, sourceable from training.gov.au / VETNet) before any cluster mapping can include it. This is the one place the read-only-originals principle has to flex: we won't chase *source learning content* upstream, but we do need the UoC reference itself, because without it we have no defined target to author against.
- **ICTPRG549** and **ICTSAS518** have folders in `original_materials` but are **not in the cluster list** — confirm they are intentionally out of scope (legacy units from a prior version of the diploma).
