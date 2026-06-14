---
# SUBAGENT — a delegate Claude can hand focused work to.
# Identity comes from the `name:` field (NOT the filename). Folders under agents/ are
# just organization. The markdown body becomes this agent's system prompt.

name: example-agent                     # REQUIRED — how Claude refers to/spawns it
description: >-                          # REQUIRED — when Claude should delegate here
  Example subagent template. Describe the kind of task this agent is best at so Claude
  knows when to route work to it.

# tools: ["Read", "Grep", "Glob"]       # allowed tools (inherits all if omitted)
# disallowedTools: ["Bash"]             # denied tools (applied before `tools`)
# model: inherit                        # sonnet|opus|haiku|fable|<full-id>|inherit
# permissionMode: default               # default|acceptEdits|plan|dontAsk|bypassPermissions
# maxTurns: 20                          # cap on agentic turns
# skills: ["example-skill"]             # preload these skills' full content at startup
# mcpServers: ["example-http-server"]   # MCP servers available to this agent
# memory: project                       # persistent memory scope: user|project|local
# background: false                     # always run as a background task
# effort: high                          # low|medium|high|xhigh|max
# isolation: worktree                   # run in an isolated git worktree
# color: cyan                           # display color in the UI
---

# Example subagent

You are a focused subagent. Describe the role, the method, and the expected output here.
Keep it tight — this prompt replaces the agent's general instructions for its task.

- State what to do and what NOT to do.
- Define the exact shape of the result you should return to the main session.
