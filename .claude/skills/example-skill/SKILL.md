---
# SKILL — invokable as /example-skill (the FOLDER name becomes the command name).
# Claude may also auto-invoke it when `description`/`when_to_use` match the task.
# Full frontmatter reference below; all fields except the body are OPTIONAL.

name: Example Skill                     # display name (command name still = folder name)
description: >-                         # when to use it (Claude reads this to auto-invoke)
  Example skill template. Demonstrates frontmatter and content substitutions.
when_to_use: >-                         # extra auto-invocation context (appended to description)
  Use as a reference when authoring a new skill in this project.

argument-hint: "[target]"               # shown in the / menu
arguments: ["target"]                   # named positional args -> use as $target in body

# disable-model-invocation: true        # only manual /example-skill (Claude won't auto-pick)
# user-invocable: false                 # hide from / menu (Claude can still invoke)
# allowed-tools: ["Read", "Grep"]       # pre-approve tools while this skill runs
# disallowed-tools: ["Bash"]            # remove tools while this skill runs
# model: inherit                        # sonnet|opus|haiku|fable|<full-id>|inherit
# effort: high                          # low|medium|high|xhigh|max
# context: fork                         # run in a forked subagent context
# agent: Explore                        # subagent type to use when context: fork
# shell: powershell                     # shell for !`command` injection (default: bash)
---

# Example Skill

Write the skill's instructions here as if briefing Claude. Useful substitutions:

- `$ARGUMENTS` — all args; `$0`/`$ARGUMENTS[0]` — first arg; `$target` — named arg.
- `${CLAUDE_SKILL_DIR}` — this skill's folder (reference bundled templates/scripts).
- `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`.
- `` !`echo hello` `` — injects a shell command's output before Claude sees the prompt.

## Supporting files
Put templates, examples, or scripts alongside this file (e.g. `templates/`, `scripts/`).
They are loaded on demand only when referenced — keep SKILL.md itself lean.
