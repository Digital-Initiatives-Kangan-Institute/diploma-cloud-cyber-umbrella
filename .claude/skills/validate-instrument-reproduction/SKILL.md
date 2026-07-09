---
name: validate-instrument-reproduction
version: 1.0.0
updated: 2026-07-09
model: claude-haiku-4-5-20251001
description: >-
  This skill should be used whenever a regenerated document must be proven to reproduce a committed one —
  e.g. "does the regenerated instrument match the committed docx", "check the generator reproduces the
  authored version", "prove the retrofit is faithful", or when retro-fitting a generator to a
  hand-authored .docx / regenerating an instrument and confirming nothing changed. It runs a
  deterministic check (the bundled validate_instrument_reproduction.py): both .docx are extracted to body
  text in document order (paragraphs + table cells), normalised (whitespace collapsed, blank lines
  dropped), and diffed — PASS only when content + order are identical. A `--sub OLD::NEW` rule rewrites
  the reference before diffing to absorb a DELIBERATE change (e.g. a URL edit), so the check still proves
  "identical except the intended change". Byte/XML identity is not required (python-docx vs Word differ);
  the bar is content equivalence.
---

# Validate instrument reproduction (regenerated == committed)

When a generator is retro-fitted to a hand-authored assessment instrument — or an instrument is
regenerated after an edit — this skill proves the regenerated `.docx` **reproduces** the committed one at
the content level, so the generated version can safely become canonical. It is the gate that made the
CL1 instrument retrofit trustworthy (2026-07-09): each generated instrument was proven identical to the
committed doc except a deliberate URL removal.

## When to use

- Retro-fitting a generator to a hand-authored `.docx` (prove the generator is faithful before adopting).
- Regenerating an instrument after editing its builder (prove only the intended change landed).
- Any "does the rebuilt document still match?" check between two `.docx`.

## How it compares

Both documents' **body text** is extracted in document order (paragraphs + table cells) via the pack's
`docx_to_text`, normalised (runs of whitespace → one space, per-line strip, blank lines dropped), and
diffed. **PASS = identical content + order.** Byte/XML identity is *not* the bar — python-docx and Word
author different markup for the same content, so only the readable content is compared (headers/footers
come from the shared template, not the filled content).

**Absorbing a deliberate change:** `--sub OLD::NEW` rewrites `OLD`→`NEW` in the **reference** before
diffing (applied after normalisation, so a plain-space rule matches a non-breaking space in the source).
Use it so an intended edit is not counted as a difference — e.g. proving a now-evergreen instrument is
identical to the committed one *except* the removed URL clause:

```bash
python .claude/skills/scripts/validate_instrument_reproduction.py \
  --candidate <regenerated.docx> --reference <committed.docx> \
  --sub ' (https://www.placeholder.com.au)::' --sub ' at https://www.placeholder.com.au::'
```

Keep `--sub` rules **minimal and auditable** — each should strip only the intended text (e.g. a URL and
its immediate wrapper, `NEW` empty). If a PASS needs a `--sub` that rewrites *substantive* content, that
is a reproduction failure to fix in the generator, not to paper over.

## How to run it

> **Python:** any Python 3 launcher (`python` / `python3` / `py -3`) — it only needs the text extractor.

```bash
python .claude/skills/scripts/validate_instrument_reproduction.py --candidate <regen.docx> --reference <committed.docx> [--sub 'OLD::NEW' ...]
```

Exit `0` = PASS (reproduces), `1` = FAIL (content differs — the first differences print as
`- committed` / `+ regenerated`), `2` = usage/error.

## Interpreting the result

Goal: `RESULT: PASS`. On FAIL it reports a similarity ratio and the differing lines. Fix the generator's
content data until the only remaining differences are ones you deliberately absorb with an auditable
`--sub`. For adopting a retrofit, additionally diff the regenerated in-place file against the **git-HEAD**
original (`git show HEAD:<path> > /tmp/orig.docx`) so the reference is the pristine committed version.

## Portability

Self-contained + stdlib-only (`validate_instrument_reproduction.py` in `.claude/skills/scripts/`, reusing
the pack's `docx_to_text`). Works on any two `.docx`, any course.
