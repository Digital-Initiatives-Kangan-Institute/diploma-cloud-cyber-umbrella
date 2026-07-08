#!/usr/bin/env python3
"""Validate a cluster's assessment_plan.md against the assessment-plan format standard.

Two checks (see docs/assessment-plan-format.md):

  FORMAT (linter — deterministic): the required sections are present and in order; the header carries a
    STATUS + Scenario-binding line; §3 has an AT table and a per-AT block carrying both a 'UoC coverage:'
    and a 'Scenario requirements:' field; §6 is a scenario-requirements register of well-formed SR-<CL>-NN
    rows; every SR-* referenced in §3 is defined in §6 (and, advisory, every §6 SR is referenced).

  COVERAGE: every PC/PE/KE/FS item in the cluster's consolidated_uoc.md is referenced by at least one AT's
    'UoC coverage:' (the canonical [UNIT SEC num] tags). AC items are discharged via the SR register, so
    they are not required here (reported as info). Phantom refs (tags that are not real UoC items) fail.

Reuses the bundled tag machinery (resolve_tags / valid_tag_set); stdlib only.

Usage:
  validate_assessment_plan.py --cluster <S1-CLx dir> [--plan <path>] [--consolidated <path>]

Exit 0 = PASS (format valid AND every required item covered, no phantoms).
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_at_traceability import resolve_tags, valid_tag_set

SR_RE = re.compile(r"\bSR-([A-Z]+\d+)-(\d+)\b")

# (regex for the heading, human label) in required order
REQUIRED = [
    (r"^#\s+.*Cluster Assessment Plan\b", "title — '# … Cluster Assessment Plan'"),
    (r"^##\s+1\.\s+Integration approach\b", "## 1. Integration approach"),
    (r"^##\s+2\.\s+Scenario\b", "## 2. Scenario"),
    (r"^##\s+3\.\s+Assessment structure\b", "## 3. Assessment structure"),
    (r"^##\s+4\.\s+Provenance\b", "## 4. Provenance"),
    (r"^##\s+5\.\s+Coverage verification\b", "## 5. Coverage verification"),
    (r"^##\s+6\.\s+Scenario requirements register\b", "## 6. Scenario requirements register"),
    (r"^##\s+7\.\s+Worklist\b", "## 7. Worklist"),
    (r"^##\s+8\.\s+Open questions\b", "## 8. Open questions"),
    (r"^##\s+Changelog\b", "## Changelog"),
]


def section_span(lines, start_pat, end_pats):
    """Return the text of the section whose heading matches start_pat, up to the next end heading."""
    start = next((i for i, ln in enumerate(lines) if re.match(start_pat, ln)), None)
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if any(re.match(p, lines[j]) for p in end_pats):
            end = j
            break
    return "\n".join(lines[start:end])


def check_format(text, cl_token):
    """Return (problems, advisories, found_uoc_tags, sr_refs, sr_defs)."""
    lines = text.splitlines()
    problems, advisories = [], []

    # 1) required sections present + in order
    last_idx = -1
    for pat, label in REQUIRED:
        idx = next((i for i, ln in enumerate(lines) if re.match(pat, ln)), None)
        if idx is None:
            problems.append(f"missing required section: {label}")
        elif idx < last_idx:
            problems.append(f"section out of order: {label}")
        else:
            last_idx = idx

    # 2) header fields
    if not re.search(r"^>\s*\*\*STATUS", text, re.MULTILINE):
        problems.append("header missing a '> **STATUS** …' line")
    if "Scenario binding" not in text:
        problems.append("header missing a 'Scenario binding' line")

    # 3) §3 — AT table + per-AT blocks with UoC coverage + Scenario requirements
    sec3 = section_span(lines, r"^##\s+3\.", [r"^##\s+4\."]) or ""
    if not re.search(r"^\|.*\bAT1\b", sec3, re.MULTILINE):
        problems.append("§3 has no AT table row (expected a markdown table listing the ATs)")
    at_blocks = re.findall(r"^###\s+(AT\d+\b.*)$", sec3, re.MULTILINE)
    if not at_blocks:
        problems.append("§3 has no '### ATn' per-AT detail blocks")
    # split §3 into per-AT chunks to check each carries both fields
    chunks = re.split(r"^###\s+AT\d+\b.*$", sec3, flags=re.MULTILINE)[1:]
    labels = re.findall(r"^###\s+(AT\d+)\b", sec3, re.MULTILINE)
    found_uoc = set()
    sr_refs = set()
    for label, chunk in zip(labels, chunks):
        if "UoC coverage:" not in chunk:
            problems.append(f"{label} block missing a 'UoC coverage:' field")
        if "Scenario requirements:" not in chunk:
            problems.append(f"{label} block missing a 'Scenario requirements:' field")
        for line in chunk.splitlines():
            if "UoC coverage:" in line:
                for tag, form in resolve_tags(line):
                    if form == "unresolved" or tag.startswith("?? "):
                        problems.append(f"{label} UoC coverage has an unresolved tag: {tag}")
                    else:
                        found_uoc.add(tag)
            if "Scenario requirements:" in line:
                sr_refs.update(f"SR-{a}-{b}" for a, b in SR_RE.findall(line))

    # 4) §6 — SR register definitions
    sec6 = section_span(lines, r"^##\s+6\.", [r"^##\s+7\."]) or ""
    sr_defs = {f"SR-{a}-{b}" for a, b in SR_RE.findall(sec6)}
    if not sr_defs:
        problems.append("§6 scenario requirements register defines no SR-… rows")
    for sr in sorted(sr_defs):
        if not sr.startswith(f"SR-{cl_token}-"):
            problems.append(f"§6 SR id '{sr}' is not cluster-scoped (expected SR-{cl_token}-NN)")

    # 5) cross-refs: every SR referenced in §3 is defined in §6; advise on unreferenced defs
    for sr in sorted(sr_refs - sr_defs):
        problems.append(f"§3 references {sr}, which is not defined in §6")
    for sr in sorted(sr_defs - sr_refs):
        advisories.append(f"§6 defines {sr} but no AT references it")

    return problems, advisories, found_uoc, sr_refs, sr_defs


def check_coverage(found_uoc, consolidated: Path):
    """Return (missing, phantom, info_ac). Coverage of PC/PE/KE/FS; AC is informational."""
    valid = valid_tag_set(consolidated)
    required = {t for t in valid if t.split()[1] in ("PC", "PE", "KE", "FS")}
    missing = sorted(required - found_uoc)
    phantom = sorted(found_uoc - valid)
    info_ac = sorted({t for t in found_uoc if t.split()[1] == "AC"})
    return missing, phantom, info_ac, len(required)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description="Validate a cluster assessment_plan.md (format + coverage).")
    ap.add_argument("--cluster", required=True, type=Path)
    ap.add_argument("--plan", type=Path, help="default <cluster>/assessments/assessment_plan.md")
    ap.add_argument("--consolidated", type=Path, help="default <cluster>/consolidated_uoc.md")
    args = ap.parse_args()

    plan = args.plan or (args.cluster / "assessments" / "assessment_plan.md")
    consolidated = args.consolidated or (args.cluster / "consolidated_uoc.md")
    if not plan.exists():
        print(f"No assessment plan at {plan}"); sys.exit(2)
    cl = re.search(r"(CL\d+)", args.cluster.name)
    cl_token = cl.group(1) if cl else "CL?"

    text = plan.read_text(encoding="utf-8")
    print(f"=== {plan} ===")

    problems, advisories, found_uoc, sr_refs, sr_defs = check_format(text, cl_token)
    if not problems:
        print(f"  FORMAT: PASS — all sections present; {len(sr_defs)} SR defined, {len(sr_refs)} referenced")
    else:
        print(f"  FORMAT: FAIL — {len(problems)} issue(s)")
        for p in problems:
            print(f"    [FAIL] {p}")
    for a in advisories:
        print(f"    [info] {a}")

    cov_fail = False
    if consolidated.exists():
        missing, phantom, info_ac, n_req = check_coverage(found_uoc, consolidated)
        if not missing and not phantom:
            print(f"  COVERAGE: PASS — all {n_req} PC/PE/KE/FS items referenced by an AT"
                  + (f" (+{len(info_ac)} AC via SR register)" if info_ac else ""))
        else:
            cov_fail = True
            print(f"  COVERAGE: FAIL — {len(missing)} missing, {len(phantom)} phantom (of {n_req} required)")
            for m in missing:
                print(f"    [MISSING] {m} — no AT's UoC coverage references it")
            for p in phantom:
                print(f"    [PHANTOM] {p} — not a real UoC item")
    else:
        print(f"  COVERAGE: SKIPPED — no consolidated UoC at {consolidated}")

    ok = not problems and not cov_fail
    print("\nRESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
