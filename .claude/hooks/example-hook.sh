#!/usr/bin/env bash
# =============================================================================
# EXAMPLE HOOK SCRIPT (referenced from ../settings.json -> hooks.PreToolUse)
# -----------------------------------------------------------------------------
# Hooks let the HARNESS (not Claude) run logic on lifecycle events. A `command`
# hook receives the event as JSON on stdin and communicates back via:
#   - exit code 0  -> allow / continue (stdout may add context)
#   - exit code 2  -> block the action (stderr is shown as the reason)
#   - JSON on stdout -> structured decision (advanced)
#
# Common events you can wire up in settings.json:
#   SessionStart · PreToolUse · PostToolUse · UserPromptSubmit · Stop ·
#   PreCompact · Notification · SubagentStart/Stop · FileChanged · ...
#
# This example just logs the event and allows it. It is NOT doing anything real.
# On Windows, prefer a PowerShell script or ensure bash is on PATH; mark +x on Unix.
# =============================================================================

payload="$(cat)"               # the event JSON from stdin
echo "[example-hook] fired: ${payload}" >&2   # visible in hook debug output
exit 0                          # allow the tool call to proceed
