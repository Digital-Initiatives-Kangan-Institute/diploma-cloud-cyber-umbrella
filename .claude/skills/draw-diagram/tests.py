#!/usr/bin/env python3
"""Offline tests for draw-diagram — run with the skill's venv python:

  .claude/skills/draw-diagram/.venv/Scripts/python .claude/skills/draw-diagram/tests.py   (Windows)
  .claude/skills/draw-diagram/.venv/bin/python     .claude/skills/draw-diagram/tests.py   (macOS/Linux)

Covers the stdlib build/parse/geometry helpers and a real Pillow render round-trip. No network.
"""
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import draw_diagram as dd

SPEC = {
    "title": "Test net",
    "nodes": [
        {"id": "fw", "label": "Firewall", "row": 1, "col": 1, "fill": "red"},
        {"id": "sw", "label": "Switch", "row": 2, "col": 1, "fill": "blue"},
        {"id": "pc", "label": "PC-1\n10.0.0.11", "row": 3, "col": 0, "fill": "green"},
    ],
    "edges": [
        {"from": "fw", "to": "sw", "label": "LAN"},
        {"from": "sw", "to": "pc", "label": ""},
    ],
}


class TestBuild(unittest.TestCase):
    def test_wellformed_and_counts(self):
        xml = dd.build_drawio(SPEC)
        root = ET.fromstring(xml)  # raises if malformed
        verts = [c for c in root.iter("mxCell") if c.get("vertex") == "1"]
        edges = [c for c in root.iter("mxCell") if c.get("edge") == "1"]
        self.assertEqual(len(verts), 3)
        self.assertEqual(len(edges), 2)

    def test_geometry_from_row_col(self):
        nodes, _ = dd.parse_drawio(dd.build_drawio(SPEC))
        # fw at row 1, col 1
        self.assertEqual(nodes["fw"]["x"], dd.MARGIN + 1 * (dd.W + dd.GX))
        self.assertEqual(nodes["fw"]["y"], dd.MARGIN + 1 * (dd.H + dd.GY))

    def test_auto_stack(self):
        spec = {"nodes": [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}], "edges": []}
        nodes, _ = dd.parse_drawio(dd.build_drawio(spec))
        self.assertEqual(nodes["a"]["y"], dd.MARGIN)               # row 0
        self.assertEqual(nodes["b"]["y"], dd.MARGIN + (dd.H + dd.GY))  # row 1


class TestParseRoundTrip(unittest.TestCase):
    def test_nodes_and_edges(self):
        nodes, edges = dd.parse_drawio(dd.build_drawio(SPEC))
        self.assertEqual(set(nodes), {"fw", "sw", "pc"})
        self.assertEqual(nodes["pc"]["label"], "PC-1\n10.0.0.11")   # \n preserved
        self.assertIn({"source": "fw", "target": "sw", "label": "LAN"}, edges)

    def test_fill_resolves(self):
        nodes, _ = dd.parse_drawio(dd.build_drawio(SPEC))
        self.assertEqual(nodes["fw"]["fill"], dd.PALETTE["red"][0])


class TestRender(unittest.TestCase):
    def test_render_produces_png(self):
        nodes, edges = dd.parse_drawio(dd.build_drawio(SPEC))
        img = dd.render(nodes, edges, scale=2)
        w = int(max(n["x"] + n["w"] for n in nodes.values()) + dd.MARGIN) * 2
        h = int(max(n["y"] + n["h"] for n in nodes.values()) + dd.MARGIN) * 2
        self.assertEqual(img.size, (w, h))

    def test_render_drawio_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            drawio = dd.save_drawio(dd.build_drawio(SPEC), Path(d) / "t.drawio")
            png = dd.render_drawio(drawio)
            self.assertTrue(png.is_file())
            from PIL import Image
            with Image.open(png) as im:
                self.assertGreater(im.size[0], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
