# Temporal Awareness for AI Assistants

A pattern for AI projects that use filesystem access.

---

## The Problem

AI assistants have no internal sense of time within a conversation. Every message feels like it arrived moments after the last one, whether five seconds or five hours have actually passed.

This creates two failure modes:

**At session start:** The AI doesn't know how long it's been since the last session. A return after a long gap feels the same as a continuation from moments ago.

**Mid-chat:** In a long conversation that spans hours or days, the AI has no way to know the human left and came back. If a gap passes between messages in the same chat, the AI continues as if moments elapsed, writes timestamps based on its last clock reading or guesses entirely, and produces logs that are hours wrong.

The second failure mode is worse because it's invisible. A startup procedure has a defined moment to check the clock. A mid-chat return has no trigger unless one is built in. Without one, the AI's only time reference is its startup clock reading. When the user returns after a long gap, the AI has no signal that time has passed and may confidently fabricate timestamps based on the stale reading. Nothing in the AI's internal state flags the error.

This matters because the filesystem is a long-term record. Logs with fabricated timestamps corrupt the project's timeline and mislead future sessions.

---

## The Solution

Temporal awareness is a continuous behavior, not a startup event. It has two components:

1. **What time is it now?**
2. **How long has it been since the last known time reference?**

The mechanism depends on what the platform can do. Where it can run a script on every message, the script injects the current time into each turn; this is how the Claude Code setup works. Where it cannot, a clock file and filesystem metadata provide the time source. Both approaches solve the same problem; the mechanism differs.

### Why Both Checks Are Required

The startup check handles the common case: a new session orienting to the project. The mid-session check handles the case the startup check cannot: a human who leaves a continuing conversation and returns hours or days later.

Without a mid-session check, the AI's only time reference is its startup reading. When the human returns after a gap, the AI has no signal that time has passed. It writes timestamps based on the stale reading or fabricates them entirely.

### File Metadata as Context

When processing files the human drops in an inbox or working directory, the modified timestamp on those files tells you when the human placed them there. Email files (.eml) also contain send/receive timestamps in their headers. Both sources help reconstruct the timeline of events that happened between work sessions.

### Cross-Referencing Timestamps

Screenshot filenames often contain timestamps in the filename itself. Email headers contain send times. PDF metadata may contain creation dates. These all serve as independent time references when a single time source isn't sufficient.

---

## Implementation

**With a per-message script (Claude Code).** A UserPromptSubmit hook injects the current local time into every turn automatically. See [claude-code-setup.md](../claude-code-setup.md) for the setup.

**With a clock file (platforms without per-message scripts).** Keep one small file for the purpose. To take a reading, the AI overwrites the file and reads its modified time. Read the modified time, not the created time: the created time is the file's birth and does not change when the file is overwritten. Take a reading at session start, and again mid-session before the first file operation in a response when the last reading is old.

---

## Limitations

Timestamps are approximate. The time on a file reflects when the AI wrote it, not when the user sent the message that prompted it. There's a delay between the message and the write that depends on how much work the AI does before writing the file.

The clock-file method only works where the session can reach the filesystem. A session without filesystem access has no file metadata to work with.

File metadata reflects the timezone of the machine, which is useful but means the AI needs to note the timezone in log entries.

Within a single rapid exchange (messages seconds apart), the timestamps won't be meaningfully different. The mid-session check is designed to detect gaps of hours, not seconds.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.9*
