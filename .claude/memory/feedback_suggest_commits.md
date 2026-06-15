---
name: feedback-suggest-commits
description: "When a commit seems appropriate, suggest it but wait for confirmation — never auto-commit"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ad0f36ec-5ceb-4613-80b8-e7e99fd914eb
---

When a commit looks appropriate (memory changes, a finished unit of work, a good checkpoint), *suggest* that it's a good time to commit — but wait for explicit confirmation before running it. Don't auto-commit.

**Why:** The user wants to stay in control of what enters git history and when, especially because this work spans two machines where commit/push timing affects sync.

**How to apply:** Surface the suggestion ("this looks like a good point to commit — want me to?") and pause. Applies to all commits, with extra relevance to `[[memory-principles-not-state]]` memory writes, which are now version-controlled and only sync between machines once committed and pushed.
