---
name: umbrella-engine-architecture
description: The course-agnostic authoring engine (deck/doc/mapping + validators) lives in the UMBRELLA scripts/ + .claude/skills/; each course supplies its own brand.py + mapping_registry.py + generators in its content repo. How the split works + how to invoke.
metadata: 
  node_type: memory
  type: project
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
---

**The shared authoring engine is course-agnostic and lives in the UMBRELLA** (2026-07-08 restructure).
This is the reproducible machinery — the same for any course/semester plugged in; only the sub-repo data
differs. Where things live now:

- **Umbrella `.claude/skills/`** — all the process skills + validators (`validate-*`, `consolidate-uocs`,
  `generate-consolidated-plan`, `setup-cluster-spec`, `transcribe-uoc`, `inspect-file-size`) +
  `.claude/skills/scripts/` (the validator engines) + `draw-diagram`/`image-gen` + **`review-slides`**
  (render a `.pptx` → per-slide PNGs via LibreOffice + PyMuPDF for visual QA; own venv; LibreOffice is a
  system dep — `brew install --cask libreoffice`).
- **Umbrella `scripts/`** — the **deck/doc/mapping engine**: `build_topic_deck.py`, `helpers/`
  (brand-agnostic docx/pptx + `scenario_document`), `mapping/generate_mapping_doc.py`, `tests/` (self-test
  via a neutral `tests/_fixtures/brand.py` + `conftest.py`), `requirements.txt`. Run with the umbrella's
  `scripts/.venv` (python-docx/pptx).
- **Content repo `scripts/`** — the **course specifics**: `brand.py` (palette + org identity:
  `ORG_NAME`/`ORG_WORDMARK`/`ADDRESS`/`DISCLOSURE`), `mapping_registry.py` (`CLUSTERS` + `QUALIFICATION` +
  `UNIT_PREFIXES`), and the semester generators (`s1_cl*/`, `scenario/`, `templates/`). `kangan-templates/`
  (institutional docx templates) also stays in the content repo (referenced content-repo-relative). Plus
  `tests/test_yat_brand.py` (tests THIS course's brand pack).

**How the engine finds the course's data (the two seams):**
- **Brand** — the engine's helpers `from brand import …`; `build_topic_deck` walks up from the slide-plan
  path to the content repo's `scripts/brand.py` (`--brand <path>` override). Generators put their
  content-repo `scripts/` (parents[1]) + the umbrella `scripts/` (walk up for `scripts/helpers/__init__.py`)
  on `sys.path`.
- **Mapping registry** — `generate_mapping_doc.py --registry <content-repo>/scripts/`; `REPO` is derived
  from the registry's own location, so the engine runs from the umbrella against any content repo.

**Invoking (from the umbrella root):**
- Deck: `scripts/.venv/bin/python scripts/build_topic_deck.py <content-repo>/…/topic_NN/slide_plan.md [out] [--allow-gen]`
- Mapping: `scripts/.venv/bin/python scripts/mapping/generate_mapping_doc.py --check|--build all --registry <content-repo>/scripts/`
- Generators (content-repo scripts): run with the **umbrella** `scripts/.venv/bin/python`.

**Deck-engine capabilities (added 2026-07-08/09; in `kangan_deck.py` + `deck_images.py`, so every deck
build — generic builder AND the CL1 per-topic scripts — gets them):** `deck_images.resolve_image` PLACES a
committed `reuse <file>` from `topic_NN/images/` (deck = pure function of committed source; a rebuild
repopulates); body text **auto-fits + vertical-centres** (bounded tiers {18–24}); `[TABLE]`-with-no-columns
degrades to a content slide (no crash); **teacher speaker notes** via `notes=` on content/visual/activity/
demo layouts + `register_notes({title: notes})` → the notes pane. See [[delivery-run-sheet]] for the Step-4
pipeline that uses these + docs/slide-plan-format.md for the authoring contract.

**Retest proven (2026-07-08):** 35 engine tests pass (fixture brand); `mapping --check all` reproduces
every committed docx; deck build works — all from the new layout. Related: [[mapping-pipeline]],
[[delivery-run-sheet]], [[assessment-run-sheet]].
