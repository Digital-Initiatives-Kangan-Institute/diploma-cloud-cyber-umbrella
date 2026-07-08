# review-slides

Render a `.pptx` teaching deck to one PNG per slide (LibreOffice → PyMuPDF) and visually review it —
placeholder boxes, overflow/clipping, image/text overlap, broken layouts, garbled gen images, off-brand
slides. Deterministic + re-runnable. See [SKILL.md](SKILL.md) for the workflow and dependencies
(LibreOffice is a system app; PyMuPDF lives in a gitignored per-skill `.venv/`).
