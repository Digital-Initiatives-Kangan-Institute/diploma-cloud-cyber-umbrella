# Common

Shared across more than one process. `common/` is the parent rather than `helpers/` directly, so things
that are shared but are **not** Python helpers — fixtures, schemas, shared vocabularies — get a home
without a later rename.

| Folder | Holds |
|---|---|
| `helpers/` | shared Python modules (today's `scripts/helpers/`: docx/pptx construction, run-sheet and workbook engines, UoC tag parsing) |

Wherever the same logic appears in more than one step, it moves here and is tested on its own — a
`common/` module is covered by its own cases in the test plan (`H-` prefix), not indirectly through a
caller.

## Status

Structure only — **nothing ported**. The legacy `scripts/helpers/` is still live and still where every
caller resolves its imports.

`[TBD — needs discussion: helper migration]` — a helper cannot move on its own: 90 scripts reach their
dependencies through `sys.path.insert()` against the legacy path, so moving a module means updating the
callers that resolve it. Whether helpers move per-module as steps port, or in one pass, is open.
