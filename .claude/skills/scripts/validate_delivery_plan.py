#!/usr/bin/env python3
"""Validate a delivery-plan.md outline (the delivery-run-sheet Step-6 artefact).

Deterministic, stdlib-only. The CONTRACT is not hard-coded here: the linter reads the
format document's ``## Skeleton`` block (docs/delivery-plan-format.md) to learn the required
headings, header fields and session-grid columns, so the format doc is the single source of
truth. On top of that structural check it verifies the grid's internal consistency, that
every Topic and every assessment is placed, and that the grid reconciles with the frame.

The delivery plan is a SEMESTER-INSTANCE artefact produced in a human-AI juggling session.
This gate is a COMPLETENESS-FOR-GENERATION check: a PASS means the outline holds every
decision the docx generator needs. Every failure is a decision still to be made -- so the
producing session can keep prompting the human until the plan is complete. It does NOT judge
whether the sequence is good (spacing, catch-up, online/classroom mix) -- that is the human
call made live in the juggling session.

Checks:
  - every heading / header field / grid column NAMED IN THE SKELETON is present (fields non-empty);
  - the session grid is internally consistent (numbered 1..N contiguously; every cell decided;
    Mode + Activity in vocabulary);
  - every built Topic (delivery/topic_NN/) and every assessment (assessments/AT<n>/) is placed;
  - the grid reconciles with the frame (row count == declared total; reservations honoured);
  - REPORTS divergence from the frame's nominal total, the mode split, and the assessment count.

Usage:
  python validate_delivery_plan.py --plan <cluster>/delivery/delivery-plan.md
  python validate_delivery_plan.py --cluster <S1-CLx dir>   # finds delivery/delivery-plan.md
  [--format <path to delivery-plan-format.md>]              # auto-located if omitted

Exit 0 on PASS, 1 otherwise.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# --- vocabularies (intrinsic to the artefact; the format doc documents them in prose) ---
MODES = {"online", "classroom"}
ACTIVITIES = {"onboarding", "teach", "practice", "practical", "presentation", "assessment", "spare"}

# --- header-field labels whose VALUES the reconciliation needs (names must match the skeleton) ---
F_TOTAL = "Total sessions available"

# --- how each required grid column is recognised in the plan's table header (substring, lower-case) ---
COLUMN_ROLES = {
    "num": ["#", "session", "no"],
    "week": ["week"],
    "day": ["day"],
    "mode": ["mode"],
    "activity": ["activity"],
    "placed": ["placed", "content", "topic"],
}

# --- frame fields consumed from cluster-specification.md ---
FR_TOTAL = "Total sessions"
FR_ONB = "Onboarding sessions"
FR_SPARE = "Spare sessions"
FR_ASSESS = "Dedicated assessment sessions"


def find_format_doc(explicit: str | None) -> Path | None:
    if explicit:
        p = Path(explicit)
        return p if p.is_file() else None
    name = "delivery-plan-format.md"
    here = Path(__file__).resolve()
    candidates = [
        Path("docs") / name,
        Path("..") / "docs" / name,
        Path("..") / ".." / "docs" / name,
    ]
    for parent in here.parents:
        candidates.append(parent / "docs" / name)
    for c in candidates:
        if c.is_file():
            return c
    return None


def parse_contract(format_text: str) -> tuple[list[str], list[str], list[str]]:
    """Extract (headings, header-field-labels, grid-column-names) from the ``## Skeleton`` block."""
    m = re.search(r"##\s+Skeleton\s*\n+```[a-zA-Z]*\n(.*?)\n```", format_text, re.DOTALL)
    if not m:
        return [], [], []
    block = m.group(1)
    headings = list(dict.fromkeys(re.findall(r"^(##\s+.+?)\s*$", block, re.MULTILINE)))
    fields = list(dict.fromkeys(
        lbl.strip() for lbl in re.findall(r"^-\s*([^:\n]+?):", block, re.MULTILINE)
    ))
    # grid columns = the first table header row inside the skeleton
    columns: list[str] = []
    for line in block.splitlines():
        if line.lstrip().startswith("|") and re.search(r"[A-Za-z#]", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if any(re.search(r"-{3,}", c) for c in cells):
                continue  # separator row
            columns = [c for c in cells if c]
            break
    return headings, fields, columns


def parse_header_fields(text: str) -> dict:
    """Labelled ``- Field: value`` lines that are NOT inside a table (grid rows start with '|')."""
    fields = {}
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            continue
        m = re.match(r"\s*-\s*([^:]+?):\s*(.*?)\s*$", line)
        if m:
            fields[m.group(1).strip()] = m.group(2).strip()
    return fields


def num(value):
    if value is None:
        return None
    m = re.search(r"[-+]?\d+(?:\.\d+)?", value.replace("−", "-"))
    return float(m.group(0)) if m else None


def fmt(x) -> str:
    return str(int(x)) if x is not None and float(x).is_integer() else str(x)


def extract_grid(text: str) -> list[tuple[list[str], int]]:
    """Return the rows of the '## 2. Session grid' table as (cells, source_line_no)."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^##\s+.*Session grid", line, re.IGNORECASE):
            start = i + 1
            break
    if start is None:
        return []
    rows = []
    for i in range(start, len(lines)):
        line = lines[i]
        if line.strip().startswith("##"):
            break
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if any(re.search(r"^-{3,}$", c) for c in cells):
            continue  # separator
        rows.append((cells, i + 1))
    return rows


def locate_columns(header_cells: list[str]) -> tuple[dict, list[str]]:
    """Map each required role to a column index by substring match. Returns (roles, missing)."""
    lowered = [c.lower() for c in header_cells]
    roles, missing = {}, []
    for role, keys in COLUMN_ROLES.items():
        idx = None
        for j, name in enumerate(lowered):
            if any(k == name or k in name for k in keys):
                idx = j
                break
        if idx is None:
            missing.append(role)
        else:
            roles[role] = idx
    return roles, missing


def read_frame(plan: Path) -> dict:
    """Read the sibling cluster-specification.md frame fields, if present."""
    spec = plan.parent.parent / "cluster-specification.md"
    if not spec.is_file():
        return {}
    fields = {}
    for line in spec.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.match(r"\s*-\s*([^:]+?):\s*(.*?)\s*$", line)
        if m:
            fields[m.group(1).strip()] = m.group(2).strip()
    return fields


def enumerate_targets(plan: Path) -> tuple[list[int], list[int]]:
    """Topic numbers (delivery/topic_NN/) and assessment numbers (assessments/AT<n>/)."""
    cluster = plan.parent.parent
    topics = sorted(
        int(re.search(r"(\d+)", d.name).group(1))
        for d in (cluster / "delivery").glob("topic_*")
        if d.is_dir() and re.search(r"\d", d.name)
    )
    ats = sorted(
        int(re.search(r"(\d+)", d.name).group(1))
        for d in (cluster / "assessments").glob("AT*")
        if d.is_dir() and re.search(r"\d", d.name)
    )
    return topics, ats


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser(description="Validate a delivery-plan.md outline (Step-6 gate).")
    ap.add_argument("--plan", help="path to delivery-plan.md")
    ap.add_argument("--cluster", help="an S1-CLx dir; finds delivery/delivery-plan.md inside")
    ap.add_argument("--format", dest="fmt_doc", help="path to delivery-plan-format.md")
    args = ap.parse_args()

    if args.plan:
        plan = Path(args.plan)
    elif args.cluster:
        plan = Path(args.cluster) / "delivery" / "delivery-plan.md"
    else:
        ap.error("give --plan or --cluster")
    if not plan.is_file():
        print(f"ERROR: delivery plan not found: {plan}")
        return 1

    fmt_doc = find_format_doc(args.fmt_doc)
    if fmt_doc is None:
        print("ERROR: format doc not found - pass --format <delivery-plan-format.md>")
        return 1
    req_headings, req_fields, req_columns = parse_contract(fmt_doc.read_text(encoding="utf-8"))
    if not req_headings or not req_columns:
        print(f"ERROR: could not parse a contract from {fmt_doc} (## Skeleton block)")
        return 1

    text = plan.read_text(encoding="utf-8")
    errors, warnings, notes = [], [], []

    # --- structure from the contract ---
    if not re.search(r"^#\s+.+Delivery Plan\b", text, re.MULTILINE):
        errors.append("missing title '# <cluster> — Delivery Plan (<intake>)'")
    if not re.search(r"^>\s*\*\*INSTANCE:", text, re.MULTILINE):
        errors.append("missing '> **INSTANCE:** …' banner line")
    for h in req_headings:
        if h not in text:
            errors.append(f"missing required heading: {h}")

    header_fields = parse_header_fields(text)
    for label in req_fields:
        if label not in header_fields:
            errors.append(f"missing header field: '{label}'")
        elif header_fields[label] == "":
            errors.append(f"empty header field: '{label}'")

    # --- session grid ---
    grid = extract_grid(text)
    roles, missing_cols = {}, list(COLUMN_ROLES)
    data_rows = []
    if not grid:
        errors.append("no '## 2. Session grid' table found (or it has no rows)")
    else:
        header_cells = grid[0][0]
        for col in req_columns:
            if not any(col.lower() == c.lower() or col.lower() in c.lower() for c in header_cells):
                errors.append(f"session grid missing column: '{col}'")
        roles, missing_cols = locate_columns(header_cells)
        for role in missing_cols:
            errors.append(f"session grid: cannot locate a '{role}' column")
        data_rows = grid[1:]

    session_numbers = []
    if not missing_cols and data_rows:
        for cells, lineno in data_rows:
            if len(cells) <= max(roles.values()):
                errors.append(f"grid row (line {lineno}) has too few cells: {cells}")
                continue
            n = num(cells[roles["num"]])
            if n is None:
                errors.append(f"grid row (line {lineno}) has no session number: {cells[roles['num']]!r}")
            else:
                session_numbers.append(int(n))
            # every cell must be decided
            for role in ("week", "day", "mode", "activity"):
                if cells[roles[role]] == "":
                    errors.append(f"session {cells[roles['num']] or f'@line {lineno}'}: empty '{role}' (undecided)")
            placed = cells[roles["placed"]]
            if placed == "":
                errors.append(
                    f"session {cells[roles['num']] or f'@line {lineno}'}: 'Placed' is blank "
                    f"— write '—' for an intentionally-empty session"
                )
            mode = cells[roles["mode"]].lower()
            if mode and mode not in MODES:
                errors.append(f"session {cells[roles['num']]}: invalid Mode '{cells[roles['mode']]}' (use {sorted(MODES)})")
            activity = cells[roles["activity"]].lower()
            if activity and activity not in ACTIVITIES:
                errors.append(f"session {cells[roles['num']]}: invalid Activity '{cells[roles['activity']]}' (use {sorted(ACTIVITIES)})")

    # --- grid contiguity 1..N ---
    n_rows = len(session_numbers)
    if session_numbers:
        expected = list(range(1, n_rows + 1))
        if sorted(session_numbers) != expected:
            dupes = sorted({x for x in session_numbers if session_numbers.count(x) > 1})
            gaps = sorted(set(expected) - set(session_numbers))
            detail = []
            if gaps:
                detail.append(f"missing #: {gaps}")
            if dupes:
                detail.append(f"duplicate #: {dupes}")
            extra = sorted(set(session_numbers) - set(expected))
            if extra:
                detail.append(f"out-of-range #: {extra}")
            errors.append(f"session numbers are not contiguous 1..{n_rows} ({'; '.join(detail)})")

    # --- placement coverage: every Topic + every AT placed ---
    topics, ats = enumerate_targets(plan)
    placed_text = ""
    if not missing_cols and data_rows:
        placed_text = " ".join(cells[roles["placed"]] for cells, _ in data_rows if len(cells) > roles["placed"])
    if not topics:
        warnings.append("no delivery/topic_NN/ dirs found — cannot check Topic placement")
    for t in topics:
        if not re.search(rf"\bT0*{t}\b", placed_text) and not re.search(rf"\btopic\s*0*{t}\b", placed_text, re.IGNORECASE):
            errors.append(f"Topic T{t} is not placed in any session (gap)")
    if not ats:
        warnings.append("no assessments/AT<n>/ dirs found — cannot check assessment placement")
    for a in ats:
        if not re.search(rf"\bAT0*{a}\b", placed_text, re.IGNORECASE):
            errors.append(f"assessment AT{a} is not placed in any session (gap)")

    # --- reconcile with the declared instance total + the frame ---
    declared_total = num(header_fields.get(F_TOTAL))
    if declared_total is not None and n_rows and int(declared_total) != n_rows:
        errors.append(
            f"grid has {n_rows} session rows but '{F_TOTAL}' says {fmt(declared_total)} — reconcile"
        )

    frame = read_frame(plan)
    if frame:
        fr_total = num(frame.get(FR_TOTAL))
        if fr_total is not None and declared_total is not None and fr_total != declared_total:
            notes.append(
                f"intake has {fmt(declared_total)} sessions vs frame nominal {fmt(fr_total)} "
                f"({'+' if declared_total > fr_total else ''}{fmt(declared_total - fr_total)}) — instance allocation"
            )
        # reservations the frame budgets for must appear in the grid
        if not missing_cols and data_rows:
            acts = [cells[roles["activity"]].lower() for cells, _ in data_rows if len(cells) > roles["activity"]]
            fr_onb = num(frame.get(FR_ONB))
            fr_spare = num(frame.get(FR_SPARE))
            fr_assess = num(frame.get(FR_ASSESS))
            if fr_onb and fr_onb > 0 and acts.count("onboarding") == 0:
                errors.append(f"frame budgets {fmt(fr_onb)} onboarding session(s) but the grid has none")
            if fr_spare and fr_spare > 0 and acts.count("spare") == 0:
                errors.append(f"frame budgets {fmt(fr_spare)} spare session(s) but the grid has none")
            notes.append(
                f"reservations — onboarding {acts.count('onboarding')} (frame {fmt(fr_onb) if fr_onb is not None else '?'}), "
                f"spare {acts.count('spare')} (frame {fmt(fr_spare) if fr_spare is not None else '?'}), "
                f"assessment {acts.count('assessment')} (frame dedicated {fmt(fr_assess) if fr_assess is not None else '?'})"
            )
    else:
        warnings.append("cluster-specification.md not found beside the plan — skipped frame reconciliation")

    # --- mode split (info) ---
    if not missing_cols and data_rows:
        modes = [cells[roles["mode"]].lower() for cells, _ in data_rows if len(cells) > roles["mode"]]
        notes.append(f"mode split — online {modes.count('online')}, classroom {modes.count('classroom')}")

    # --- report ---
    print(f"  contract: {fmt_doc}  ({len(req_headings)} headings, {len(req_fields)} fields, {len(req_columns)} columns)")
    print(f"  plan: {plan}  ({n_rows} sessions; {len(topics)} topics, {len(ats)} assessments to place)")
    for n in notes:
        print(f"  [plan] {n}")
    for w in warnings:
        print(f"  [warn] {w}")

    if errors:
        print()
        for e in errors:
            print(f"  FAIL: {e}")
        print(f"\nRESULT: FAIL — {len(errors)} decision(s)/issue(s) outstanding in {plan}")
        return 1

    print(f"\nRESULT: PASS — {plan} is complete enough to generate the delivery-plan docx.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
