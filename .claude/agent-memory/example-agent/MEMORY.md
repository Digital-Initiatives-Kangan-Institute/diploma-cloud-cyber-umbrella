# Agent memory index — example-agent (project scope)

> This is the persistent memory for the subagent named `example-agent`, at **project**
> scope (committed to git, shared across machines). The first ~200 lines / 25KB of this
> index file are loaded when the agent starts; topic files alongside it are read on demand.
>
> Scopes: `project` -> `.claude/agent-memory/<agent>/` (committed) ·
> `local` -> `.claude/agent-memory-local/<agent>/` (gitignored) ·
> `user` -> `~/.claude/agent-memory/<agent>/` (all projects).

## Index
- [example-topic.md](example-topic.md) — one-line hook describing what's in the topic file

<!-- Add one line per topic file. Keep facts in the topic files, not here. -->
