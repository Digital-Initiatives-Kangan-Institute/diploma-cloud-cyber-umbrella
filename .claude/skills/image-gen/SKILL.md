---
name: image-gen
version: 1.0.0
description: |
  Deterministic image-generation engine. A no-LLM mechanical wrapper that calls an
  OpenRouter image model with a fully-resolved prompt + reference image(s) + a model
  name, and saves candidate images to a review folder for human curation. The model
  is a parameter (multi-model bake-off, or a per-series / per-image choice). This is
  the BASE UNIT the use-case image skills (character reference, cover, page art)
  compose on top of — it does NO prompt composition and holds NO IP knowledge. Use
  it directly when you already have a resolved prompt + refs and just need images.
allowed-tools:
  - Bash
---

# image-gen

The **deterministic engine** at the bottom of the image pipeline. Give it a
finished prompt, zero or more reference images, and a model; it returns saved
candidate images. Everything *above* it — composing the prompt from the visual
style + character bible, choosing references, picking the model — belongs to the
use-case skills that call this one.

> **"No LLM in the loop"** describes the *orchestration*: the same arguments build
> the same API request, with no model deciding anything. The image *output* is of
> course non-deterministic — that is the image model, not this script.

## How to run

From the **umbrella root**:

```bash
python .claude/skills/image-gen/generate.py \
  --model google/gemini-3-pro-image-preview \
  --prompt "flat 2D vector cartoon, bold outlines, flat colours ..." \
  --ref ip-contractor-cody/foundation/reference-art/darren_the_digger.png \
  --n 1 \
  --out ip-contractor-cody/foundation/style-lock/_candidates
```

`--ref` is repeatable → a `refs[]` array (multiple angles, or character + a style
reference). The model uses references to preserve identity while the prompt directs
the style.

## Parameters

| Flag | Required | Meaning |
|---|---|---|
| `--model` | yes | OpenRouter model slug (e.g. `google/gemini-3-pro-image-preview`, a FLUX.2, Seedream, GPT-Image slug) |
| `--prompt` | yes | the fully-resolved generation prompt (this engine does not compose it) |
| `--ref` | no, repeatable | reference image path; pass several for multi-reference consistency |
| `--n` | no (1) | number of candidates to generate |
| `--out` | yes | folder to save into; created if absent |
| `--name` | no | output filename stem (e.g. `bella` → `bella.png`; extras → `bella_2.png`); omit to name files by the model slug (handy for a bake-off into one folder) |

## Output

- Saves `<name>.<ext>` (extra images from one call → `<name>_2.<ext>`…) when `--name` is given; otherwise `<model-slug>.<ext>`. Into `--out`.
- Prints a final machine-readable line for callers to parse:
  `RESULT {"model": ..., "count": N, "saved": [paths], "ok": true|false}`.
- Exit code `0` if any image was saved, else non-zero.

## Where it sits (the layering)

```
use-case skills   character-ref │ cover │ page-art   ← own/receive the SUBJECT brief
                            ╲       │     ╱
prompt assembly   compose(subject_brief + style_spec + character_refs)  ← shared, deterministic
                                  │
ENGINE (this)     generate.py:  prompt + refs[] + model → images        ← base unit
```

## Notes

- **Key.** Reads `OPENROUTER_API_KEY` from the environment or the repo-root `.env`
  (git-crypt keeps the working copy plaintext). Tolerates the legacy
  `OPEN_ROUTER_API_KEY` name with a nudge to rename. The key is never printed.
- **Costs credit.** Successful generations spend OpenRouter credit; failed calls
  (auth / bad model / bad request) generally do not.
- **Model-agnostic by design.** The factory commits to no single model. Bench
  several by looping this engine over a model list; pin the winner per series or
  per image.
- **Tests ship with the skill.** `python .claude/skills/image-gen/tests.py` runs
  the stdlib unit tests offline (no network, no API cost) — every pure helper plus
  an injected-caller run of `generate()`. Run it after any change to `generate.py`.
- **Print resolution.** Managed models cap output resolution; for KDP print
  (~2,625 px/side at 300 DPI for 8.5") an upscale stage is a separate component.
