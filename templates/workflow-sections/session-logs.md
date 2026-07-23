# Session Logs

WORKFLOW section — universal, identical across all projects.

## Template Text

```
---
SESSION LOGS

Location: Workflow Files/Session Logs/
Naming: Session_XXXX.txt (four-digit, zero-padded, sequential across the project). One log per session, numbered to match the session number.

TITLE LINE: The first line of each log file: PROJECT — SESSION NNN — Month DD, YYYY. Example: MYPROJECT — SESSION 042 — July 15, 2026. The date is the day the session started; if a later entry lands on a different day, extend it to a range: MYPROJECT — SESSION 038 — June 25 – July 2, 2026.

ENTRY FORMAT: Each entry begins with a header line: [Date, ~Time Timezone] TOPIC

WHAT TO LOG: Decisions, state changes, reasoning, and the current state of evolving work. Not process narration. Thoroughness applies to coverage. Conciseness applies to expression.

LOG WHEN WORK ACCUMULATES: Write a log entry when substantive decisions, findings, or file changes have accumulated — when losing context now would cost the next session. Each entry should be self-contained. Multiple distinct topics means multiple entries within the same log.

WRITE FREQUENTLY: Sessions can end without warning. Never defer logging to "end of session" or wait to be asked. Logging is insurance against context loss, not a signal that work is finishing. After writing a log entry, continue working.

PAIRED WRITES: Every log entry is paired with a HANDOFF.txt overwrite — both happen together, every time. When the entry covers sub-project work, also verify the sub-project's status file reflects the current state.

STRUCTURE CHANGES: When file operations change directory structure (creating, moving, or renaming files or directories), verify Workflow Files/PROJECT_INDEX.txt reflects the current structure.

FIX ON CONTACT: When you encounter stale or incorrect information in a project file during normal work, fix it then and there before continuing with other work. Do not defer in any form — noting it for later, flagging it as pending, or adding it to a task list all count as deferring.

EVOLVING STATE: Log topics at their current state of progress, not as binary open/closed. Capture what was gathered, what was considered, where thinking landed, and what remains. Each in-progress item should let the next session continue where this one stopped, not restart from scratch.

HANDOFF POINTERS: The handoff controls how much context loads at activation. Point to everything the next session needs. Scale the pointers to the complexity of the work they cover.

After structural or meta work, note which earlier sessions contain the last domain work and carry a compressed domain narrative.

FRESHNESS LINES: Every project file (except session logs and Clock) carries two lines after its title:

  Last updated: [Month DD, YYYY] (Session NNN)
  Last reviewed: [Month DD, YYYY]

"Last updated" means content was intentionally changed — adding, removing, revising, or restructuring. Updating only the freshness lines themselves does not count. "Last reviewed" means content was read and confirmed accurate during substantive work, whether or not anything changed. A correction refreshes both.

For files overwritten wholesale (HANDOFF, STATUS) or newly created, both lines carry the same date and session.
```

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.7*
