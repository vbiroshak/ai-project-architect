# Session Startup Procedure

WORKFLOW section — universal, identical across all projects.

## Template Text

```
---
SESSION STARTUP PROCEDURE

1. Confirm Filesystem tools are loaded for these essential operations: reading, writing, editing, creating directories, listing directory contents, getting file info, searching for files, moving files, and copying files to Claude. Use tool search queries broad enough to cover these operations together — per-verb queries often miss operations like move and search. If any of these essential filesystem operations aren't loaded now, run additional broad queries now until all are loaded.
2. Read Workflow Files/Config/PROJECT_INSTRUCTIONS.txt. If it differs from the project instructions in context, update the file to match. Do not narrate unless a discrepancy is found.
3. Check the clock and time since last logged interaction (see TEMPORAL AWARENESS below)
4. Read Workflow Files/PROJECT_INDEX.txt and Workflow Files/HANDOFF.txt
5. Read the most recent session log in Workflow Files/Session Logs/, plus any additional logs the handoff identifies.
6. If the project has a task queue, read it and fix any completed items.
7. List Inbox/ contents (filenames only, don't read)

Then present a brief orientation: where we left off, what's pending. Not education on what each item is about.
```

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.7*
