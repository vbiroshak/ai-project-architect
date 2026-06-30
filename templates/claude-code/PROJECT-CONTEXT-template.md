# PROJECT_CONTEXT.md Template

Governing document for a Code project. Place at `Project/PROJECT_CONTEXT.md`. Imported by CLAUDE.md at session start via the `@` syntax.

## Template Text

```
[PROJECTNAME] — PROJECT CONTEXT
Last updated: [Month DD, YYYY] (Session NNN)
Last reviewed: [Month DD, YYYY]

This is the project's governing document. It contains the rules, procedures, and project context that tell Claude how this project works and how to work in it. The startup procedure lives in CLAUDE.md; everything else lives here.

---
WHAT THIS PROJECT DOES

[Brief project description, 1-3 sentences.]

Current sub-projects:

  [Sub-Project Name]/ — [One-line description]

  [Sub-Project Name]/ — [One-line description]

See Project/PROJECT_INDEX.txt for file structure.

---
SUB-PROJECT ACTIVATION

To activate a sub-project:

1. Read the sub-project's reference file (see below)
2. Read everything HANDOFF.txt identifies for that sub-project: session logs, work plans, status files. Scale loading depth to complexity — a lightweight sub-project may need one log; a large active effort may need a work plan and multiple session logs.
3. Load any additional files needed for the current task

Domain knowledge ([domain-specific examples]) goes in files inside the sub-project directory. PROJECT_INDEX.txt points to these files but does not hold domain content.

Completed sub-projects or finished efforts can be moved to Archive/ at the project root to keep the directory focused on active work. Add a closing note to the status file before archiving. An ARCHIVE_INDEX.txt inside Archive/ tracks what's there.

Sub-project reference files:
  [Sub-Project Name]/ — [Sub-Project Name]/[REFERENCE_FILE].txt

---
SESSION LOGS

Location: Project/Session Logs/
Naming: Session_XXXX.txt (four-digit, zero-padded, sequential across the project). One log per session, numbered to match the session number.

ENTRY FORMAT: Each entry begins with a header line: [Date, ~Time Timezone] TOPIC

WHAT TO LOG: Decisions, state changes, reasoning, and the current state of evolving work. Not process narration. Thoroughness applies to coverage. Conciseness applies to expression.

LOG WHEN WORK ACCUMULATES: Write a log entry when substantive decisions, findings, or file changes have accumulated — when losing context now would cost the next session. Each entry should be self-contained. Multiple distinct topics means multiple entries within the same log.

WRITE FREQUENTLY: Sessions can end without warning. Never defer logging to "end of session" or wait to be asked. Logging is insurance against context loss, not a signal that work is finishing. After writing a log entry, continue working.

PAIRED WRITES: Every log entry is paired with a HANDOFF.txt overwrite — both happen together, every time. When the entry covers sub-project work, also verify the sub-project's status file reflects the current state.

STRUCTURE CHANGES: When file operations change directory structure (creating, moving, or renaming files or directories), verify Project/PROJECT_INDEX.txt reflects the current structure.

FIX ON CONTACT: When you encounter stale or incorrect information in a project file during normal work, fix it then and there before continuing with other work. Do not defer in any form — noting it for later, flagging it as pending, or adding it to a task list all count as deferring.

EVOLVING STATE: Log topics at their current state of progress, not as binary open/closed. Capture what was gathered, what was considered, where thinking landed, and what remains. Each in-progress item should let the next session continue where this one stopped, not restart from scratch.

FRESHNESS LINES: Every project file (except session logs) carries two lines after its title:

  Last updated: [Month DD, YYYY] (Session NNN)
  Last reviewed: [Month DD, YYYY]

"Last updated" means content was intentionally changed — adding, removing, revising, or restructuring. Updating only the freshness lines themselves does not count. "Last reviewed" means content was read and confirmed accurate during substantive work, whether or not anything changed. A correction refreshes both.

For files overwritten wholesale (HANDOFF, STATUS) or newly created, both lines carry the same date and session.

---
HANDOFF

Location: Project/HANDOFF.txt

The handoff gives the current state snapshot: where things stand, what to read for depth. Session logs are the archive. The handoff is the orientation. It is overwritten fresh with each paired write. The handoff controls how much context loads at startup — scale the pointers to the complexity of the work.

Sections:

  ACTIVE WORK — each item on its own line with its current state, sub-items indented under their header. This is the list the startup presents to the user: where work left off, what's pending. One item per line, not education on what each item is about. For each area of active work, point to everything the next session needs: session logs, key documents, status of open questions.

  STANDING ITEMS — active work that is paused but not completed, one item per line. Items here are ongoing, not queued — they can be picked up any session.

  FOR DEPTH — which session logs to read for additional context. After structural or meta work, note which earlier sessions contain the last domain work and carry forward the domain work narrative, prioritizing it above structural project system work.

Scope: handoff is limited to what the next session needs to continue the work. Rules, operating knowledge, and reference facts belong in governing documents. Completed work belongs in the session log.

---
INBOX

Location: Inbox/ (at project root)

Asynchronous interface between the user and the project, in both directions. The user drops files for processing; the AI writes drafts for review or anything needing the user's attention outside the current conversation.

Contents change at any time. List the directory before any reference to its contents — at startup, before mid-session processing, and before writing inbox references into the handoff. Before assessing an inbox item, check the project's existing work structure for related items. The handoff records actions taken but does not carry inbox filenames as a persistent list.

---
TEMPORAL AWARENESS

The temporal-awareness hook injects the current local time with every user message, so every turn has an accurate time reference. Consult it before any time-referential statement — greetings, "today"/"this morning", elapsed-time remarks.

---
TOOL GUIDES

[Include this section only if the project uses tools that need pre-read guides.]

Required guides to read before using tools.

  CHROME BROWSER: The web_fetch tool returns stale cached content for some sites therefore Claude may need to use Chrome for live web tasks. Before loading any Claude in Chrome tool via tool_search, read Project/Tool Guides/chrome-devtools-guide.txt. Try the tool first; if Chrome isn't running, the tool will say so and you can then ask the user to open it.

[Add entries for other project-specific tool guides as needed. Remove this entry if the project doesn't use Chrome.]

---
TASK QUEUE

[Include this section only if the project uses a file-based task queue.]

Project/TASKS.txt tracks open work only. No DONE section — completions go in session logs. Read at startup and fix any completed items.

Add new items as they come up. On completion, remove from TASKS.txt and note in the session log.

---
SHARED KNOWLEDGE BASE

[Include this section only if running multiple projects with a shared knowledge base.]

[path to shared knowledge base]

Shared knowledge base across all projects.

---
PROJECT CONTEXT

  FACTUAL GROUNDING: For verifiable claims in this project's domain (such as [domain-specific examples]), verify via search rather than relying on training data or assumptions.

  [Additional project-specific entries accumulate here through use]
```

## Notes

Sections marked "[Include this section only if...]" are optional. Remove them if the project doesn't need them.

The PROJECT CONTEXT section at the end is where project-specific corrections and behavioral entries accumulate through use. FACTUAL GROUNDING is the seed entry — replace the bracketed domain examples with examples relevant to your project.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.5*
