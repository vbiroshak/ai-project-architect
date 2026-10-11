# Evolving State in Session Handoffs

---

## The Problem

Session logs that track design questions or decisions as binary (open/closed, resolved/unresolved) lose the middle of the thinking process. A topic progresses through stages: not yet discussed → context gathered → options identified → partially decided → resolved. Logging only the endpoints forces the next session to restart topics where significant work was done.

This is the default failure mode wherever decisions develop across sessions, not an edge case. The cost falls on the human, who has to reconstruct their own prior thinking; their memory of conversational decisions fades just as the AI's context window ends. The session log's job is not only to orient the next session but to protect the human from repeating themselves.

---

## The Fix

Replace binary framing with state-of-thinking capture.

Instead of:

```
OPEN QUESTIONS FOR NEXT SESSION
- Where should the quarterly reports go?
- How to handle items that span multiple categories?
```

Use:

```
QUESTIONS: STATE OF THINKING AT SESSION END

- Report location: discussed extensively. Currently in
  the shared folder but used primarily by one team.
  Consensus leaning toward moving into the team's
  sub-project. Summary spreadsheet would absorb into
  it. Remaining question: whether to create sub-folders
  by quarter or keep flat.

- Cross-category items: three examples examined. Emerging
  principle: documents stay in their primary category even
  when they're relevant to other areas. Working copies can
  go to wherever the active project is. Not yet tested
  against remaining items.
```

Each item captures:

- What information was gathered
- What options were considered
- Where the person's thinking landed
- What specifically still needs to be figured out

The next session picks up each thread from its actual state rather than treating it as a blank slate.

---

## Related Principle

### Reconcile Logs Against Current State

When updating a session log late in a session with decisions made after the first entry, reconcile every section of the log against the current state; do not append new information and leave earlier sections inconsistent. A log that contradicts itself is worse than an incomplete one: it misleads.

---

## Application

This applies to any project that tracks decisions, design questions, or ongoing investigations across sessions. It is especially important in:

- Session logs (the state of thinking at session end)
- HANDOFF.txt (which carries forward the current state)
- Task queue items that have associated reasoning
- Sub-project reference files that evolve through use

The general principle: when something is in process, log the state of the process, not just the fact that it is in process.

---

The evolving state principle is deployed through the EVOLVING STATE entry in the SESSION LOGS section of the [PROJECT_CONTEXT template](../templates/claude-code/PROJECT-CONTEXT-template.md).

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.11*
