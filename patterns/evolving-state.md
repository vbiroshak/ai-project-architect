# Evolving State in Session Handoffs

---

## The Problem

Session logs that track design questions or decisions as binary (open/closed, resolved/unresolved) lose the middle of the thinking process. A topic progresses through stages: not yet discussed → context gathered → options identified → partially decided → resolved. Logging only the endpoints forces the next chat to restart from scratch on topics where significant work has already been done.

This is not an edge case. It is the default failure mode for any project where decisions develop across multiple sessions.

---

## Why This Matters More Than It Appears

When a chat re-asks questions that were already discussed in depth, the cost is not just duplicated token spend. The human has to reconstruct their own prior thinking: what they said, what they decided, what context they provided. Human memory of conversational decisions fades just as the AI's context window ends. The person cannot simply recall and restate what they previously worked through, any more than a new chat can.

This is especially damaging in projects with:

**Wide scope.** A project involving hundreds of individual decisions (about file organization, client strategy, research direction) requires context and reasoning for each one. Repeating even a fraction of those conversations is exhausting.

**Extended duration.** Over many sessions, the volume of partially-resolved topics grows. Binary logging (open vs. closed) loses more information as the project stretches longer.

**High personal investment.** When someone has spent significant effort explaining their reasoning, being asked to redo it signals that the system failed to preserve what they contributed. The experience is not just inefficient; it is frustrating and erodes trust in the continuity system.

The session log's job is not just to orient the next chat. It is to protect the human from having to repeat themselves.

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

The next chat picks up each thread from its actual state rather than treating it as a blank slate.

---

## Related Principles

### Act at the Moment of Decision

When a conversation produces a decision, execute it immediately rather than logging it for future action. The same context fade that affects humans between sessions also operates within sessions. A decision captured only as a to-do item requires the next handler (human or AI) to reconstruct the reasoning behind it. A decision executed immediately preserves the reasoning in the action itself.

This compounds with the evolving-state problem: if decisions are deferred AND logged in binary format, both the decision and the context behind it are lost.

### Reconcile Logs Against Current State

When updating a session log late in a conversation (adding context from decisions made after the initial log entry was written), reconcile ALL sections of the log against the current state. Do not append new information while leaving earlier sections inconsistent. A log that contradicts itself between sections is worse than an incomplete log. It actively misleads.

---

## Application

This applies to any project that tracks decisions, design questions, or ongoing investigations across chat sessions. It is especially important in:

- Session logs (the state of thinking at session end)
- HANDOFF.txt (which carries forward the current state)
- Task queue items that have associated reasoning
- Sub-project reference files that evolve through use

The general principle: when something is in process, log the state of the process, not just the fact that it is in process.

---

The evolving state principle is deployed through the EVOLVING STATE subsection of the [session logs template](../templates/workflow-sections/session-logs.md).

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.4*
