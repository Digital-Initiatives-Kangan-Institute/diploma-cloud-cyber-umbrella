# image-gen

The deterministic image-generation **engine** for the KDP factory — a no-LLM
wrapper around the OpenRouter image API. Give it a resolved prompt, reference
image(s), and a model; it saves candidate images for human curation.

It is the **base unit** other image skills (character reference, cover, page art)
compose on top of: it performs no prompt composition and holds no IP knowledge.

- `generate.py` — the engine (CLI + pure, testable functions).
- `tests.py` — stdlib unit tests, offline, no API cost: `python .claude/skills/image-gen/tests.py`.
- `SKILL.md` — how/when to use it.

See `SKILL.md` for parameters and the layering it fits into.
