# Status File

Per sub-project orientation file. Read at activation. Overwritten as state changes. Verified against HANDOFF during paired writes.

**Naming:** Must include sub-project name or domain identifier. Never generic STATUS.txt. Examples: RESEARCH_STATUS.txt, CLIENTS_STATUS.txt, WEBSITE_STATUS.txt

## Structural Template

```
[PROJECT] [SUB-PROJECT] — STATUS
Last updated: [date] (Session NNN)
Last reviewed: [date]
[Optional role/tier line]

[Brief sub-project description, 1-3 sentences.]

---
CURRENT STATE

[What the sub-project looks like now. Active work, version numbers, recent completions. Dense factual summary.]

---
[EFFORT-SPECIFIC SECTIONS]

[Named sections for ongoing efforts. Each contains current state, decisions, and what's next. Add and remove as efforts begin and complete.]

---
PENDING

[Open items not tied to an effort section above.]
```

## Notes

CURRENT STATE is always present. Effort-specific sections and PENDING appear as needed — a simple sub-project may have only CURRENT STATE; a complex one may have multiple effort sections.

Status files orient sessions to sub-project state without requiring session log parsing — the sub-project equivalent of HANDOFF.txt.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.1*
