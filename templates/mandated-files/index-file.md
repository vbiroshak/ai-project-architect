# Index File

Per collection folder. Standing rule: any folder where a reader needs to discover and selectively access its contents gets an INDEX.txt at creation time. Does not apply to infrastructure folders with architecturally defined contents (Workflow Files/, Session Logs/, Config/).

Carries freshness lines. Updated when items are added, removed, or changed.

## Structural Template

```
[COLLECTION NAME] — INDEX
Last updated: [date] (Session NNN)
Last reviewed: [date]

[Optional description of what this collection contains.]

  [Item name or path]    [Description sufficient to decide whether to read it]
  [Item name or path]    [Description]
```

## Notes

Entry format adapts to the domain (topic tags for references, status for work plans, type classifications for templates).

Key principle: enough description per entry to decide whether to load without opening. An INDEX is a routing table, not a table of contents.

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.6*
