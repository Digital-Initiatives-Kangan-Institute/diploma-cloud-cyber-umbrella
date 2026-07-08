---
name: review-slides
version: 1.0.0
description: |
  Render a built teaching deck (.pptx) to one image per slide and visually review it — catch leftover
  image-placeholder boxes, text overflow/clipping, image/text overlap, broken or empty layouts, garbled
  AI-generated images, and off-brand or wrong-looking slides. LibreOffice renders the .pptx exactly as
  PowerPoint would (headless); PyMuPDF rasterises each page. Deterministic + re-runnable: rebuild a deck,
  re-run this, and re-review. Use after building/regenerating any deck, or as a pre-commit sensibility check.
allowed-tools:
  - Bash
  - Read
---

# review-slides

Turn a `.pptx` into per-slide PNGs and **look at every slide**. The rendering is deterministic tooling;
the *review* is the visual judgement you (the model) apply to the images.

## Dependencies

- **LibreOffice** — a **system app**, not a pip package. It converts `.pptx` → PDF headless, faithful to
  PowerPoint's own layout. macOS: `brew install --cask libreoffice`. Detected on PATH (`soffice` /
  `libreoffice`) or the standard macOS app path. `render_deck.py` prints the install hint if it's absent.
- **PyMuPDF** — the venv dependency (`requirements.txt`). Per the skill-dependencies convention
  (`docs/skill-dependencies.md`): committed `requirements.txt` + a per-skill **gitignored `.venv/`** +
  import guard + invoke with the venv's Python.

**One-time setup** (from the umbrella root):

```bash
python3 -m venv .claude/skills/review-slides/.venv
.claude/skills/review-slides/.venv/bin/python -m pip install -r .claude/skills/review-slides/requirements.txt
```

## How to run

1. **Render** the deck to PNGs (from the umbrella root):

   ```bash
   .claude/skills/review-slides/.venv/bin/python .claude/skills/review-slides/render_deck.py \
     --deck <path/to/Topic_NN_Slides.pptx> \
     --out  <scratchpad>/review/topic_NN
   ```

   Writes `slide-001.png`, `slide-002.png`, … Prints `RESULT {"slides": N, "out": …}`. `--dpi` (default
   110) trades sharpness for size; a `.pdf` can be passed instead of a `.pptx` (skips LibreOffice).
   Put `--out` in the scratchpad — the PNGs are a disposable review artefact, not a committed one.

2. **Review** — `Read` each `slide-NNN.png` and check for:
   - **Leftover image placeholders** — a dashed box with 🖼 / "IMAGE" / a description (an unfilled slot).
   - **Text overflow / clipping** — text running off the slide or out of its box; titles truncated.
   - **Image ↔ text overlap** — a picture sitting on top of bullets, or vice-versa.
   - **Broken / empty layouts** — a blank content area, a table with no rows, a missing hero image.
   - **Garbled AI-gen images** — nonsense text, malformed hands/objects, obvious artefacts.
   - **Off-brand / wrong content** — wrong colours, a stray reconstruction artefact, duplicated text.

3. **Report** per slide: `slide N — <title>: <issue>` (or "clean"). Group by deck when reviewing several.

## Re-run

Rebuild the deck, re-run step 1 (same command) — the PNGs refresh. Nothing to clean up; the temp
LibreOffice profile + PDF are removed automatically each run.

## Notes

- **Deterministic** — same deck → same PNGs (LibreOffice layout + PyMuPDF raster; no model in the render).
- **Headless** — no LibreOffice window; a private user-profile dir per run avoids the "already running" lock.
- **Batch** — loop the render over several decks into per-deck `--out` folders, then review each set.
- **What it can't do** — it renders what's *in* the file; it won't tell you a slide is pedagogically weak,
  only that it's visually broken/placeholder/garbled. Pedagogical quality stays a human read.
