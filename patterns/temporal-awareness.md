# Temporal Awareness for AI Assistants

A pattern for AI projects that use filesystem access.

---

## The Problem

AI assistants have no internal sense of time within a conversation. Every message feels like it arrived moments after the last one, whether five seconds or five hours have actually passed. In a long chat that spans a full day or multiple days, this creates blind spots:

The AI doesn't know that the human left and came back. It can't tell whether an update is part of the same work session or a new one hours later. Session logs and documentation lack temporal precision. When reviewing logs later, the actual timeline of events is invisible. And the AI can't make sensible decisions about when to close out a log entry versus append to one.

This matters because the filesystem is a long-term record. Logs without timestamps collapse everything into a flat sequence that obscures the real pace and rhythm of work.

---

## The Solution

Temporal awareness has two components, both essential:

1. **What time is it now?**
2. **How long has it been since the last logged interaction?**

The first gives you the current moment. The second gives you context: is this a continuation from an hour ago, or a return after three days? Both inform how the AI orients to the work. A project that knows it's Friday afternoon but doesn't know the last logged interaction was Monday morning is missing half the picture.

The mechanism: a persistent Clock file and filesystem metadata. The Clock file lives permanently in the project directory. The AI writes to it (overwriting the content) and then reads the modified timestamp. The most recent session log's metadata provides the second component. No throwaway files, no cleanup needed.

**Critical distinction:** Reading metadata on an old file tells you when *that file* was written, not what time it is now. Only a freshly modified file reflects the actual current time.

**Important (macOS):** Read only the "modified" field from the file's metadata. Ignore the "created" field. On macOS APFS, "created" is the file's birth time and never updates after initial creation. If the Clock file was created on a Monday and edited on a Wednesday, "created" still says Monday. Only "modified" reflects the edit.

---

## Setup

Create a Clock directory in your project's Workflow Files with a single text file inside it:

```
[project base path]/Workflow Files/Clock/timestamp.txt
```

Contents can be anything. A description like "This file exists so the AI can check the current time" works. The file is permanent and reusable. Never delete it.

---

## Implementation

### 1. Knowing What Time It Is Now

1. Write "tick" to the Clock file (overwrite)
2. Get the file's info using your Filesystem tools — the "modified" field is the current time
3. If the modified date is earlier than the system prompt date, repeat both steps once

The first read of a session may return stale metadata from a prior session's edit due to filesystem caching. The sanity check against the system prompt date catches this without requiring an external time reference.

Do not create throwaway files. Do not rely on metadata from files written in previous exchanges.

### 2. Knowing When the Last Action Happened

Get the file info on the most recent log file or the last file written in a previous exchange using Filesystem tools. That timestamp tells you when the previous logged interaction happened.

### 3. Detecting Time Gaps (Baseline Startup Behavior)

At session startup, after checking the Clock, get the most recent session log's file info using Filesystem tools. Compare its modified timestamp to the current time from the Clock. The difference tells you how long it's been since the last logged interaction.

This is not optional. Every startup should produce both the current time and the time since last logged interaction. The gap informs orientation: a return after three days means more may have changed than a continuation from an hour ago. It also informs logging: whether to append to a current entry or start a new one.

Within a single long chat, the same technique detects when the human left and came back. Check the Clock when activity resumes; compare to the last file write. If hours have passed, you're in a new work session within the same chat.

### 4. File Metadata as Context

When processing files the human drops in an inbox or working directory, the modified timestamp on those files tells you when the human placed them there. Email files (.eml) also contain send/receive timestamps in their headers. Both sources help reconstruct the timeline of events that happened between work sessions.

### 5. Cross-Referencing Timestamps

Screenshot filenames often contain timestamps (e.g. "Screenshot 2026-03-06 at 16.51.22.png"). Email headers contain send times. PDF metadata may contain creation dates. These all serve as independent time references when file metadata alone isn't sufficient.

---

For the deployable WORKFLOW section text, see the [temporal awareness template](../templates/workflow-sections/temporal-awareness.md).

---

## Limitations

Timestamps are approximate. The time on a file reflects when the AI wrote it, not when the human sent the message that prompted it. There's usually a small delay (seconds to minutes) depending on how much work the AI does before writing a file.

This only works with filesystem access (typically a desktop application). On mobile or web, the AI has no file metadata to work with and no temporal awareness.

File metadata reflects the timezone of the machine, which is useful but means the AI needs to note the timezone in log entries.

Within a single rapid exchange (messages seconds apart), the timestamps won't be meaningfully different. This is most useful for detecting gaps of minutes to hours.
