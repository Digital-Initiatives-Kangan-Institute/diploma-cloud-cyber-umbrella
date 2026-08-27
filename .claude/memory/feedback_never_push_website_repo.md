---
name: feedback-never-push-website-repo
description: "Commit anywhere, but never push a website repo — the push triggers a continuous-deployment redeploy"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a40bd230-c889-45bf-97c8-0b1ee173f18b
  modified: 2026-08-26T17:53:54.720Z
---

Committing to a **website** sub-repo is fine. **Pushing** it is not — the push kicks off a
continuous-deployment cycle and redeploys the live scenario site. Hold website pushes for the human.

Pushing the **other** repos (umbrella, content) is fine when asked, **even when the push carries
commits from other sessions**. Don't flag those as a concern or hold the push for them.

**Why:** a website push has an immediate external effect (the live site changes) that the human wants
to time deliberately, usually after the matching content/instrument changes have landed. Commits carry
no such effect, so they are not the thing to gate. Extra commits riding along on a content push are
harmless — the earlier flagging of them was noise.

**How to apply:** commit in every repo as normal (still asking first, per
[[feedback-suggest-commits]]). When proposing or running a push, exclude the website repo and say why
in one line. Don't enumerate other sessions' commits that a non-website push would carry.
