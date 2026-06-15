---
name: feedback-verify-change-impact
description: Before any side-effecting change (esp. running generators / creating files), verify WHERE output lands and WHAT gets staged — a "helpful" regenerate created a phantom nested sub-repo that got committed.
metadata:
  type: feedback
---

Before making a side-effecting change — especially **running a generator or any script that writes
files** — stop and verify *where the bytes land* and *what would get staged*, not just that the script
ran. A past session helpfully re-ran content generators without checking, and their **relative default
output paths** (e.g. `../diploma-cloud-cyber-website/public/...`) resolved one level too shallow from
the wrong working dir → `..` became the **content repo** instead of the umbrella → a phantom
`diploma-cloud-cyber-content/diploma-cloud-cyber-website/` tree was created **and committed to content**
(stale stubs + a misdirected unique doc), silently breaking the umbrella↔sub-repo separation.

**Why:** in this umbrella+gitignored-sub-repos layout, a relative path is only correct from one cwd;
a wrong one creates a plausible-looking duplicate tree that goes stale and pollutes a repo that should
hold none of those artefacts. "It generated without error" is **not** evidence it did the right thing.

**How to apply:** before running a writer, confirm its resolved output path (print/inspect the
`Default:`/argv target); after, `git status` the affected repo to see exactly what changed and where;
treat unexpected new paths as a red flag, not noise. Same caution as [[feedback-suggest-commits]] and
the no-unilateral-changes rule — think about the **impact** of a change, don't just be helpfully busy.
Relates to [[memory-principles-not-state]] (a stale duplicate is exactly the rot that creates).
