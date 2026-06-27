# PROJECT_INDEX.txt (Chat)

Project file structure index for Chat projects. Read at startup alongside HANDOFF.txt: what exists, where, and what it's for. Located at Workflow Files/PROJECT_INDEX.txt. For Code projects, see the [Code PROJECT_INDEX template](../claude-code/PROJECT-INDEX-template.md).

## Structural Template

```
[PROJECT] — PROJECT INDEX
Last updated: [date] (Session NNN)
Last reviewed: [date]

Project file structure. Read at startup for structural context.

---
PROJECT FILE STRUCTURE

[Full directory tree with one-line descriptions, indented to show hierarchy.]

[Project-specific notes as needed, e.g. session log migration history.]
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
    PROJECT_INDEX.txt       this file
    Clock/timestamp.txt
    Config/
      PROJECT_INSTRUCTIONS.txt
    Lessons/                operational knowledge (indexed)
    Session Logs/
      Session_XXXX.txt
```

## Notes

PROJECT_INDEX.txt is a pure structural index. It contains the project's directory tree with one-line descriptions and nothing else. It does not hold domain knowledge (that belongs in sub-project reference files), session log format specs (that's in the WORKFLOW's SESSION LOGS section), config backup descriptions (that's in the WORKFLOW's startup step 2), or shared knowledge base paths (that's in the WORKFLOW's SHARED KNOWLEDGE BASE section).

PROJECT_INDEX.txt must stay current when directory structure changes (see STRUCTURE CHANGES in the [session logs template](../workflow-sections/session-logs.md)).

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.4*
