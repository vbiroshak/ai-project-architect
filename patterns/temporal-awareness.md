# Temporal Awareness for AI Assistants

A pattern for AI projects that use filesystem access.

---

## The Problem

AI assistants have no internal sense of time within a conversation. Every message feels like it arrived moments after the last one, whether five seconds or five hours have actually passed.

This creates two failure modes:

**At session start:** The AI doesn't know how long it's been since the last session. A return after a long gap feels the same as a continuation from moments ago.

**Mid-session:** In a long session that spans hours or days, the AI has no way to know the human left and came back. If a gap passes between messages in the same session, the AI continues as if moments elapsed, writes timestamps based on its last clock reading or guesses entirely, and produces logs that are hours wrong.

The second is worse because it is invisible: a startup procedure has a defined moment to check the clock, a mid-session return has no trigger unless one is built in. Without one, the AI's only time reference is its startup reading, so when the user returns after a long gap it has no signal that time has passed and may fabricate timestamps from the stale reading, with nothing to flag the error.

This matters because the filesystem is a long-term record. Logs with fabricated timestamps corrupt the project's timeline and mislead future sessions.

---

## The Solution

Temporal awareness is a continuous behavior, not a startup event. It has two components:

1. **What time is it now?**
2. **How long has it been since the last known time reference?**

The mechanism depends on what the platform can do. Where it can run a script on every message, the script injects the current time into each turn; this is how the Claude Code setup works. Where it cannot, a clock file and filesystem metadata provide the time source.

---

## Implementation

**With a per-message script (Claude Code).** A UserPromptSubmit hook injects the current local time into every turn automatically. See [claude-code-setup.md](../claude-code-setup.md) for the setup.

**With a clock file (platforms without per-message scripts).** Keep one small file for the purpose. To take a reading, the AI overwrites the file and reads its modified time. Read the modified time, not the created time: the created time is the file's birth and does not change when the file is overwritten. Take a reading at session start, and again mid-session before the first file operation in a response when the last reading is old.

---

## Limitations

Timestamps are approximate: the time on a file is when the AI wrote it, not when the user sent the message, and the delay depends on how much work the AI does before writing.

The clock-file method needs a session that can reach the filesystem; without file access there is no file metadata.

File metadata is in the machine's timezone, so the AI notes the timezone in log entries.

Within a rapid exchange (messages seconds apart) the timestamps barely differ; the mid-session check detects gaps of hours, not seconds.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.11*
