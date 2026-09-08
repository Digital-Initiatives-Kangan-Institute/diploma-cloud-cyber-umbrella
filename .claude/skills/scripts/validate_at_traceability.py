#!/usr/bin/env python3
"""Validate an assessment task's UoC traceability — the bidirectional rule that every marking
criterion carries a unit-of-competency reference and every referenced item is a real UoC item.

This enforces, mechanically, the traceability discipline that is otherwise checked by eye:
  * No phantom references — every tag in the AT resolves to a real item in the cluster's
    consolidated_uoc.md (catches typos, wrong unit codes, stale numbers).
  * No free-floating criteria — every criterion in the Marking Benchmark / UoC-traceability
    section carries at least one tag (catches a criterion added without provenance).
  * Optionally, coverage — every item the AT is expected to evidence appears against a criterion
    (pass --expect with the per-AT allocation from the assessment plan).

It also reports, as advisories:
  * Abbreviated tags (e.g. `[KE 2]` with the unit implied) — the convention is full unit refs;
    these are resolved against the nearest preceding full tag on the line, but flagged.
  * Marking-guide criteria not found in the benchmark section (best-effort — depends on the AT's
    criterion-id scheme; skipped cleanly if none is detected).

Reads the AT from its .docx (the artefact of record) or a .md companion. Reuses the bundled
docx_to_text extractor; stdlib only.

Usage:
  validate_at_traceability.py --at <AT.docx|AT.md> --consolidated <cluster>/consolidated_uoc.md
      [--expect "<UNIT SEC num>" --expect "..."]      # optional reverse-coverage check

Exit 0 = PASS (no phantom tags, no untagged criteria, expected coverage met if given).
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_uoc import docx_to_text  # bundled, stdlib-only

FULL = re.compile(r"^(ICT\w+|BSB\w+|VU\d+)\s+(PC|FS|PE|KE|AC)\s+(.+)$")
ABBR = re.compile(r"^(PC|FS|PE|KE|AC)\s+(.+)$")
ANY_BRACKET = re.compile(r"\[([^\]]+)\]")
CRIT_ID = re.compile(r"^([A-Z]{1,2}\d+)\s*[—–-]\s*(.*)$")
BENCH_HEADING = re.compile(r"(benchmark|traceability)", re.IGNORECASE)


def load_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        return docx_to_text(path)
    return path.read_text(encoding="utf-8")


def valid_tag_set(consolidated: Path) -> set:
    """Every real item tag from the cluster's consolidated_uoc.md (code spans stripped)."""
    txt = re.sub(r"`[^`]*`", "", consolidated.read_text(encoding="utf-8"))
    out = set()
    for m in re.finditer(r"\[(ICT\w+|BSB\w+|VU\d+) (PC|FS|PE|KE|AC) ([^\]]+)\]", txt):
        out.add(f"{m.group(1)} {m.group(2)} {m.group(3).strip()}")
    return out


RANGE = re.compile(r"^(\d+(?:\.\d+)?)\s*[–—-]\s*(\d+(?:\.\d+)?)$")


def is_compressed(num: str) -> bool:
    return ("," in num) or bool(re.search(r"\d\s*[–—-]\s*\d", num))


def expand_numbering(num: str):
    """Expand a compressed numbering string into its individual members.
    'KE'-style ints: '1–6' -> 1..6, '3, 4, 6' -> [3,4,6]. 'PC'-style: '1.1–1.4' -> 1.1..1.4
    within the same major. Plain singles and FS skill-names pass through unchanged."""
    num = num.strip()
    if "," in num:
        return [m for part in num.split(",") for m in expand_numbering(part)]
    r = RANGE.match(num)
    if r:
        a, b = r.group(1), r.group(2)
        if "." in a and "." in b:
            amaj, amin = a.split("."); bmaj, bmin = b.split(".")
            if amaj == bmaj and amin.isdigit() and bmin.isdigit():
                return [f"{amaj}.{i}" for i in range(int(amin), int(bmin) + 1)]
            return [a, b]
        if a.isdigit() and b.isdigit():
            return [str(i) for i in range(int(a), int(b) + 1)]
        return [a, b]
    # numeric item with a trailing qualifier (e.g. '4.3 — partial') -> just the number;
    # a Foundation-skill name (no leading digit) passes through unchanged
    mnum = re.match(r"^(\d+(?:\.\d+)?)\b", num)
    return [mnum.group(1)] if mnum else [num]


def resolve_tags(line: str):
    """Yield (resolved 'UNIT SEC num', form) for each UoC item referenced on a line. Compressed
    range/list tags are expanded into one entry per member. Abbreviated tags (no unit) inherit the
    nearest preceding full tag's unit. form is one of: full | abbrev | compressed | unresolved."""
    current_unit = None
    for m in ANY_BRACKET.finditer(line):
        inside = m.group(1).strip()
        # compound multi-item tags join several references with a middle dot,
        # e.g. [ICTCLD401 KE 1 · ICTCLD502 KE 1]; resolve each part on its own
        for part in re.split(r"\s*·\s*", inside):
            part = part.strip()
            compound = part != inside
            mf = FULL.match(part)
            if mf:
                unit, sec, num = mf.group(1), mf.group(2), mf.group(3).strip()
                current_unit = unit
                form = "compressed" if (is_compressed(num) or compound) else "full"
                for member in expand_numbering(num):
                    yield (f"{unit} {sec} {member}", form)
                continue
            ma = ABBR.match(part)
            if ma:
                sec, num = ma.group(1), ma.group(2).strip()
                if not current_unit:
                    yield (f"?? {sec} {num}", "unresolved")
                    continue
                form = "compressed" if (is_compressed(num) or compound) else "abbrev"
                for member in expand_numbering(num):
                    yield (f"{current_unit} {sec} {member}", form)
            # other parts (placeholders, prose) are ignored


def criteria_table_tags(pre_benchmark: str) -> set:
    """Resolved UoC tags carried by the Assessment Criteria table — the tick-list the assessor
    actually marks against, which sits ABOVE the benchmark in the document.

    Everything before the benchmark heading is scanned: the criteria table is the only thing in that
    region that carries UoC tags. Returns an EMPTY set for instruments whose criteria and benchmark
    are one combined traceability table (S1-CL2 / S1-CL3), which is the caller's signal that there is
    no separate tick-list to check.
    """
    tags = set()
    for line in pre_benchmark.splitlines():
        for tag, form in resolve_tags(line):
            if form != "unresolved":
                tags.add(tag)
    return tags


ITEM_MARKER = re.compile(r"^(TASK|TEST|QUESTION)\s+(\d+)$", re.IGNORECASE)
EVIDENCES = re.compile(r"^Evidences:\s*(.+)$", re.IGNORECASE)


def instrument_evidence(pre_benchmark: str):
    """Where the WORK is: each run-sheet item -> the UoC tags its own `Evidences:` line claims.

    Run-sheet-style instruments state their traceability twice, independently: once per item (the
    `Evidences:` line under each task/test/question) and once per marking criterion (the benchmark).
    Nothing previously compared the two, so a criterion could claim an item that none of the work it
    covers actually evidences — a claim of coverage with no work behind it. See `orphan_claims`.

    Keys are ('task'|'test'|'question', n) plus ('section', '<heading>') for a titled block such as
    Handover. Returns {} for instruments that carry no per-item Evidences lines, which is the
    caller's signal that this convention is not in use and the check does not apply.
    """
    found, current, recent = {}, None, []
    for raw in pre_benchmark.splitlines():
        line = raw.strip()
        m = ITEM_MARKER.match(line)
        if m:
            current = (m.group(1).lower(), int(m.group(2)))
            continue
        ev = EVIDENCES.match(line)
        if ev:
            key = current
            if key is None or key in found:
                # An Evidences line with no fresh item marker belongs to a titled section
                # (Handover and the like). Such a block renders as a section heading followed by
                # its own title, so key it by BOTH recent headings and let a criterion match
                # either — keying by the nearest alone matches the title and misses the section.
                key = ("section", " | ".join(h.lower() for h in recent[:2]))
            tags = {t for t, form in resolve_tags(line) if form != "unresolved"}
            found.setdefault(key, set()).update(tags)
            current = None
            continue
        if line and "[" not in line and len(line) < 60:
            recent.insert(0, line)
            del recent[3:]
    return found


CRIT_TASKS = re.compile(r"tasks?\s+([0-9][0-9,\s\-–—]*(?:and\s+\d+)?)", re.IGNORECASE)
CRIT_TESTS = re.compile(r"\bT(\d+)\s*[-–—]\s*T(\d+)\b|\bT(\d+)\b")
CRIT_QS = re.compile(r"\bQ(\d+)\s*[-–—]\s*Q(\d+)\b|\bQ(\d+)\b")


def criterion_items(label: str, known: set):
    """Which run-sheet items a criterion says it covers, parsed from its own statement.

    Depends on the convention that a criterion names its scope ("A1 Network foundation (tasks 2-7)").
    Returns an empty set when it names none, which excludes that criterion from the orphan check
    rather than failing it.
    """
    out = set()
    for m in CRIT_TASKS.finditer(label):
        for part in re.split(r",|\band\b", m.group(1)):
            part = part.strip()
            rng = re.fullmatch(r"(\d+)\s*[-–—]\s*(\d+)", part)
            if rng:
                out |= {("task", i) for i in range(int(rng.group(1)), int(rng.group(2)) + 1)}
            elif part.isdigit():
                out.add(("task", int(part)))
    for m in CRIT_TESTS.finditer(label):
        a, b, single = m.groups()
        if a and b:
            out |= {("test", i) for i in range(int(a), int(b) + 1)}
        elif single:
            out.add(("test", int(single)))
    for m in CRIT_QS.finditer(label):
        a, b, single = m.groups()
        if a and b:
            out |= {("question", i) for i in range(int(a), int(b) + 1)}
        elif single:
            out.add(("question", int(single)))
    for kind, name in (k for k in known if k[0] == "section"):
        # A section key carries both the block heading and its title; either may be what the
        # criterion calls it.
        for part in (p.strip() for p in (name or "").split("|")):
            if part and re.search(rf"\b{re.escape(part)}\b", label, re.IGNORECASE):
                out.add((kind, name))
                break
    return out & known


TICKBOX = re.compile(r"[☐☒✓]")
CRITERION_ROW = re.compile(r"^([A-Z]{1,2}\d+)\s*[-–—]?\s*(\S.*)$")
CRIT_REF_LINE = re.compile(r"^([A-Z]{1,2}\d+(?:\s*[·,]\s*[A-Z]{1,2}\d+)*)\s*(?:\([^)]*\))?$")


def marking_criteria(text: str):
    """The marking-guide criteria table -> {criterion id: set of claimed tags}.

    A marking criterion is a row the assessor TICKS: an id and statement, its tag line, then a
    Yes/No tick box. The tick box is what separates a marking criterion from an assessment-condition
    row (the C-series), which carries tags but is never marked — counting those would fire the
    free-floating check on every instrument and get the check switched off.

    Criteria carrying NO tags are recorded with an empty set, deliberately: they are precisely what
    the free-floating check exists to find, so skipping them (as a tag-keyed parse must) makes that
    check vacuous. That is how it came to be inert on every run-sheet instrument.

    Handles both instrument formats — `A1 - statement` (narrative) and `A1 statement` (run sheet),
    with tags on the row itself or on the line below it.
    """
    out = {}
    lines = [ln.strip() for ln in text.splitlines()]
    for i, line in enumerate(lines):
        m = CRITERION_ROW.match(line)
        if not m:
            continue
        window = lines[i + 1:i + 4]
        if not any(TICKBOX.search(w) for w in window):
            continue                      # not a marked row — a condition, or prose
        tags = {t for t, form in resolve_tags(line) if form != "unresolved"}
        for w in window:
            if TICKBOX.search(w):
                break
            tags |= {t for t, form in resolve_tags(w) if form != "unresolved"}
        out[m.group(1)] = tags
    return out


def benchmark_criterion_refs(bench: str):
    """Criterion ids the benchmark points at — the reverse map's 'evidenced by' column.

    A reverse-map row renders the criterion id on its own line (`A6`, `A3 · A4`, `A9 (Q1)`).
    Returns an empty set for a narrative benchmark that names no criterion ids, which is the
    caller's signal to skip the guide-vs-benchmark comparison rather than report everything missing.
    """
    refs = set()
    for line in bench.splitlines():
        m = CRIT_REF_LINE.match(line.strip())
        if m:
            refs |= set(re.findall(r"[A-Z]{1,2}\d+", m.group(1)))
    return refs


GUIDE_CRIT = re.compile(r"^([A-Z]{1,2}\d+)\s+(\S.*)$")


def guide_criteria(text: str):
    """The marking-guide criteria table: criterion id -> (statement, claimed tags).

    A criterion renders as its statement line followed immediately by its tag line, e.g.

        A4 Database (tasks 14-15) — student creates the subnet group and deploys the database
        [ICTCLD401 PC 2.4] · [ICTCLD401 PC 2.5] · [ICTCLD401 PE 2]

    Deliberately separate from the benchmark parse in main(), which keys off a different
    criterion-id convention (`A1 — ...`) that this instrument family does not use.
    """
    out = {}
    lines = [ln.strip() for ln in text.splitlines()]
    for i, line in enumerate(lines):
        m = GUIDE_CRIT.match(line)
        if not m or "[" in line:
            continue
        for nxt in lines[i + 1:i + 3]:
            if not nxt:
                continue
            tags = {t for t, form in resolve_tags(nxt) if form != "unresolved"}
            # A tag line is (almost) nothing but tags — guards against a following prose line
            # that happens to quote one.
            if tags and len(ANY_BRACKET.sub("", nxt).strip(" ·—–-")) < 12:
                out.setdefault(m.group(1), (m.group(2), tags))
            break
    return out


def orphan_claims(criteria, evidence):
    """Criteria claiming a UoC item that none of the work they cover actually evidences.

    The gap this closes: an instrument states its traceability twice and independently — per
    run-sheet item (`Evidences:`) and per marking criterion — and nothing compared the two. A
    criterion could name a real item, on a real criterion, while none of the tasks it covers
    demonstrated anything of the kind. The phantom and free-floating checks both pass on that,
    because both only ask whether tags exist and resolve.

    Foundation skills are excluded: they are genuinely cross-cutting and are conventionally carried
    at criterion level rather than repeated on every item.
    """
    out = []
    for cid, (label, claimed) in sorted(criteria.items()):
        items = criterion_items(label, set(evidence))
        if not items:
            continue          # criterion names no run-sheet scope — not checkable, not a failure
        evidenced = set().union(*[evidence[k] for k in items])
        orphans = sorted(t for t in claimed - evidenced if " FS " not in f" {t} ")
        if orphans:
            out.append((cid, label, orphans, sorted(items)))
    return out


def split_benchmark(text: str):
    """Return (pre_benchmark_text, benchmark_text). The benchmark section starts at the FIRST
    heading-like line mentioning 'benchmark' or 'traceability', so a multi-part AT with more than one
    benchmark sub-section (e.g. a Part-A 'Design Benchmark' + a Part-B 'Report Benchmark') is captured
    whole — taking the last heading would drop every sub-section above it."""
    lines = text.splitlines()
    idx = None
    for i, ln in enumerate(lines):
        s = ln.strip()
        if BENCH_HEADING.search(s) and len(s) < 80 and "[" not in s:
            idx = i
            break
    if idx is None:
        return text, ""
    return "\n".join(lines[:idx]), "\n".join(lines[idx:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--at", required=True, type=Path, help="the AT .docx or .md")
    ap.add_argument("--consolidated", required=True, type=Path,
                    help="the cluster's consolidated_uoc.md (the valid-tag set)")
    ap.add_argument("--expect", action="append", default=[],
                    help="a UoC item the AT must evidence, e.g. 'BSBXTW401 PC 1.1' (repeatable)")
    args = ap.parse_args()

    text = load_text(args.at)
    valid = valid_tag_set(args.consolidated)
    pre, bench = split_benchmark(text)

    problems = []     # hard failures
    advisories = []   # warnings

    # ---- Parse the benchmark: criterion id -> resolved tags ----
    bench_criteria = {}   # id -> list[(tag, form)]
    covered = set()       # all resolved item tags across the AT (for reverse coverage)
    nonconforming = []    # tags not in individual full-ref form (abbreviated or compressed)
    invalid = []
    unresolved = []

    scan = bench if bench else text
    for line in scan.splitlines():
        m = CRIT_ID.match(line.strip())
        tags = list(resolve_tags(line))
        for tag, form in tags:
            if form == "unresolved":
                unresolved.append((line.strip()[:60], tag))
                continue
            covered.add(tag)
            if form != "full":
                nonconforming.append(tag)
            if tag not in valid:
                invalid.append(tag)
        if m:
            bench_criteria.setdefault(m.group(1), []).extend(tags)

    if not bench:
        problems.append("No 'Marking Benchmark / UoC traceability' section found — the AT has no "
                        "traceability table to validate. Add one (criterion -> UoC tags).")

    # ---- Hard check 1: phantom / invalid tags ----
    invalid = sorted(set(invalid))
    if invalid:
        problems.append(f"{len(invalid)} reference(s) not found in the consolidated UoC "
                        f"(phantom or mistyped):\n    " + "\n    ".join(invalid))
    if unresolved:
        problems.append(f"{len(unresolved)} abbreviated tag(s) with no preceding full tag to "
                        f"resolve the unit:\n    " + "\n    ".join(f"{t}  (in: {ln})" for ln, t in unresolved))

    # ---- Hard check 2: free-floating criteria (benchmark criterion with no tag) ----
    untagged = sorted(cid for cid, tags in bench_criteria.items()
                      if not any(f != "unresolved" for _, f in tags))
    if untagged:
        problems.append(f"{len(untagged)} benchmark criterion(s) with no UoC tag (free-floating): "
                        + ", ".join(untagged))

    # ---- Hard check 2b: free-floating MARKING criteria ----
    # Check 2 above reads whatever the benchmark parse recognised, which on a run-sheet instrument
    # is nothing and on a narrative one is the knowledge questions — never the marking criteria.
    # This reads the criteria table itself, so the check runs against the rows an assessor ticks.
    marking = marking_criteria(text)
    bench_refs = benchmark_criterion_refs(bench)
    untagged_marking = sorted(cid for cid, tags in marking.items() if not tags)
    if untagged_marking:
        problems.append(f"{len(untagged_marking)} marking criterion(s) with no UoC tag "
                        f"(free-floating — the assessor ticks it, but nothing says what it "
                        f"evidences): " + ", ".join(untagged_marking))
    if not marking:
        advisories.append("no marking criteria recognised in this instrument — the criteria-table "
                          "checks did not run. Reported rather than passed silently: a criterion "
                          "set that fails to parse makes every check keyed off it vacuous.")

    # ---- Advisory: the criteria table and the reverse map must agree, both ways ----
    if marking and bench_refs:
        orphan_crit = sorted(set(marking) - bench_refs)
        if orphan_crit:
            advisories.append(f"{len(orphan_crit)} marking criterion(s) not found in the benchmark "
                              f"reverse map — nothing claims to be evidenced by them: "
                              + ", ".join(orphan_crit))
        dangling = sorted(bench_refs - set(marking))
        if dangling:
            advisories.append(f"{len(dangling)} benchmark reference(s) to a criterion that is not in "
                              f"the criteria table (no such criterion to mark): " + ", ".join(dangling))

    # ---- Hard check 3: criteria claiming work that does not evidence them ----
    # The two checks above ask only whether tags EXIST and RESOLVE. This one asks whether the work a
    # criterion covers actually demonstrates what the criterion claims — by comparing the criterion's
    # tags against the `Evidences:` lines of the run-sheet items it names. Runs only where both
    # conventions are present; silently not applicable otherwise.
    evidence = instrument_evidence(pre)
    criteria = guide_criteria(text)
    orphans = orphan_claims(criteria, evidence) if evidence and criteria else []
    checkable = sum(1 for cid, (label, _) in criteria.items()
                    if criterion_items(label, set(evidence))) if evidence and criteria else 0
    if orphans:
        lines = []
        for cid, label, tags, items in orphans:
            scope = ", ".join(f"{k} {n}" for k, n in items)
            lines.append(f"{cid} ({label.split('—')[0].strip()}) claims "
                         + ", ".join(tags)
                         + f"\n        but nothing in {scope} evidences it")
        problems.append(
            f"{len(orphans)} criterion(s) claim a UoC item that none of the work they cover "
            f"evidences — the tag is real and the criterion is tagged, so this passes the checks "
            f"above while the claim has no work behind it:\n    " + "\n    ".join(lines))

    # ---- Advisory: tags not in individual full-ref form ----
    if nonconforming:
        uniq = sorted(set(nonconforming))
        advisories.append(f"{len(uniq)} reference(s) not in individual full-ref form (abbreviated, "
                          f"or a range/list — expanded and validated here, but the convention prefers "
                          f"one full [UNIT SEC num] per item):\n    " + "\n    ".join(uniq))

    # ---- Advisory: marking-guide criteria missing from the benchmark (best-effort) ----
    # Only meaningful when the benchmark uses an identifiable criterion-id scheme; restrict the
    # guide scan to the same letter prefix(es) so task labels (AT1) and conditions (C1) don't match.
    if bench and bench_criteria:
        bench_prefixes = {re.match(r"[A-Z]+", cid).group() for cid in bench_criteria}
        guide_ids = set()
        for line in pre.splitlines():
            m = CRIT_ID.match(line.strip())
            if m and re.match(r"[A-Z]+", m.group(1)).group() in bench_prefixes:
                guide_ids.add(m.group(1))
        missing = sorted(guide_ids - set(bench_criteria))
        if missing:
            advisories.append(f"{len(missing)} marking-guide criterion(s) not found in the benchmark "
                              f"(possible free-floating — verify): " + ", ".join(missing))

    # ---- Additive check: the Assessment Criteria table (the tick-list) ----
    # The checks above read the BENCHMARK. This reads the criteria table above it — the rows the
    # assessor ticks, which decide the student's result. Findings are advisory: nothing here changes
    # the verdict of the benchmark checks.
    crit_tags = criteria_table_tags(pre)
    if not crit_tags:
        criteria_note = ("no separate Assessment Criteria table carrying UoC tags — criteria and "
                         "benchmark are one combined table in this instrument; check not applicable")
    else:
        criteria_note = f"{len(crit_tags)} unique tag(s)"
        crit_phantom = sorted(t for t in crit_tags if t not in valid)
        if crit_phantom:
            advisories.append(
                f"{len(crit_phantom)} reference(s) in the ASSESSMENT CRITERIA TABLE not found in the "
                f"consolidated UoC (phantom or mistyped):\n    " + "\n    ".join(crit_phantom))
        only_criteria = sorted((crit_tags & valid) - covered)
        if only_criteria:
            advisories.append(
                f"{len(only_criteria)} item(s) tagged in the ASSESSMENT CRITERIA TABLE but absent from "
                f"the benchmark — the assessor marks them with no guidance on what satisfactory looks "
                f"like, and cluster coverage cannot see them:\n    " + "\n    ".join(only_criteria))
        only_benchmark = sorted((covered & valid) - crit_tags)
        if only_benchmark:
            advisories.append(
                f"{len(only_benchmark)} item(s) claimed in the BENCHMARK but absent from the assessment "
                f"criteria table — nothing on the tick-list marks them, so the claim of coverage has no "
                f"criterion behind it:\n    " + "\n    ".join(only_benchmark))

    # ---- Optional reverse coverage vs an expected allocation ----
    if args.expect:
        expected = {e.strip() for e in args.expect}
        uncovered = sorted(expected - covered)
        if uncovered:
            problems.append(f"{len(uncovered)} expected item(s) not evidenced by any criterion:\n    "
                            + "\n    ".join(uncovered))

    # ---- Report ----
    print(f"AT:           {args.at.name}")
    print(f"Consolidated: {args.consolidated}")
    print(f"Tags found:   {len(covered)} unique  |  benchmark criteria: {len(bench_criteria)}  |  "
          f"marking criteria: {len(marking)}")
    print(f"Criteria tbl: {criteria_note}")
    if evidence and criteria:
        print(f"Work check:   {len(evidence)} run-sheet item(s) with an Evidences line  |  "
              f"{checkable}/{len(criteria)} criteria name a scope and were cross-checked")
    else:
        print("Work check:   not applicable — this instrument does not carry both per-item "
              "'Evidences:' lines and criteria that name their scope")
    if args.expect:
        print(f"Expected:     {len(args.expect)} item(s) to cover")
    print()
    for a in advisories:
        print(f"ADVISORY: {a}\n")
    if problems:
        for p in problems:
            print(f"FAIL: {p}\n")
        print("RESULT: FAIL")
        sys.exit(1)
    print("RESULT: PASS — every criterion is tagged and every reference is a real UoC item"
          + (" with expected coverage met." if args.expect else "."))
    sys.exit(0)


if __name__ == "__main__":
    main()
