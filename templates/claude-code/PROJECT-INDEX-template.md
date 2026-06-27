# PROJECT_INDEX.txt (Code)

Project file structure index. Read at startup alongside HANDOFF.txt: what exists, where, and what it's for. Located at Project/PROJECT_INDEX.txt.

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
  CLAUDE.md                 startup procedure (auto-loaded by Code)
  .claude/                  Code configuration
    settings.json           permissions, hooks
    settings.local.json     output style, personal overrides
    hooks/                  event scripts
    output-styles/          behavioral profiles
  Inbox/                    asynchronous interface, both directions
  Sub-Project/              [one-line description]
    SUBPROJECT_STATUS.txt   orientation (current state)
  Project/                  project-wide infrastructure
    PROJECT_CONTEXT.md      governing document
    HANDOFF.txt             startup orientation
    PROJECT_INDEX.txt       this file
    TASKS.txt               active work items
    CHANGELOG.txt           structural/infrastructure changes
    Claude Memory/          auto memory (redirected)
    Lessons/                operational knowledge (indexed)
    Tool Guides/            on-demand tool reference
    Session Logs/
      Session_XXXX.txt
    Sessions/               archived transcripts
  Archive/                  completed sub-projects
```

## Notes

PROJECT_INDEX.txt is a pure structural index. It contains the project's directory tree with one-line descriptions and nothing else. It does not hold domain knowledge (that belongs in sub-project reference files) or operating instructions (that's in PROJECT_CONTEXT.md).

PROJECT_INDEX.txt must stay current when directory structure changes (see STRUCTURE CHANGES in the [PROJECT_CONTEXT template](PROJECT-CONTEXT-template.md)).

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.4*
