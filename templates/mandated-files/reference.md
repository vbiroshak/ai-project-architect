# REFERENCE.txt

Directory index read at startup alongside HANDOFF.txt: what exists, where, and what it's for. Located at Workflow Files/REFERENCE.txt.

## Structural Template

```
[PROJECT] — REFERENCE
Last updated: [date] (Session NNN)
Last reviewed: [date]

Project structure and reference details. Read at startup for structural context.

---
PROJECT FILE STRUCTURE

[Full directory tree with one-line descriptions, indented to show hierarchy.]

---
SESSION LOG FORMAT

Naming: Session_XXX.txt (three-digit, zero-padded, sequential). Location: Workflow Files/Session Logs/

Entry format:
  [date, ~time timezone] ENTRY HEADING
  Content...

Each entry captures: what was done, decisions and reasoning, file updates, what's next.

---
CONFIG BACKUP

Workflow Files/Config/PROJECT_INSTRUCTIONS.txt backs up the project instructions from your AI application's settings. Synced at startup (step 2). Also the source text for guiding project creation — read and present in conversation rather than directing the user to the Config directory.

---
SHARED KNOWLEDGE BASE

[path to shared knowledge base]

Shared knowledge base across all projects.

[Project-specific sections as needed]
```

## Example File Structure

```
Project/
  WORKFLOW.txt              entry point (read every startup)
  Inbox/                    asynchronous interface, both directions
  Sub-Project/              [one-line description]
    SUBPROJECT_STATUS.txt   orientation (current state)
  Workflow Files/           project-wide infrastructure
    HANDOFF.txt             startup orientation
    REFERENCE.txt           this file
    Clock/timestamp.txt
    Config/
      PROJECT_INSTRUCTIONS.txt
    Lessons/                operational knowledge (indexed)
    Session Logs/
      Session_XXX.txt
```

## Notes

Three universal sections (PROJECT FILE STRUCTURE, SESSION LOG FORMAT, CONFIG BACKUP) appear in every REFERENCE.txt. SHARED KNOWLEDGE BASE is included only for multi-project setups. Project-specific sections follow.

PROJECT FILE STRUCTURE must stay current when directory structure changes (see STRUCTURE CHANGES in the [session logs template](../workflow-sections/session-logs.md)).

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.1*
