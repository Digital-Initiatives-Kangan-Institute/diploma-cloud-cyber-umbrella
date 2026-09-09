#!/usr/bin/env python3
"""Validate ONE cluster's delivery-plan.md outline (the delivery Step-6 gate).

Deterministic, stdlib-only. The CONTRACT is not hard-coded here: the linter reads the format
document's ``## Skeleton`` block to learn the required headings, header fields and session-grid
columns, so the format document is the single source of truth. On top of that structural check it
verifies the grid's internal consistency, that every Topic and every assessment is placed, and that
the grid reconciles with the frame.

The delivery plan is a SEMESTER-INSTANCE artefact produced in a human-AI juggling session. This gate
is a COMPLETENESS-FOR-GENERATION check: a PASS means the outline holds every decision the docx
generator needs. Every failure is a decision still to be made, so the producing session can keep
prompting the human. It does NOT judge whether the sequence is good (spacing, catch-up placement,
online/classroom mix) -- that is the human's call, made live.

SCOPE IS ONE CLUSTER. ``--plan`` and ``--cluster-dir`` are two ways to name the same file; the
whole-of-semester plan is step 07's separate ``validate_semester_delivery_plan.py``.

Behaviour is specified by cases CDP-01 .. CDP-29 in factory/docs/test-plan.md.

Usage:
  python validate_cluster_delivery_plan.py --plan <cluster>/delivery/delivery-plan.md
  python validate_cluster_delivery_plan.py --cluster-dir <S1-CLx dir>
  [--format <path to the delivery-plan format standard>]   # auto-located if omitted

Exit 0 on PASS, 1 otherwise.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

# Shared machinery lives in the factory's common helpers -- never re-create it here.
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common" / "helpers"))
from format_contract import find_format_doc, parse_contract, parse_labelled_fields  # noqa: E402
from numeric import fmt, num  # noqa: E402

FORMAT_DOC_NAME = "delivery-plan-format.md"

# --- vocabularies (intrinsic to the artefact; the format doc documents them in prose) ---
MODES = {"online", "classroom"}
ACTIVITIES = {"onboarding", "teach", "practice", "practical", "presentation", "assessment", "spare"}

# --- header-field label whose VALUE the reconciliation needs (name must match the skeleton) ---
F_TOTAL = "Total sessions available"

# --- how each required grid column is recognised in the plan's table header (substring, lower-case) ---
COLUMN_ROLES = {
    "num": ["#", "session", "no"],
    "date": ["date"],
    "week": ["week"],
    "time": ["time"],
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


def extract_grid(text: str) -> list[tuple[list[str], int]]:
    """Rows of the session-grid table as (cells, source_line_no), header row first."""
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
    """The sibling cluster-specification.md frame fields, if it is there."""
    spec = plan.parent.parent / "cluster-specification.md"
    if not spec.is_file():
        return {}
    return parse_labelled_fields(spec.read_text(encoding="utf-8", errors="ignore"))


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

    ap = argparse.ArgumentParser(
        description="Validate one cluster's delivery-plan.md outline (delivery Step-6 gate)."
    )
    ap.add_argument("--plan", help="path to the cluster's delivery-plan.md")
    ap.add_argument("--cluster-dir", dest="cluster_dir",
                    help="a cluster directory; the same file, reached as delivery/delivery-plan.md")
    ap.add_argument("--format", dest="fmt_doc", help="path to the delivery-plan format standard")
    args = ap.parse_args()

    if args.plan:
        plan = Path(args.plan)
    elif args.cluster_dir:
        plan = Path(args.cluster_dir) / "delivery" / "delivery-plan.md"
    else:
        ap.error("give --plan or --cluster-dir")
    if not plan.is_file():
        print(f"ERROR: delivery plan not found: {plan}")
        return 1

    fmt_doc = find_format_doc(FORMAT_DOC_NAME, explicit=args.fmt_doc,
                              start=Path(__file__).resolve().parent)
    if fmt_doc is None:
        print(f"ERROR: format doc not found - pass --format <{FORMAT_DOC_NAME}>")
        return 1
    req_headings, req_fields, req_columns = parse_contract(fmt_doc.read_text(encoding="utf-8"))
    if not req_headings or not req_columns:
        print(f"ERROR: could not parse a contract from {fmt_doc} (## Skeleton block)")
        return 1

    text = plan.read_text(encoding="utf-8")
    errors, warnings, notes = [], [], []

    # --- structure from the contract ---
    if not re.search(r"^#\s+.+Delivery Plan\b", text, re.MULTILINE):
        errors.append("missing title '# <cluster> - Delivery Plan (<intake>)'")
    if not re.search(r"^>\s*\*\*INSTANCE:", text, re.MULTILINE):
        errors.append("missing '> **INSTANCE:** ...' banner line")
    for h in req_headings:
        if h not in text:
            errors.append(f"missing required heading: {h}")

    header_fields = parse_labelled_fields(text)
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
        errors.append("no session-grid table found (or it has no rows)")
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
    session_dates: list[tuple[int, date, str]] = []
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
            label = cells[roles["num"]] or f"@line {lineno}"
            for role in ("date", "week", "day", "time", "mode", "activity"):
                if cells[roles[role]] == "":
                    errors.append(f"session {label}: empty '{role}' (undecided)")
            if cells[roles["placed"]] == "":
                errors.append(
                    f"session {label}: 'Placed' is blank "
                    f"- write an em dash for an intentionally-empty session"
                )
            mode = cells[roles["mode"]].lower()
            if mode and mode not in MODES:
                errors.append(
                    f"session {label}: invalid Mode '{cells[roles['mode']]}' (use {sorted(MODES)})"
                )
            raw_date = cells[roles["date"]]
            if raw_date:
                try:
                    session_dates.append((int(n) if n is not None else 0,
                                          date.fromisoformat(raw_date), label))
                except ValueError:
                    errors.append(
                        f"session {label}: Date '{raw_date}' is not ISO YYYY-MM-DD"
                    )
            activity = cells[roles["activity"]].lower()
            if activity and activity not in ACTIVITIES:
                errors.append(
                    f"session {label}: invalid Activity '{cells[roles['activity']]}' "
                    f"(use {sorted(ACTIVITIES)})"
                )

    # --- grid contiguity 1..N ---
    n_rows = len(session_numbers)
    if session_numbers:
        expected = list(range(1, n_rows + 1))
        if sorted(session_numbers) != expected:
            detail = []
            gaps = sorted(set(expected) - set(session_numbers))
            if gaps:
                detail.append(f"missing #: {gaps}")
            dupes = sorted({x for x in session_numbers if session_numbers.count(x) > 1})
            if dupes:
                detail.append(f"duplicate #: {dupes}")
            extra = sorted(set(session_numbers) - set(expected))
            if extra:
                detail.append(f"out-of-range #: {extra}")
            errors.append(f"session numbers are not contiguous 1..{n_rows} ({'; '.join(detail)})")

    # --- dates run forward ---
    for (_, earlier, _), (_, later, label) in zip(session_dates, session_dates[1:]):
        if later < earlier:
            errors.append(
                f"session {label}: Date {later.isoformat()} goes backwards "
                f"(the session before it is {earlier.isoformat()}) - sessions run forward in time"
            )

    # --- placement coverage: every Topic + every AT placed ---
    topics, ats = enumerate_targets(plan)
    placed_text = ""
    if not missing_cols and data_rows:
        placed_text = " ".join(
            cells[roles["placed"]] for cells, _ in data_rows if len(cells) > roles["placed"]
        )
    if not topics:
        warnings.append("no delivery/topic_NN/ dirs found - cannot check Topic placement")
    for t in topics:
        if (not re.search(rf"\bT0*{t}\b", placed_text)
                and not re.search(rf"\btopic\s*0*{t}\b", placed_text, re.IGNORECASE)):
            errors.append(f"Topic T{t} is not placed in any session (gap)")
    if not ats:
        warnings.append("no assessments/AT<n>/ dirs found - cannot check assessment placement")
    for a in ats:
        if not re.search(rf"\bAT0*{a}\b", placed_text, re.IGNORECASE):
            errors.append(f"assessment AT{a} is not placed in any session (gap)")

    # --- reconcile with the declared instance total + the frame ---
    declared_total = num(header_fields.get(F_TOTAL))
    if declared_total is not None and n_rows and int(declared_total) != n_rows:
        errors.append(
            f"grid has {n_rows} session rows but '{F_TOTAL}' says {fmt(declared_total)} - reconcile"
        )

    frame = read_frame(plan)
    if frame:
        fr_total = num(frame.get(FR_TOTAL))
        if fr_total is not None and declared_total is not None and fr_total != declared_total:
            sign = "+" if declared_total > fr_total else ""
            notes.append(
                f"intake has {fmt(declared_total)} sessions vs frame nominal {fmt(fr_total)} "
                f"({sign}{fmt(declared_total - fr_total)}) - instance allocation"
            )
        if not missing_cols and data_rows:
            acts = [
                cells[roles["activity"]].lower()
                for cells, _ in data_rows if len(cells) > roles["activity"]
            ]
            fr_onb = num(frame.get(FR_ONB))
            fr_spare = num(frame.get(FR_SPARE))
            fr_assess = num(frame.get(FR_ASSESS))
            if fr_onb and fr_onb > 0 and acts.count("onboarding") == 0:
                errors.append(f"frame budgets {fmt(fr_onb)} onboarding session(s) but the grid has none")
            if fr_spare and fr_spare > 0 and acts.count("spare") == 0:
                errors.append(f"frame budgets {fmt(fr_spare)} spare session(s) but the grid has none")
            notes.append(
                f"reservations - onboarding {acts.count('onboarding')} "
                f"(frame {fmt(fr_onb) if fr_onb is not None else '?'}), "
                f"spare {acts.count('spare')} (frame {fmt(fr_spare) if fr_spare is not None else '?'}), "
                f"assessment {acts.count('assessment')} "
                f"(frame dedicated {fmt(fr_assess) if fr_assess is not None else '?'})"
            )
    else:
        warnings.append("cluster-specification.md not found beside the plan - skipped frame reconciliation")

    # --- mode split (info) ---
    if not missing_cols and data_rows:
        modes = [cells[roles["mode"]].lower() for cells, _ in data_rows if len(cells) > roles["mode"]]
        notes.append(f"mode split - online {modes.count('online')}, classroom {modes.count('classroom')}")

    # --- report ---
    print(f"  contract: {fmt_doc}  "
          f"({len(req_headings)} headings, {len(req_fields)} fields, {len(req_columns)} columns)")
    print(f"  plan: {plan}  ({n_rows} sessions; {len(topics)} topics, {len(ats)} assessments to place)")
    for n in notes:
        print(f"  [plan] {n}")
    for w in warnings:
        print(f"  [warn] {w}")

    if errors:
        print()
        for e in errors:
            print(f"  FAIL: {e}")
        print(f"\nRESULT: FAIL - {len(errors)} decision(s)/issue(s) outstanding in {plan}")
        return 1

    print(f"\nRESULT: PASS - {plan} is complete enough to generate the delivery-plan docx.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
