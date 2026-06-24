#!/usr/bin/env python3
"""draw-diagram — author an editable draw.io (.drawio) technical diagram from a simple spec, then
render it to PNG with Pillow (no draw.io app, no system binary; same input -> same pixels).

The .drawio is the single source of truth: a student can open and edit it in draw.io (free), and a
re-render reflects light edits. The renderer understands the box / container / arrow / label subset
this skill authors — exactly what cloud-architecture teaching diagrams need; it is not a general
draw.io renderer.

This is the technical-diagram half of the deck image pipeline (slide-plan `image: diagram` source);
the decorative half is the separate image-gen skill.

Spec (a dict / JSON):
  {
    "title": "Security-group chain",
    "nodes": [
      {"id": "alb", "label": "sg-alb\\n443 from staff CIDR", "row": 0, "col": 0, "fill": "blue"},
      {"id": "app", "label": "sg-app",                        "row": 1, "col": 0, "fill": "green"},
      {"id": "db",  "label": "sg-db",                         "row": 2, "col": 0, "fill": "amber"}
    ],
    "edges": [
      {"from": "alb", "to": "app", "label": "to sg-app"},
      {"from": "app", "to": "db",  "label": "SQL to sg-db"}
    ]
  }
Nodes lay out on a grid by (row, col); a node missing row/col auto-stacks. `fill` is a palette name
(blue/green/amber/grey/purple/red) or a #hex.

CLI (run with the skill's venv python — see SKILL.md):
  python draw_diagram.py --spec spec.json --out diagram.drawio --png [diagram.png]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit(
        "ERROR: Pillow is required for the draw-diagram skill but is not installed.\n"
        "Set up the skill's virtualenv (see .claude/skills/draw-diagram/SKILL.md), then run via that python:\n"
        "  python -m venv .claude/skills/draw-diagram/.venv\n"
        "  .claude/skills/draw-diagram/.venv/Scripts/python -m pip install -r .claude/skills/draw-diagram/requirements.txt   (Windows)\n"
        "  .claude/skills/draw-diagram/.venv/bin/python   -m pip install -r .claude/skills/draw-diagram/requirements.txt   (macOS/Linux)"
    )

# box + grid geometry (draw.io points)
W, H, GX, GY, MARGIN = 200, 70, 80, 70, 40

PALETTE = {  # name -> (fill, stroke)
    "blue":   ("#dae8fc", "#6c8ebf"),
    "green":  ("#d5e8d4", "#82b366"),
    "amber":  ("#ffe6cc", "#d79b00"),
    "grey":   ("#f5f5f5", "#666666"),
    "purple": ("#e1d5e7", "#9673a6"),
    "red":    ("#f8cecc", "#b85450"),
}


def _fill(name):
    if not name:
        return PALETTE["grey"]
    if str(name).startswith("#"):
        return (name, "#444444")
    return PALETTE.get(name, PALETTE["grey"])


# --- author the .drawio (stdlib) ---------------------------------------------
def build_drawio(spec: dict) -> str:
    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    auto = 0
    for n in nodes:
        if "row" not in n or "col" not in n:
            n.setdefault("row", auto)
            n.setdefault("col", 0)
            auto += 1
    cells = []
    for n in nodes:
        fill, stroke = _fill(n.get("fill"))
        x = MARGIN + n["col"] * (W + GX)
        y = MARGIN + n["row"] * (H + GY)
        label = escape(str(n.get("label", n["id"]))).replace("\\n", "&#10;").replace("\n", "&#10;")
        style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
                 "fontSize=14;align=center;verticalAlign=middle;")
        cells.append(
            f'<mxCell id="{escape(str(n["id"]))}" value="{label}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{W}" height="{H}" as="geometry"/></mxCell>'
        )
    for i, e in enumerate(edges):
        label = escape(str(e.get("label", "")))
        style = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;fontSize=12;"
        cells.append(
            f'<mxCell id="e{i}" value="{label}" style="{style}" edge="1" parent="1" '
            f'source="{escape(str(e["from"]))}" target="{escape(str(e["to"]))}">'
            f'<mxGeometry relative="1" as="geometry"/></mxCell>'
        )
    name = escape(str(spec.get("title", "Diagram")))
    body = "".join(cells)
    return (
        '<mxfile host="diploma-cloud-cyber">'
        f'<diagram id="d1" name="{name}">'
        '<mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" '
        'connect="1" arrows="1" fold="1" page="1" pageScale="1" math="0" shadow="0">'
        f'<root><mxCell id="0"/><mxCell id="1" parent="0"/>{body}</root>'
        "</mxGraphModel></diagram></mxfile>"
    )


def save_drawio(xml: str, path: Path) -> Path:
    path = Path(path)
    path.write_text(xml, encoding="utf-8")
    ET.fromstring(xml)  # well-formedness guard
    return path


# --- parse the .drawio subset we author --------------------------------------
def _style_get(style: str, key: str, default=None):
    m = re.search(rf"{key}=([^;]+)", style or "")
    return m.group(1) if m else default


def parse_drawio(xml: str):
    """Return (nodes, edges) for the box/edge subset. nodes: id->dict; edges: list of dicts."""
    root = ET.fromstring(xml)
    nodes, edges = {}, []
    for cell in root.iter("mxCell"):
        if cell.get("vertex") == "1":
            geo = cell.find("mxGeometry")
            nodes[cell.get("id")] = {
                "label": (cell.get("value") or "").replace("&#10;", "\n").replace("\\n", "\n"),
                "x": float(geo.get("x", 0)), "y": float(geo.get("y", 0)),
                "w": float(geo.get("width", W)), "h": float(geo.get("height", H)),
                "fill": _style_get(cell.get("style"), "fillColor", "#f5f5f5"),
                "stroke": _style_get(cell.get("style"), "strokeColor", "#444444"),
            }
        elif cell.get("edge") == "1":
            edges.append({"source": cell.get("source"), "target": cell.get("target"),
                          "label": cell.get("value") or ""})
    return nodes, edges


# --- render with Pillow ------------------------------------------------------
def _font(size):
    for name in ("arial.ttf", "DejaVuSans.ttf", "Helvetica.ttf", "LiberationSans-Regular.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size)   # Pillow >= 10.1: scalable default
    except TypeError:
        return ImageFont.load_default()


def _wrap(draw, text, font, max_w):
    out = []
    for raw in text.split("\n"):
        words, line = raw.split(" "), ""
        for wd in words:
            trial = (line + " " + wd).strip()
            if draw.textlength(trial, font=font) <= max_w or not line:
                line = trial
            else:
                out.append(line)
                line = wd
        out.append(line)
    return out


def _anchors(a, b):
    """Pick (start_point, end_point, end_dir) between boxes a and b — vertical or horizontal."""
    acx, acy = a["x"] + a["w"] / 2, a["y"] + a["h"] / 2
    bcx, bcy = b["x"] + b["w"] / 2, b["y"] + b["h"] / 2
    if abs(bcy - acy) >= abs(bcx - acx):           # mostly vertical
        if bcy >= acy:
            return (acx, a["y"] + a["h"]), (bcx, b["y"]), "down"
        return (acx, a["y"]), (bcx, b["y"] + b["h"]), "up"
    if bcx >= acx:                                  # mostly horizontal
        return (a["x"] + a["w"], acy), (b["x"], bcy), "right"
    return (a["x"], acy), (b["x"] + b["w"], bcy), "left"


def render(nodes: dict, edges: list, scale: int = 2) -> "Image.Image":
    width = int(max((n["x"] + n["w"] for n in nodes.values()), default=W) + MARGIN)
    height = int(max((n["y"] + n["h"] for n in nodes.values()), default=H) + MARGIN)
    img = Image.new("RGB", (width * scale, height * scale), "white")
    d = ImageDraw.Draw(img)
    S = scale
    body_font = _font(14 * S)
    edge_font = _font(12 * S)

    # edges first (behind boxes)
    for e in edges:
        a, b = nodes.get(e["source"]), nodes.get(e["target"])
        if not a or not b:
            continue
        (sx, sy), (ex, ey), dirn = _anchors(a, b)
        # orthogonal elbow through the midpoint
        if dirn in ("down", "up"):
            my = (sy + ey) / 2
            pts = [(sx, sy), (sx, my), (ex, my), (ex, ey)]
        else:
            mx = (sx + ex) / 2
            pts = [(sx, sy), (mx, sy), (mx, ey), (ex, ey)]
        d.line([(p[0] * S, p[1] * S) for p in pts], fill="#444444", width=max(2, S))
        # arrowhead at end
        ah = 8 * S
        if dirn == "down":
            head = [(ex * S, ey * S), (ex * S - ah / 2, ey * S - ah), (ex * S + ah / 2, ey * S - ah)]
        elif dirn == "up":
            head = [(ex * S, ey * S), (ex * S - ah / 2, ey * S + ah), (ex * S + ah / 2, ey * S + ah)]
        elif dirn == "right":
            head = [(ex * S, ey * S), (ex * S - ah, ey * S - ah / 2), (ex * S - ah, ey * S + ah / 2)]
        else:
            head = [(ex * S, ey * S), (ex * S + ah, ey * S - ah / 2), (ex * S + ah, ey * S + ah / 2)]
        d.polygon(head, fill="#444444")
        if e["label"]:
            lx, ly = pts[1][0] * S + 4 * S, pts[1][1] * S - 16 * S
            d.text((lx, ly), e["label"], fill="#333333", font=edge_font)

    # boxes + labels on top
    for n in nodes.values():
        x0, y0 = n["x"] * S, n["y"] * S
        x1, y1 = (n["x"] + n["w"]) * S, (n["y"] + n["h"]) * S
        d.rounded_rectangle([x0, y0, x1, y1], radius=8 * S, fill=n["fill"], outline=n["stroke"], width=max(2, S))
        lines = _wrap(d, n["label"], body_font, n["w"] * S - 12 * S)
        lh = (body_font.getbbox("Ay")[3] - body_font.getbbox("Ay")[1]) + 4 * S
        ty = (y0 + y1) / 2 - (len(lines) * lh) / 2
        for ln in lines:
            tw = d.textlength(ln, font=body_font)
            d.text(((x0 + x1) / 2 - tw / 2, ty), ln, fill="#222222", font=body_font)
            ty += lh
    return img


def render_drawio(drawio_path, png_path=None, scale: int = 2) -> Path:
    drawio_path = Path(drawio_path)
    png_path = Path(png_path) if png_path else drawio_path.with_suffix(".png")
    nodes, edges = parse_drawio(drawio_path.read_text(encoding="utf-8"))
    img = render(nodes, edges, scale=scale)
    png_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(png_path, "PNG", dpi=(150 * scale, 150 * scale))
    return png_path


def main(argv=None) -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Author a .drawio from a spec and render it to PNG (Pillow).")
    ap.add_argument("--spec", required=True, help="path to a JSON spec")
    ap.add_argument("--out", required=True, help="output .drawio path")
    ap.add_argument("--png", nargs="?", const=True, default=False,
                    help="also render a PNG (optional path; defaults next to the .drawio)")
    args = ap.parse_args(argv)

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    out = save_drawio(build_drawio(spec), Path(args.out))
    print(f"wrote {out}")
    if args.png:
        png = render_drawio(out, None if args.png is True else Path(args.png))
        print(f"rendered {png}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
