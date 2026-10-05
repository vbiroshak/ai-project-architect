# Sub-Project Activation

WORKFLOW section — universal pattern with project-specific domain examples and status file pointers.

## Template Text

```
---
SUB-PROJECT ACTIVATION

Activation runs before the first action on any request that belongs to a sub-project — a question, a search, a draft, an edit. Reading the status file is step one of the task, not preparation for it.

1. Read the sub-project's status file (see below): the landing page with its current state, pending items, and pointers to the sub-project's other files.
2. Read the files it points to for the kind of work at hand.
3. Read everything HANDOFF.txt identifies for that sub-project: session logs, work plans. Scale loading depth to complexity — a lightweight sub-project may need one log; a large active effort may need a work plan and multiple session logs.

Domain knowledge ([domain-specific examples]) goes in files inside the sub-project directory. PROJECT_INDEX.txt points to these files but does not hold domain content. Sub-project state — each live effort with its next step — goes in the status file, which is overwritten as state changes.

Completed sub-projects or finished efforts can be moved to Archive/ at the project root to keep the directory focused on active work. Add a closing note to the status file before archiving. An ARCHIVE_INDEX.txt inside Archive/ tracks what's there.

Sub-project status files:
  [Sub-Project Name]/ — [Sub-Project Name]/[SUBPROJECT]_STATUS.txt
  [Sub-Project Name]/ — [Sub-Project Name]/[SUBPROJECT]_STATUS.txt
```

## Notes

The domain examples phrase varies per project to match the work. Examples: "configuration notes, troubleshooting findings, setup procedures" for a technical project; "case data, draft history, research findings" for a correspondence project; "portfolio analysis, trade rationale, strategy updates" for a financial project. Choose examples that reflect the kinds of domain knowledge the sub-project produces.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.8*
