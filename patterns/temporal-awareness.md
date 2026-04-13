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

The mechanism: a persistent Clock file and filesystem metadata. The Clock file lives permanently in the project directory. The AI writes to it (overwriting the content) and then reads the modified timestamp. This is the only reliable time source.

**Critical distinction:** Reading metadata on an old file tells you when *that file* was written, not what time it is now. Only a freshly modified file reflects the actual current time.

**Important (macOS):** Read only the "modified" field from the file's metadata. Ignore the "created" field. On macOS APFS, "created" is the file's birth time and never updates after initial creation. If the Clock file was created on a Monday and edited on a Wednesday, "created" still says Monday. Only "modified" reflects the edit.

---

## Setup

Create a Clock directory in your project's Workflow Files with a single text file inside it:

```
[project base path]/Workflow Files/Clock/timestamp.txt
```

Contents can be anything. The file is permanent and reusable. Never delete it.

---

## Implementation

### 1. The Clock Mechanism

To know the current time:

1. Write "tick" to the Clock file (overwrite)
2. Get the file's info using Filesystem tools — the "modified" field is the current time
3. If the modified date is earlier than the system prompt date, repeat both steps once

The first read of a session may return stale metadata from an earlier tick rather than the one just written. The sanity check against the system prompt date catches this without requiring an external time reference.

Do not create throwaway files. Do not rely on metadata from files written in previous exchanges. Do not estimate, infer, or guess the time. The clock mechanism exists because the AI has no other reliable time source.

### 2. When to Check the Clock

Temporal awareness requires checking the clock at two points:

**At startup (step 3 of the startup procedure):** Tick the clock. Then get the most recent session log's file info and compare its modified timestamp to the clock reading. The difference tells you how long it's been since the last logged interaction. This informs orientation: a return after three days means more may have changed than a continuation from an hour ago.

**Mid-chat, before the first filesystem operation in each response:** Get the Clock file's info (do NOT tick it yet — just read the existing metadata). Compare the "modified" field to the system prompt date.

If the last clock check was on a **different calendar date**, or **more than two hours ago**:

1. Tick the clock (write "tick", get file info)
2. Calculate the gap between the old reading and the new one
3. Acknowledge the gap to the user briefly before continuing with their request
4. Record the gap in the session log at the next log write

If the last clock check was today and less than two hours ago: continue with the user's request. No additional action needed.

The mid-chat check costs one tool call per response in the common case (reading file metadata). The full tick sequence only fires when a meaningful gap is detected.

### 3. Why Both Checks Are Required

The startup check handles the common case: a new chat orienting to the project. The mid-chat check handles the case the startup check cannot: a human who leaves a continuing chat and returns hours or days later.

Without the mid-chat check, the AI's only time reference is its startup clock reading. When the human returns after a gap, the AI has no signal that time has passed. It writes timestamps based on the stale reading or fabricates them entirely.

The mid-chat check detects this gap by reading the Clock file's existing metadata before doing any filesystem work. If the metadata is stale, a gap has occurred. The full clock tick then establishes the actual current time.

### 4. File Metadata as Context

When processing files the human drops in an inbox or working directory, the modified timestamp on those files tells you when the human placed them there. Email files (.eml) also contain send/receive timestamps in their headers. Both sources help reconstruct the timeline of events that happened between work sessions.

### 5. Cross-Referencing Timestamps

Screenshot filenames often contain timestamps in the filename itself. Email headers contain send times. PDF metadata may contain creation dates. These all serve as independent time references when file metadata alone isn't sufficient.

---

For the deployable WORKFLOW section text, see the [temporal awareness template](../templates/workflow-sections/temporal-awareness.md).

---

## Limitations

Timestamps are approximate. The time on a file reflects when the AI wrote it, not when the user sent the message that prompted it. There's a delay between the message and the write that depends on how much work the AI does before writing the file.

This only works with filesystem access (typically a desktop application). On mobile or web, the AI has no file metadata to work with and no temporal awareness.

File metadata reflects the timezone of the machine, which is useful but means the AI needs to note the timezone in log entries.

Within a single rapid exchange (messages seconds apart), the timestamps won't be meaningfully different. The mid-chat check is designed to detect gaps of hours, not seconds.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.2*
