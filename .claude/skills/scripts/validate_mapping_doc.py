#!/usr/bin/env python3
"""Validate an Assessment Mapping docx against its unit's UoC and the AT marking benchmarks.

The mapping doc (`<cluster>/mappings/<UNIT>_Assessment_Mapping.docx`) is a DERIVED artefact: its
rows are the unit's UoC items (PC/PE/KE/FS/AC) and its AT columns carry the criterion code(s) that
evidence each item. Because it is auto-generated, the only ways it goes wrong are (a) it drifts from
the unit's UoC — an item dropped or left unmapped — or (b) it drifts from the benchmarks it was
inverted from (a stale docx or a hand-edit). This validator catches both:

  COMPLETENESS (primary, hard — source of truth: the unit's own UoC transcription)
    Every assessable item in `units_of_competency/<UNIT>_Complete_*.md` appears as a row in the
    mapping doc AND is mapped to at least one AT. Reports:
      * MISSING  — a UoC item with no row (or a section row-count shortfall).
      * BLANK    — a row present but mapped to no AT (an unassessed requirement).
      * PHANTOM  — a mapping row that is not a UoC item (extra/stale rows).
    The source UoC is parsed here independently (NOT via the generator) so a generator bug cannot
    hide from its own check.

  ACCURACY (secondary — source of truth: the AT assessor benchmarks)
    Each row's AT-column codes are compared against the cluster's canonical benchmark inversion
    (`invert_benchmarks()` for the CL2/CL3-style generators; the hand-authored `DATA_*` for CL1).
    This is a drift check: is the on-disk docx still in sync with the benchmarks? PC/PE/KE are HARD
    (a mismatch fails); FS/AC are ADVISORY (their codes are closest-fit judgement mapped via the
    generator's FS_MAP/AC_MAP, not benchmark-derived, so a difference is reported, not failed).

The docx is read with stdlib only (the same word/document.xml walk the other validators use), so the
completeness check has no third-party dependency. The accuracy oracle imports the cluster's mapping
build module (which pulls python-docx); it is loaded lazily, so completeness runs even without it.

Usage:
  validate_mapping_doc.py --mapping <UNIT>_Assessment_Mapping.docx [--uoc <UNIT>_Complete.md]
  validate_mapping_doc.py --cluster <S1-CLx dir>      # all mappings/*_Assessment_Mapping.docx
      [--no-accuracy]                                  # completeness only
      [--require-accuracy]                             # fail (don't skip) if the oracle is missing

Exit 0 = PASS (complete; PC/PE/KE accurate where the oracle is available).
"""
import argparse
import importlib.util
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# --- shared mapping-template layout (the institutional "Assessment Mapping Tool.docx") ----------
# Tables are addressed in document order; the same template is used across all clusters, so a
# 2-AT cluster simply leaves the AT3 column blank.
TABLE = {"AC": 3, "PC": 4, "PE": 5, "KE": 6, "FS": 7}
HEADER_ROWS = 2                       # row 0 = section title, row 1 = column headers
ITEM_COL = {"AC": 0, "PC": 1, "PE": 0, "KE": 0, "FS": 0}
AT_COLS = {"AC": (1, 2, 3), "PC": (2, 3, 4), "PE": (1, 2, 3), "KE": (1, 2, 3), "FS": (3, 4, 5)}
SECTIONS = ("PC", "PE", "KE", "FS", "AC")
HARD = ("PC", "PE", "KE")             # accuracy-hard sections (FS/AC are advisory)


# ============================================================================
# stdlib docx table reader  ->  tables[i] = list of rows; row = list of cell strings
# ============================================================================

def _cell_text(tc):
    paras = []
    for p in tc.findall(f"{W}p"):
        parts = []
        for n in p.iter():
            if n.tag == f"{W}t":
                parts.append(n.text or "")
            elif n.tag == f"{W}br":
                parts.append("\n")
        paras.append("".join(parts))
    return "\n".join(paras)


def read_tables(docx_path: Path):
    with zipfile.ZipFile(docx_path) as z:
        tree = ET.parse(z.open("word/document.xml"))
    body = tree.getroot().find(f"{W}body")
    tables = []
    for tbl in body.iter(f"{W}tbl"):
        rows = [[_cell_text(tc) for tc in tr.findall(f"{W}tc")] for tr in tbl.findall(f"{W}tr")]
        tables.append(rows)
    return tables


def read_mapping(docx_path: Path):
    """{section: [(item_label, (at1, at2, at3)), ...]} from the mapping doc data rows."""
    tables = read_tables(docx_path)
    out = {}
    for sec in SECTIONS:
        rows = tables[TABLE[sec]][HEADER_ROWS:]
        ic, acols = ITEM_COL[sec], AT_COLS[sec]
        recs = []
        for r in rows:
            label = r[ic].strip() if ic < len(r) else ""
            codes = tuple((r[c].strip() if c < len(r) else "") for c in acols)
            recs.append((label, codes))
        out[sec] = recs
    return out


# ============================================================================
# Independent source-UoC parser (units_of_competency/<UNIT>_Complete_*.md)
# ============================================================================

def _sections_md(text):
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^#\s+(.*)", line)
        if m:
            if cur is not None:
                out.setdefault(cur, "\n".join(buf))
            cur, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    if cur is not None:
        out.setdefault(cur, "\n".join(buf))
    return out


def _bullets(body):
    raw = body.splitlines()
    top = [ln for ln in raw if re.match(r"^- ", ln)]
    # Parent-bullet special case (e.g. ICTICT517 PE "For one organisation:" + 6 sub-bullets):
    # a single top-level bullet ending ':' means its sub-bullets are the assessable items.
    if len(top) == 1 and top[0].rstrip().endswith(":"):
        return [re.sub(r"^\s*-\s+", "", ln).strip() for ln in raw if re.match(r"^\s+- ", ln)]
    items = []
    for ln in raw:
        s = ln.strip()
        if not s.startswith("- "):
            continue
        text = re.sub(r"^-\s+", "", s).strip()
        if (len(ln) - len(ln.lstrip())) > 0 and items:
            items[-1] += "\n  - " + text
        else:
            items.append(text)
    return items


def parse_source_uoc(md_path: Path):
    """{'PC': [(num, text)], 'PE'/'KE': [text], 'FS': [(skill, desc)], 'AC': [text]} in source order."""
    secs = _sections_md(md_path.read_text(encoding="utf-8"))

    pcs = []
    for ln in secs.get("Elements and Performance Criteria", "").splitlines():
        if not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        elem, pc_cell = cells[0], cells[1]
        if elem.upper().startswith("ELEMENTS") or elem.startswith("Elements describe"):
            continue
        if not re.match(r"^\d+\.", elem):
            continue
        for piece in pc_cell.split("<br>"):
            m = re.match(r"^(\d+\.\d+)\s+(.*)", piece.strip())
            if m:
                pcs.append((m.group(1), m.group(2).strip()))

    fss = []
    for ln in secs.get("Foundation Skills", "").splitlines():
        if not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        skill, desc = cells[0], cells[1]
        if skill.upper() == "SKILL" or not skill or skill.startswith("---"):
            continue
        fss.append((skill, desc.replace("<br>", " ")))

    acsec = secs.get("Assessment Conditions", "")
    acs = _bullets(acsec)
    for ln in acsec.splitlines():
        if ln.strip().lower().startswith("assessors of this unit must satisfy"):
            acs.append(ln.strip())

    return {
        "PC": pcs,
        "PE": _bullets(secs.get("Performance Evidence", "")),
        "KE": _bullets(secs.get("Knowledge Evidence", "")),
        "FS": fss,
        "AC": acs,
    }


# ============================================================================
# Completeness
# ============================================================================

def _mapped(codes):
    return any(c for c in codes)


def check_completeness(source, mapping):
    """Return list of (severity, section, detail) issues. severity in {'FAIL','WARN'}."""
    issues = []
    for sec in SECTIONS:
        src = source[sec]
        rows = mapping[sec]
        n_src, n_doc = len(src), len(rows)

        # Identity-matched sections: PC by number, FS by skill name.
        if sec == "PC":
            doc_nums = {re.match(r"^(\d+\.\d+)", lbl).group(1)
                        for lbl, _ in rows if re.match(r"^(\d+\.\d+)", lbl)}
            for num, _txt in src:
                if num not in doc_nums:
                    issues.append(("FAIL", sec, f"MISSING — PC {num} has no row in the mapping doc"))
            src_nums = {num for num, _ in src}
            for lbl, _ in rows:
                m = re.match(r"^(\d+\.\d+)", lbl)
                if m and m.group(1) not in src_nums:
                    issues.append(("FAIL", sec, f"PHANTOM — mapping row PC {m.group(1)} is not a UoC item"))
        elif sec == "FS":
            doc_skills = {lbl for lbl, _ in rows if lbl}
            src_skills = {s for s, _ in src}
            for skill, _ in src:
                if skill not in doc_skills:
                    issues.append(("FAIL", sec, f"MISSING — FS '{skill}' has no row"))
            for lbl, _ in rows:
                if lbl and lbl not in src_skills:
                    issues.append(("FAIL", sec, f"PHANTOM — mapping row FS '{lbl}' is not a UoC item"))
        else:
            # Positional sections (PE/KE/AC): row count must match source item count.
            if n_doc != n_src:
                issues.append(("FAIL", sec,
                               f"ROW COUNT — UoC has {n_src} {sec} item(s), mapping doc has {n_doc}"))

        # Every present row must be mapped to >=1 AT (applies to all sections).
        for i, (lbl, codes) in enumerate(rows, 1):
            if lbl and not _mapped(codes):
                tag = lbl if sec in ("PC", "FS") else f"#{i}"
                issues.append(("FAIL", sec, f"BLANK — {sec} {tag} is in the doc but mapped to no AT"))
    return issues


# ============================================================================
# Accuracy oracle  ->  {(section, item_key): {'AT1': set, 'AT2': set, 'AT3': set}}
# ============================================================================

def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = mod
    # the build module sits in scripts/s1_clN/ and imports its sibling assessor modules
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(mod)
    return mod


def _norm(codes):
    if isinstance(codes, str):
        codes = [codes]
    out = set()
    for c in codes:
        for part in str(c).split(","):
            part = part.strip()
            if part:
                out.add(part)
    return out


def build_oracle(cluster_dir: Path, unit_code: str):
    """Expected codes per item for `unit_code`. Returns (oracle|None, note)."""
    m = re.search(r"S1-CL(\d+)", cluster_dir.name)
    if not m:
        return None, f"cannot infer cluster number from '{cluster_dir.name}'"
    n = m.group(1)
    build = cluster_dir.parent / "scripts" / f"s1_cl{n}" / f"build_s1_cl{n}_mapping_docs.py"
    if not build.exists():
        return None, f"no mapping build module at {build}"
    mod = _load_module(build)

    oracle = {}

    def put(sec, item, at_label, codes):
        oracle.setdefault((sec, str(item)), {"AT1": set(), "AT2": set(), "AT3": set()})
        oracle[(sec, str(item))][at_label] |= _norm(codes)

    if hasattr(mod, "invert_benchmarks"):  # CL2/CL3-style: criterion -> UoC inversion
        inv = mod.invert_benchmarks()
        for (u, sec, item), val in inv.items():
            if u != unit_code:
                continue
            if isinstance(val, dict):       # CL3-style: already split by AT
                for at_label in ("AT1", "AT2", "AT3"):
                    if val.get(at_label):
                        put(sec, item, at_label, val[at_label])
            else:                            # CL2-style: flat list -> split by the module's own rule
                if hasattr(mod, "_split_codes"):
                    at1, at2 = mod._split_codes(val)
                else:
                    at1, at2 = ", ".join(val), ""
                put(sec, item, "AT1", at1)
                put(sec, item, "AT2", at2)
        return oracle, "invert_benchmarks()"

    # CL1-style: hand-authored DATA_* dicts (no benchmark to invert).
    data = None
    for attr in dir(mod):
        if attr.startswith("DATA_") and isinstance(getattr(mod, attr), dict):
            d = getattr(mod, attr)
            # match the unit by the docx filename recorded in UNIT_DATA
            for key, (fname, dd) in getattr(mod, "UNIT_DATA", {}).items():
                if dd is d and unit_code in fname:
                    data = d
                    break
        if data is not None:
            break
    if data is None:
        return None, f"{build.name} exposes neither invert_benchmarks() nor a DATA_* for {unit_code}"

    for num, ats in data.get("pcs", {}).items():
        for at in ("AT1", "AT2", "AT3"):
            if ats.get(at):
                put("PC", num, at, ats[at])
    for sec, keys in (("PE", ("pes", "pes_split")), ("KE", ("kes",))):
        entries = next((data[k] for k in keys if data.get(k)), [])
        for i, entry in enumerate(entries, 1):
            ats = entry[1] if isinstance(entry, tuple) else entry  # pes_split is (label, {AT})
            for at in ("AT1", "AT2", "AT3"):
                if ats.get(at):
                    put(sec, i, at, ats[at])
    for skill, ats in data.get("fss", {}).items():
        for at in ("AT1", "AT2", "AT3"):
            if ats.get(at):
                put("FS", skill, at, ats[at])
    for i, (_label, ats) in enumerate(data.get("acs", []), 1):
        for at in ("AT1", "AT2", "AT3"):
            if ats.get(at):
                put("AC", i, at, ats[at])
    return oracle, "DATA_* (hand-authored)"


def _item_key(sec, i, label):
    if sec == "PC":
        m = re.match(r"^(\d+\.\d+)", label)
        return m.group(1) if m else None
    if sec == "FS":
        return label or None
    return str(i)  # PE/KE/AC positional


def check_accuracy(mapping, oracle):
    """Return (hard_fails, advisories) lists of (section, detail)."""
    hard_fails, advisories = [], []
    for sec in SECTIONS:
        for i, (label, codes) in enumerate(mapping[sec], 1):
            if not (label or any(codes)):
                continue
            key = _item_key(sec, i, label)
            exp = oracle.get((sec, str(key)), {"AT1": set(), "AT2": set(), "AT3": set()})
            got = {"AT1": _norm(codes[0]), "AT2": _norm(codes[1]), "AT3": _norm(codes[2])}
            for at in ("AT1", "AT2", "AT3"):
                if got[at] == exp[at]:
                    continue
                missing = exp[at] - got[at]
                extra = got[at] - exp[at]
                tag = key if sec in ("PC", "FS") else f"#{i}"
                detail = (f"{sec} {tag} {at}: doc={sorted(got[at]) or '—'} "
                          f"benchmark={sorted(exp[at]) or '—'}"
                          + (f"  missing {sorted(missing)}" if missing else "")
                          + (f"  extra {sorted(extra)}" if extra else ""))
                if sec in HARD:
                    hard_fails.append((sec, detail))
                else:
                    # closest-fit (benchmark silent) is expected; a conflict (benchmark has a
                    # code AND the doc differs) is the advisory worth a human's eyes.
                    kind = "conflict" if exp[at] else "closest_fit"
                    advisories.append((kind, detail))
    return hard_fails, advisories


# ============================================================================
# Driver
# ============================================================================

def find_uoc(cluster_dir: Path, unit_code: str):
    hits = sorted((cluster_dir / "units_of_competency").glob(f"{unit_code}_Complete_*.md"))
    return hits[0] if hits else None


def validate_one(mapping_path: Path, uoc_path, do_accuracy, require_accuracy):
    unit_code = mapping_path.name.split("_Assessment_Mapping")[0]
    cluster_dir = mapping_path.parent.parent
    if uoc_path is None:
        uoc_path = find_uoc(cluster_dir, unit_code)

    print(f"\n=== {unit_code}  ({mapping_path.name}) ===")
    failed = False

    mapping = read_mapping(mapping_path)
    if uoc_path is None or not Path(uoc_path).exists():
        print("  COMPLETENESS: SKIPPED — no source UoC found "
              f"(units_of_competency/{unit_code}_Complete_*.md)")
    else:
        source = parse_source_uoc(Path(uoc_path))
        issues = check_completeness(source, mapping)
        counts = " ".join(f"{s}={len(source[s])}" for s in SECTIONS)
        if not issues:
            print(f"  COMPLETENESS: PASS — every UoC item present and mapped ({counts})")
        else:
            failed = True
            print(f"  COMPLETENESS: FAIL — {len(issues)} issue(s) ({counts})")
            for sev, sec, detail in issues:
                print(f"    [{sev}] {detail}")

    if do_accuracy:
        oracle, note = build_oracle(cluster_dir, unit_code)
        if oracle is None:
            msg = f"  ACCURACY: {'FAIL' if require_accuracy else 'SKIPPED'} — {note}"
            print(msg)
            if require_accuracy:
                failed = True
        else:
            hard, adv = check_accuracy(mapping, oracle)
            if not hard:
                print(f"  ACCURACY: PASS — PC/PE/KE codes match the benchmarks [oracle: {note}]")
            else:
                failed = True
                print(f"  ACCURACY: FAIL — {len(hard)} PC/PE/KE mismatch(es) [oracle: {note}]")
                for sec, detail in hard:
                    print(f"    [FAIL] {detail}")
            conflicts = [d for k, d in adv if k == "conflict"]
            closest = [d for k, d in adv if k == "closest_fit"]
            if closest:
                print(f"  ACCURACY (advisory): {len(closest)} FS/AC closest-fit cell(s) "
                      "— not benchmark-traceable, review by hand")
            if conflicts:
                print(f"  ACCURACY (advisory): {len(conflicts)} FS/AC conflict(s) "
                      "— benchmark tags this item but the doc differs:")
                for detail in conflicts:
                    print(f"    [info] {detail}")
    return not failed


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # AC tick (✓) + em-dashes survive a cp1252 console
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description="Validate Assessment Mapping docx vs UoC + benchmarks.")
    ap.add_argument("--mapping", type=Path, help="a single <UNIT>_Assessment_Mapping.docx")
    ap.add_argument("--uoc", type=Path, help="the unit's <UNIT>_Complete_*.md (auto-found if omitted)")
    ap.add_argument("--cluster", type=Path, help="an S1-CLx dir; validate all its mapping docs")
    ap.add_argument("--no-accuracy", action="store_true", help="completeness only")
    ap.add_argument("--require-accuracy", action="store_true", help="fail if the oracle is unavailable")
    args = ap.parse_args()

    if args.cluster:
        targets = sorted((args.cluster / "mappings").glob("*_Assessment_Mapping.docx"))
        if not targets:
            print(f"No mapping docs under {args.cluster / 'mappings'}")
            sys.exit(2)
    elif args.mapping:
        targets = [args.mapping]
    else:
        ap.error("give --mapping <docx> or --cluster <dir>")

    ok = True
    for t in targets:
        ok &= validate_one(t, args.uoc if args.mapping else None,
                           not args.no_accuracy, args.require_accuracy)
    print()
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
