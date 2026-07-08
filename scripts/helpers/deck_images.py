#!/usr/bin/env python3
"""deck_images — resolve a slide-plan `image:` directive into something the deck builder can place.

The slide plan declares one `image:` value per slide (slide-plan-format.md). This bridge turns that
declaration into a placement instruction for kangan_deck:

  none              -> None                      (no image on the slide)
  diagram <ref>     -> {"path": <png>, ...}       render <topic>/diagrams/<ref>.json in-pipeline via
                                                  the draw-diagram skill (editable .drawio + Pillow PNG)
  gen <prompt>      -> placeholder by default     image-gen costs money + needs a key; only run when
                                                  explicitly enabled (allow_gen=True), else placeholder
  reuse <ref>       -> {"label": <ref>}           human pastes an existing external asset (e.g. AWS)
  placeholder <n>   -> {"label": <n>}             human supplies it
                      -> {"label": ...} is a placeholder; {"path": ...} is a real picture.

Generated diagrams are deterministic + offline (no key); they are placed straight into the deck. The
.drawio stays beside the PNG as the editable source (student-editable; manual draw.io export is the
fallback if a render isn't close enough — see the draw-diagram SKILL.md)."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

# Nano Banana — Gemini 2.5 Flash Image (low cost, ~US$0.04/image). The decorative-image model.
GEN_MODEL = "google/gemini-2.5-flash-image"


def _umbrella_root(start: Path) -> Path:
    """Walk up from `start` to the dir that holds .claude/skills/draw-diagram (the umbrella root —
    the launch dir; skills live only there, not in the sub-repo)."""
    for d in [start, *start.parents]:
        if (d / ".claude" / "skills" / "draw-diagram" / "draw_diagram.py").exists():
            return d
    raise FileNotFoundError(
        "Could not locate the draw-diagram skill (.claude/skills/draw-diagram). "
        "Run the build from the umbrella workspace root."
    )


def _venv_python(skill_dir: Path) -> Path:
    """The skill's own venv python (per the skill-dependencies convention)."""
    win = skill_dir / ".venv" / "Scripts" / "python.exe"
    nix = skill_dir / ".venv" / "bin" / "python"
    if win.exists():
        return win
    if nix.exists():
        return nix
    raise FileNotFoundError(
        f"draw-diagram venv missing ({skill_dir/'.venv'}). One-time setup:\n"
        f"  python -m venv {skill_dir/'.venv'}\n"
        f"  <venv python> -m pip install -r {skill_dir/'requirements.txt'}\n"
        "See the draw-diagram SKILL.md."
    )


def _render_diagram(ref: str, topic_dir: Path) -> dict:
    """Render <topic_dir>/diagrams/<ref>.json -> .drawio + .png via the draw-diagram skill. Returns
    a placement dict {"path", "label", "drawio"}."""
    spec = topic_dir / "diagrams" / f"{ref}.json"
    if not spec.exists():
        raise FileNotFoundError(
            f"image: diagram {ref} -> missing spec {spec}. Author the draw-diagram JSON spec there."
        )
    out_drawio = spec.with_suffix(".drawio")
    out_png = spec.with_suffix(".png")
    skill_dir = _umbrella_root(topic_dir) / ".claude" / "skills" / "draw-diagram"
    py = _venv_python(skill_dir)
    cmd = [str(py), str(skill_dir / "draw_diagram.py"),
           "--spec", str(spec), "--out", str(out_drawio), "--png", str(out_png)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"draw-diagram failed for {ref}:\n{res.stdout}\n{res.stderr}")
    return {"path": out_png, "drawio": out_drawio, "label": ref}


def _gen_image(prompt: str, topic_dir: Path) -> dict:
    """Generate a decorative image via the image-gen skill (Nano Banana). Generate-once: a committed
    image for this prompt is reused, so rebuilds cost nothing. Returns {"path", "label"}."""
    topic_dir = Path(topic_dir)
    out_dir = topic_dir / "images"
    name = "gen-" + hashlib.md5(prompt.encode("utf-8")).hexdigest()[:8]
    existing = sorted(out_dir.glob(name + ".*")) if out_dir.exists() else []
    if existing:
        return {"path": existing[0], "label": prompt}      # cached — no API call, no cost
    umbrella = _umbrella_root(topic_dir)
    gen = umbrella / ".claude" / "skills" / "image-gen" / "generate.py"
    cmd = [sys.executable, str(gen), "--model", GEN_MODEL, "--prompt", prompt,
           "--n", "1", "--out", str(out_dir), "--name", name]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(umbrella))
    line = next((l for l in res.stdout.splitlines() if l.startswith("RESULT ")), None)
    data = json.loads(line[len("RESULT "):]) if line else {"ok": False}
    if not data.get("ok") or not data.get("saved"):
        raise RuntimeError(f"image-gen failed for prompt {prompt!r}:\n{res.stdout}\n{res.stderr}")
    return {"path": Path(data["saved"][0]), "label": prompt}


def resolve_image(directive: str, topic_dir: Path, allow_gen: bool = False):
    """Resolve one slide's `image:` directive. Returns None (no image), or a dict that is either a
    placeholder ({"label"}) or a real picture ({"path", "label"})."""
    directive = (directive or "").strip()
    if not directive or directive == "none":
        return None
    kind, _, rest = directive.partition(" ")
    rest = rest.strip()
    kind = kind.lower()
    if kind == "diagram":
        return _render_diagram(rest, Path(topic_dir))
    if kind == "gen":
        if not allow_gen:
            # Cost guard: image-gen calls a paid model. Default to a placeholder; enable explicitly.
            return {"label": f"GEN (not run): {rest}"}
        return _gen_image(rest, topic_dir)
    if kind in ("reuse", "placeholder"):
        return {"label": rest or kind}
    # Unknown keyword -> placeholder naming the raw directive, so nothing is silently dropped.
    return {"label": directive}


if __name__ == "__main__":
    # Smoke test: resolve a directive against a topic dir.  argv: <directive> <topic_dir>
    d = sys.argv[1] if len(sys.argv) > 1 else "none"
    td = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
    print(resolve_image(d, td))
